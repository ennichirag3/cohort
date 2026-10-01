import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Load environment variables from .env
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER") or os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class EvidenceRAGPipeline:
    def __init__(self):
        # Initialize Neo4j Driver safely with URI validation
        if NEO4J_URI and NEO4J_PASSWORD and NEO4J_URI.strip():
            try:
                self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            except Exception as e:
                print(f"Warning: Neo4j Driver failed to initialize: {e}")
                self.driver = None
        else:
            self.driver = None

        # Initialize LLM with zero temperature for factual adherence
        # Uses explicit key or falls back gracefully
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.0,
            api_key=OPENAI_API_KEY if OPENAI_API_KEY else "dummy-key-for-init"
        )

        # Define system prompt enforcing strict evidence vs inference separation
        self.prompt_template = PromptTemplate(
            template="""
You are an evidence-backed software architecture assistant. Your job is to explain WHY a codebase or module was designed a certain way based strictly on historical repository context.

STRICT INSTRUCTIONS:
1. Base your answer ONLY on the provided Repository Evidence below.
2. If the provided evidence contains enough information, explain the reasoning clearly.
3. Explicitly categorize your findings into:
   - DIRECT EVIDENCE: Historical facts, commit messages, PR discussions, and issue comments.
   - INFERENCE: Logical interpretations directly supported by the evidence.
4. CITE SOURCES: Include exact commit hashes, PR IDs, author names, dates, and source URLs where applicable.
5. FALLBACK RULE: If the retrieved evidence does NOT contain the reason or is empty, output EXACTLY this response:
   "Insufficient evidence in repository history to answer this question." Do NOT speculate or invent reasons.

Repository Evidence:
{context}

User Question:
{question}

Structured Answer:
""",
            input_variables=["context", "question"]
        )

    def fetch_graph_evidence(self, question: str) -> List[Dict[str, Any]]:
        """
        Retrieves relevant commits, pull requests, and issues from Neo4j.
        Supports multiple schema property naming variations.
        """
        if not self.driver:
            return []

        # Cypher query with multi-property fallbacks
        cypher_query = """
        MATCH (e)
        WHERE (e:Commit OR e:PullRequest OR e:Issue OR e:Decision)
          AND (toLower(coalesce(e.message, "")) CONTAINS toLower($query) 
            OR toLower(coalesce(e.description, "")) CONTAINS toLower($query)
            OR toLower(coalesce(e.summary, "")) CONTAINS toLower($query)
            OR toLower(coalesce(e.body, "")) CONTAINS toLower($query)
            OR toLower(coalesce(e.title, "")) CONTAINS toLower($query))
        RETURN 
            labels(e)[0] AS entity_type,
            coalesce(e.hash, e.id, e.number, "N/A") AS identifier,
            coalesce(e.message, e.summary, e.title, e.description, e.body, "") AS detail,
            coalesce(e.author, e.user, "Unknown") AS author,
            coalesce(e.date, e.created_at, "Unknown Date") AS date,
            coalesce(e.url, e.html_url, "") AS url
        LIMIT 5
        """
        try:
            with self.driver.session() as session:
                result = session.run(cypher_query, query=question)
                records = [record.data() for record in result]
                return records
        except Exception as e:
            print(f"Error querying Neo4j: {e}")
            return []

    def format_context(self, evidence_records: List[Dict[str, Any]]) -> str:
        """Formats Neo4j records into a structured context string for the LLM."""
        if not evidence_records:
            return ""

        formatted_str = ""
        for idx, item in enumerate(evidence_records, start=1):
            formatted_str += f"--- Record {idx} [{item.get('entity_type')}] ---\n"
            formatted_str += f"ID: {item.get('identifier')}\n"
            formatted_str += f"Author: {item.get('author')} | Date: {item.get('date')}\n"
            formatted_str += f"Details: {item.get('detail')}\n"
            if item.get('url'):
                formatted_str += f"URL: {item.get('url')}\n"
            formatted_str += "\n"
        return formatted_str

    def answer_question(self, question: str) -> Dict[str, Any]:
        """Runs retrieval, checks context sufficiency, and invokes the LLM chain."""
        evidence_records = self.fetch_graph_evidence(question)
        context = self.format_context(evidence_records)

        # Fallback early if no graph context is returned
        if not context.strip():
            return {
                "question": question,
                "answer": "Insufficient evidence in repository history to answer this question.",
                "evidence_found": False,
                "sources": []
            }

        # Run LLM chain
        chain = self.prompt_template | self.llm
        response = chain.invoke({"context": context, "question": question})
        answer_text = response.content.strip()

        return {
            "question": question,
            "answer": answer_text,
            "evidence_found": "Insufficient evidence" not in answer_text,
            "sources": evidence_records
        }

    def close(self):
        if self.driver:
            self.driver.close()

# Singleton instance for export
rag_pipeline = EvidenceRAGPipeline()
