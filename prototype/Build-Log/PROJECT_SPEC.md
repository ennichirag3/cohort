# PROJECT_SPEC.md

## 1. What is this?
An evidence-backed developer assistant that queries a Neo4j knowledge graph of Git commits, PRs, and issues to explain architectural decisions with traceable citations.

## 2. Who uses it?
Software engineers, maintainers, and onboarding developers seeking historical context behind codebase choices.

## 3. What must it do?
- Accept public GitHub repo metadata and user why-questions.
- Graph-traverse `:Commit`, `:PullRequest`, `:Issue`, `:Developer`, and `:File` nodes.
- Return zero-hallucination answers citing exact commit hashes and PR IDs.
- Explicitly refuse to answer when evidence in the graph is insufficient.

## 4. What does it NOT do?
- Does not edit, write, or refactor source code files.
- Does not index private repositories without access tokens.

## 5. Technology Stack
- **Frontend**: HTML5, Glassmorphic CSS3, Vanilla JS ES6+
- **Backend**: Python FastAPI, Uvicorn
- **Database**: Neo4j AuraDB (Cypher Query Language)
- **AI / RAG**: OpenAI API (`gpt-4o`), LangChain, Zero-temperature (`0.0`) settings

## 6. Definition of Done
A user enters a why-question, receives a factual answer grounded in graph nodes, and can click a citation card to open the corresponding GitHub PR/commit.
