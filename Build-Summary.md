# BUILD_SUMMARY.md: "Why The Code Is Like This" RAG Assistant

## 1. Executive Summary
The **"Why The Code Is Like This"** RAG Assistant is an enterprise-grade retrieval-augmented generation system designed to eliminate architectural context loss in software development teams. By connecting a **FastAPI** backend with a **Neo4j Knowledge Graph** and presenting results through an interactive **Glassmorphic UI**, the platform allows engineers to query legacy code choices, trade-offs, and refactors, receiving factual, source-backed explanations grounded in raw Git commits, PR discussions, and issue logs.

---

## 2. Technical Stack & System Architecture
- **Backend API**: Python 3.10+, FastAPI, Uvicorn
- **Knowledge Graph Database**: Neo4j AuraDB (Cypher Query Language)
- **RAG & Guardrail Engine**: OpenAI API (`gpt-4o`), LangChain utilities, zero-temperature execution (`0.0`)
- **Frontend Interface**: HTML5, CSS3 Glassmorphism design system, Vanilla JS ES6+ (`fetch` API)
- **Security & Evaluation Layer**: Claims classification, refusal precision, and input/output guardrails

---

## 3. Team Roster & Module Breakdown

| Team Member | Domain / Role | Primary Responsibilities | Key Deliverables |
| :--- | :--- | :--- | :--- |
| **Manas** | Tech & Neo4j Lead | Schema definition, Neo4j AuraDB setup, index optimization, and Cypher query templates. | `Entry-2.md` |
| **Anirudh** | Data & Ingestion Lead | GitHub API integration, commit/PR log parsing, data normalization, and batch graph loading. | `Entry-2.md` |
| **Anshika** | AI & RAG Lead | RAG pipeline architecture (`rag_pipeline.py`), FastAPI backend (`main.py`), and zero-temp system prompts. | `Entry-3.md`, `Entry-4.md` |
| **Shreya** | Evaluation & Security Lead | Faithfulness evaluation, claim classification framework, refusal triggers, and security guardrails. | `Entry-4.md`, `Entry-5.md` |
| **Chirag** | Frontend & QA Lead | Glassmorphic interface (`index.html`, `app.js`), async API integration, failure testing, and stranger testing execution. | `Entry-5.md`, `Entry-6.md` |

---

## 4. Completed Build Milestones

### 1. Knowledge Graph Schema & Ingestion (`Entry-1.md`, `Entry-2.md`)
- Established graph entities: `:Commit`, `:PullRequest`, `:Issue`, `:Developer`, and `:File`.
- Wired directional relationships (`:AUTHORED`, `:MERGED_INTO`, `:CLOSES`, `:MODIFIED`) for clear lineage tracking.
- Implemented batch ingestion pipelines parsing raw GitHub metadata into Neo4j nodes.

### 2. RAG Pipeline & Zero-Hallucination Guardrails (`Entry-3.md`, `Entry-4.md`)
- Constructed `rag_pipeline.py` to map natural language queries into target Cypher lookups.
- Enforced a strict `0.0` LLM temperature setting to guarantee deterministic outputs.
- Built claims classification rules ensuring every generated statement cites a valid commit hash or PR ID, returning *"Insufficient context in knowledge graph to answer this query"* when graph evidence is absent.

### 3. Frontend Development & Stranger Testing (`Entry-5.md`, `Entry-6.md`)
- Designed and connected a responsive glassmorphic web dashboard with real-time feedback states.
- Validated failure recovery under empty context states, network timeouts, and bad inputs.
- Conducted stranger testing with external engineers to optimize query suggestions and citation card clarity.

---

## 5. Repository Deployment Status
- **GitHub Repository**: Synchronized with `ennichirag3/cohort`.
- **Environment Protection**: `.env` and `venv/` files untracked via project root `.gitignore`.
- **Documentation**: All core documentation files (`PROJECT_SPEC.md`, `Entry-1.md` to `Entry-6.md`, `BUILD_SUMMARY.md`) verified and complete.
