# Entry 3: RAG Pipeline, Guardrails & Prompt Engineering

## 1. Module Overview & Primary Lead
- **Module Lead**: Anshika (AI & RAG Lead)
- **Co-Lead / Contributor**: Shreya (Evaluation & Security Lead)
- **Collaborators**: Manas (Neo4j Context Retrieval), Anirudh (Context Structuring), Chirag (Backend API Integration)

---

## 2. Retrieval-Augmented Generation (RAG) Architecture
The RAG pipeline (`rag_pipeline.py`) bridges developer natural language queries with the Neo4j knowledge graph to deliver accurate, context-bound explanations.

1. **Query Parsing**: Translates developer questions into structured Cypher database queries.
2. **Context Retrieval**: Fetches relevant nodes and relationships (commits, PRs, issues) from Neo4j.
3. **Context Construction**: Formats raw graph data into clean, chronological context blocks for LLM processing.
4. **Response Generation**: Generates source-backed explanations using strictly bounded prompts.

---

## 3. Zero-Temperature & Prompt Engineering
To eliminate LLM hallucinations when explaining code choices:
- **Temperature Setting**: Set strictly to `0.0` for deterministic, reproducible answers.
- **Strict Grounding**: System prompts force the model to rely solely on the provided graph context.
- **Fall-back Handling**: If the retrieved context lacks sufficient evidence, the model responds with: *"Insufficient context in knowledge graph to answer this query."*

---

## 4. API Integration & Guardrail Layer
- Integrated within `main.py` via FastAPI endpoints.
- Pre-processing checks sanitize input queries against injection attacks.
- Post-processing checks ensure every output claim cites a specific commit, PR, or issue ID.
