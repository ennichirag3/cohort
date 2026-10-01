# PROJECT_SPEC.md

## 1. What is this?
An evidence-backed developer assistant that queries a Neo4j knowledge graph of Git commits, PRs, and issues to explain architectural decisions with traceable citations[span_70](start_span)[span_70](end_span).

## 2. Who uses it?
Software engineers, maintainers, and onboarding developers seeking historical context behind codebase choices[span_71](start_span)[span_71](end_span).

## 3. What must it do?
- Accept public GitHub repo metadata and user why-questions[span_72](start_span)[span_72](end_span).
- Graph-traverse `:Commit`, `:PullRequest`, `:Issue`, `:Developer`, and `:File` nodes[span_73](start_span)[span_73](end_span).
- Return zero-hallucination answers citing exact commit hashes and PR IDs[span_74](start_span)[span_74](end_span).
- Explicitly refuse to answer when evidence in the graph is insufficient[span_75](start_span)[span_75](end_span).

## 4. What does it NOT do?
- Does not edit, write, or refactor source code files[span_76](start_span)[span_76](end_span).
- Does not index private repositories without access tokens[span_77](start_span)[span_77](end_span).

## 5. Technology Stack
- **Frontend**: HTML5, Glassmorphic CSS3, Vanilla JS ES6+[span_78](start_span)[span_78](end_span)
- **Backend**: Python FastAPI, Uvicorn[span_79](start_span)[span_79](end_span)
- **Database**: Neo4j AuraDB (Cypher Query Language)[span_80](start_span)[span_80](end_span)
- **AI / RAG**: OpenAI API (`gpt-4o`), LangChain, Zero-temperature (`0.0`) settings[span_81](start_span)[span_81](end_span)

## 6. Definition of Done
A user enters a why-question, receives a factual answer grounded in graph nodes, and can click a citation card to open the corresponding GitHub PR/commit[span_82](start_span)[span_82](end_span).
