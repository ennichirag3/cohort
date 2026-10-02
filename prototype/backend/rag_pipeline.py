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
    "why", "will", "with",
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
        WITH e, [
            toLower(coalesce(e.message, "")),
            toLower(coalesce(e.title, "")),
            toLower(coalesce(e.body, "")),
            toLower(coalesce(e.summary, "")),
            toLower(coalesce(e.description, ""))
        ] AS searchable_text
        WITH e, searchable_text,
            reduce(
                score = 0,
                keyword IN $keywords |
                score + CASE
                    WHEN any(text IN searchable_text WHERE text CONTAINS keyword)
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
            match_score
        ORDER BY match_score DESC, toString(date) DESC
        LIMIT 10
        """

        with self.driver.session() as session:
            result = session.run(
                cypher_query,
                keywords=keywords,
                repository=repository,
            )
            return [record.data() for record in result]

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
