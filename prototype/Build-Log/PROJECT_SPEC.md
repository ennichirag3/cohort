# Project Specification: "Why The Code Is Like This" RAG Assistant

## 1. Project Overview & System Scope
Developers frequently struggle to understand historical context behind architectural decisions, legacy trade-offs, and design patterns within a codebase. The **"Why The Code Is Like This"** assistant is a Retrieval-Augmented Generation (RAG) system that connects developer natural language queries to a structured **Neo4j Knowledge Graph** containing Git commits, pull requests, issues, and developer discussion logs.

The primary objective is to deliver **factual, zero-hallucination, source-backed explanations** for architectural decisions, complete with direct citations to specific commits and PRs.

---

## 2. Team Composition & Role Distribution

| Team Member | Role | Core Responsibilities | Key Build-Log Deliverables |
| :--- | :--- | :--- | :--- |
| **Manas** | Tech & Neo4j Lead | Graph database modeling in Neo4j AuraDB, Cypher query optimization, schema constraints. | `Entry-2.md` |
| **Anirudh** | Data & Ingestion Lead | Repository parsing (commits/PRs/issues), data normalization, and Neo4j batch ingestion. | `Entry-2.md` |
| **Anshika** | AI & RAG Lead | RAG pipeline (`rag_pipeline.py`), FastAPI server (`main.py`), prompt engineering, temperature guardrails. | `Entry-3.md`, `Entry-4.md` |
| **Shreya** | Evaluation & Security Lead | Faithfulness metrics, claim classification, refusal precision, and input/output guardrails. | `Entry-4.md`, `Entry-5.md` |
| **Chirag** | Frontend & QA Lead | Glassmorphic UI (`index.html`, `styles.css`, `app.js`), async API integration, failure testing, stranger testing. | `Entry-5.md`, `Entry-6.md` |

---

## 3. Technology Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Graph Database**: Neo4j AuraDB (Cypher Query Language)
- **AI / LLM Framework**: OpenAI API (`gpt-4o` / custom embeddings), LangChain / LlamaIndex context utilities
- **Frontend**: Glassmorphic UI (HTML5, Custom CSS3, Vanilla JS ES6+)
- **Environment & Configuration**: `python-dotenv`, Git / GitHub

---

## 4. System Architecture & Data Flow

1. **User Query Input**: The developer submits a question via the glassmorphic web dashboard (e.g., *"Why did we move from Redis to Memcached?"*).
2. **Cypher Generation & Context Retrieval**: The backend RAG engine converts or maps the query into an optimized Cypher statement to query Neo4j.
3. **Subgraph Extraction**: Relevant nodes (`:Commit`, `:PullRequest`, `:Issue`, `:Developer`, `:File`) and their relationships are retrieved.
4. **Bounded LLM Generation**: The extracted graph context is passed to the LLM with a `0.0` temperature setting and strict system prompts requiring source attribution.
5. **Claims Classification & Response**: Post-generation guardrails verify that all claims are backed by retrieved graph nodes before streaming the citations and answer back to the frontend UI.

---

## 5. Knowledge Graph Schema

### Nodes
- `:Commit` (`hash`, `author`, `timestamp`, `message`)
- `:PullRequest` (`id`, `title`, `body`, `status`)
- `:Issue` (`id`, `title`, `description`, `state`)
- `:Developer` (`username`, `email`)
- `:File` (`path`, `module`)

### Relationships
- `(:Developer)-[:AUTHORED]->(:Commit)`
- `(:Commit)-[:MERGED_INTO]->(:PullRequest)`
- `(:PullRequest)-[:CLOSES]->(:Issue)`
- `(:Commit)-[:MODIFIED]->(:File)`
- `(:Developer)-[:COMMENTED_ON]->(:PullRequest)`

---

## 6. Guardrail & Evaluation Specifications

- **Hallucination Prevention**: Prompts explicitly instruct the model to state *"Insufficient context in knowledge graph to answer this query"* if relevant graph nodes are missing.
- **Citation Enforcement**: Every response must cite at least one explicit commit hash or pull request ID.
- **Input Sanitization**: Client-side and server-side checks reject malicious injection attempts or malformed Cypher/SQL syntax.
- **Evaluation Metrics**: Measured on Faithfulness Score, Citation Accuracy, and Refusal Precision across a standardized benchmark test set.
