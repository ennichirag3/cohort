# Entry 1: Team Onboarding & System Scope

## 1. Team Responsibilities
- **Anshika (AI & RAG Lead)**: RAG pipeline implementation (`rag_pipeline.py`), FastAPI backend server (`main.py`), prompt engineering with zero-temperature guardrails, and claims classification (`Entry-3.md`, `Entry-4.md`).
- **Chirag (Frontend & QA Lead)**: Glassmorphic user interface (`index.html`, `styles.css`, `app.js`), async API integration, failure case validation, and stranger testing documentation (`Entry-5.md`, `Entry-6.md`).
- **Manas (Tech & Neo4j Lead)**: Graph database modeling in Neo4j AuraDB, schema definition, Cypher query optimization, and entity ingestion (`Entry-2.md`).

## 2. Core Problem & System Objective
Developers often lack historical context regarding architectural decisions. The "Why The Code Is Like This" assistant queries a Neo4j knowledge graph containing commits, PRs, and issues to provide factual, source-backed explanations for developer queries without hallucination.
