import os
import re
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from neo4j import GraphDatabase


# Load credentials from prototype/backend/.env, regardless of the terminal folder.
load_dotenv(Path(__file__).with_name(".env"))

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER") or os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

NO_EVIDENCE_ANSWER = "Insufficient evidence in repository history to answer this question."

STOP_WORDS = {
    "a", "about", "an", "and", "are", "as", "at", "be", "been", "by",
    "can", "code", "does", "do", "for", "from", "had", "has", "have",
    "how", "i", "in", "is", "it", "of", "on", "or", "our", "the", "their",
    "this", "to", "was", "were", "what", "when", "where", "which", "who",
    "why", "will", "with", "would", "new", "change", "changes", "changed",
    "support", "supports", "request", "requests", "body", "handling", "handle",
    "ignore", "ignores", "option", "options", "pass", "through", "limit",
    "limits", "fastapi", "starlette",
}


class EvidenceRAGPipeline:
    """Find repository evidence in Neo4j and summarize it without a paid LLM."""

    def __init__(self) -> None:
        self.driver = None

        if NEO4J_URI and NEO4J_PASSWORD:
            self.driver = GraphDatabase.driver(
                NEO4J_URI,
                auth=(NEO4J_USER, NEO4J_PASSWORD),
            )

    def extract_keywords(self, question: str) -> List[str]:
        """Keep meaningful words from a natural-language question."""
        words = re.findall(r"[a-zA-Z0-9_]+", question.lower())

        keywords = [
            word
            for word in words
            if len(word) > 1
            and word not in STOP_WORDS
        ]

        # Remove duplicates while keeping the original order.
        return list(dict.fromkeys(keywords))

    def fetch_graph_evidence(
        self,
        question: str,
        repository: str | None = None,
    ) -> List[Dict[str, Any]]:
        """Return matching records, optionally restricted to one repository."""
        if not self.driver:
            raise RuntimeError(
                "Neo4j is not configured. Check NEO4J_URI, "
                "NEO4J_USERNAME, and NEO4J_PASSWORD in prototype/backend/.env."
            )

        keywords = self.extract_keywords(question)
        if not keywords:
            return []

        repository = repository.strip().lower() if repository and repository.strip() else None

        cypher_query = """
        MATCH (e)
        WHERE (e:Commit OR e:PullRequest OR e:Issue)
          AND (
              $repository IS NULL OR (
                  e.id IS NOT NULL AND (
                      toLower(toString(e.id)) STARTS WITH $repository + "@"
                      OR toLower(toString(e.id)) STARTS WITH $repository + "#"
                  )
              )
          )
        WITH e,
            toLower(coalesce(e.title, "")) AS title_text,
            toLower(coalesce(e.message, "")) AS message_text,
            toLower(coalesce(e.summary, "")) AS summary_text,
            toLower(coalesce(e.description, "")) AS description_text,
            toLower(coalesce(e.body, "")) AS body_text
        WITH e, title_text, message_text, summary_text, description_text, body_text,
            reduce(
                score = 0,
                keyword IN $keywords |
                score + CASE
                    WHEN title_text CONTAINS keyword OR message_text CONTAINS keyword
                    THEN 3
                    WHEN summary_text CONTAINS keyword OR description_text CONTAINS keyword
                    THEN 2
                    WHEN body_text CONTAINS keyword
                    THEN 1
                    ELSE 0
                END
            ) AS match_score
        WHERE match_score > 0
        RETURN
            labels(e)[0] AS entity_type,
            coalesce(e.hash, e.id, e.number, "N/A") AS identifier,
            coalesce(e.message, e.title, e.body, e.summary, e.description, "")
                AS detail,
            coalesce(e.author, e.author_login, e.user, "Unknown") AS author,
            coalesce(
                e.date,
                e.committed_at,
                e.created_at,
                "Unknown Date"
            ) AS date,
            coalesce(e.url, e.source_url, e.html_url, "") AS url,
            match_score,
            CASE
                WHEN e.id CONTAINS "@" THEN split(e.id, "@")[0]
                WHEN e.id CONTAINS "#" THEN split(e.id, "#")[0]
                ELSE ""
            END AS repository,
            "Direct keyword match" AS match_reason
        ORDER BY match_score DESC, toString(date) DESC
        LIMIT 10
        """

        with self.driver.session() as session:
            result = session.run(
                cypher_query,
                keywords=keywords,
                repository=repository,
            )
            direct_records = [record.data() for record in result]

            matched_issue_ids = [
                record["identifier"]
                for record in direct_records
                if record.get("entity_type") == "Issue"
            ]
            related_records = []
            if matched_issue_ids:
                related_query = """
                MATCH (i:Issue)<-[:REFERENCES_ISSUE]-(p:PullRequest)
                WHERE i.id IN $issue_ids
                RETURN
                    "PullRequest" AS entity_type,
                    p.id AS identifier,
                    coalesce(p.title, p.body, "") AS detail,
                    coalesce(p.author, "Unknown") AS author,
                    coalesce(p.merged_at, p.created_at, "Unknown Date") AS date,
                    coalesce(p.url, p.source_url, "") AS url,
                    0 AS match_score,
                    split(p.id, "#")[0] AS repository,
                    "Linked to matching issue " + i.id AS match_reason
                UNION
                MATCH (i:Issue)<-[:REFERENCES_ISSUE]-(p:PullRequest)-[:INCLUDES_COMMIT]->(c:Commit)
                WHERE i.id IN $issue_ids
                RETURN
                    "Commit" AS entity_type,
                    c.id AS identifier,
                    coalesce(c.message, "") AS detail,
                    coalesce(c.author, "Unknown") AS author,
                    coalesce(c.date, "Unknown Date") AS date,
                    coalesce(c.url, c.source_url, "") AS url,
                    0 AS match_score,
                    split(c.id, "@")[0] AS repository,
                    "Linked through PR " + p.id + " for issue " + i.id AS match_reason
                LIMIT 10
                """
                related_result = session.run(
                    related_query,
                    issue_ids=matched_issue_ids,
                )
                related_records = [record.data() for record in related_result]

        seen = {
            (record.get("entity_type"), str(record.get("identifier", "")))
            for record in direct_records
        }
        for record in related_records:
            key = (record.get("entity_type"), str(record.get("identifier", "")))
            if key not in seen:
                direct_records.append(record)
                seen.add(key)

        return direct_records

    def make_evidence_answer(
        self,
        evidence_records: List[Dict[str, Any]],
    ) -> str:
        """Summarize what matching records say without inventing a rationale."""
        if not evidence_records:
            return NO_EVIDENCE_ANSWER

        lines = [
            "### DIRECT EVIDENCE",
            "These repository records matched the words in your question:",
        ]

        for record in evidence_records[:5]:
            detail = str(record.get("detail") or "").replace("\n", " ").strip()
            if len(detail) > 500:
                detail = detail[:497] + "..."

            lines.append(
                f"- **[{record.get('entity_type', 'Evidence')}]** "
                f"`{record.get('identifier', 'N/A')}`: {detail}"
            )

        lines.extend(
            [
                "",
                "### LIMITATION",
                "These records show what was recorded, but matching text alone "
                "does not prove why the change was made. Open the source links "
                "to read the original context.",
                "",
                "*(Generated using the no-cost evidence path.)*",
            ]
        )
        return "\n".join(lines)

    def answer_question(self, question: str) -> Dict[str, Any]:
        """Retrieve matching records and return an evidence-based response."""
        question = question.strip()
        if not question:
            return {
                "question": question,
                "answer": NO_EVIDENCE_ANSWER,
                "evidence_found": False,
                "sources": [],
            }

        evidence_records = self.fetch_graph_evidence(question)

        return {
            "question": question,
            "answer": self.make_evidence_answer(evidence_records),
            "evidence_found": bool(evidence_records),
            "sources": evidence_records,
        }

    def close(self) -> None:
        if self.driver:
            self.driver.close()


# main.py imports this shared instance.
rag_pipeline = EvidenceRAGPipeline()
