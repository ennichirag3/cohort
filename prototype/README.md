# Why The Code Is Like This

An evidence explorer for public GitHub repository history. Import a bounded set of commits, merged pull requests, and issues into Neo4j, then search for matching records and inspect their original source links.

## Hosted app

[https://cohort-do0y.onrender.com](https://cohort-do0y.onrender.com)

The frontend includes Evidence Engine, Graph Explorer, and Documentation pages.

## What it does

1. Enter a public GitHub repository URL or owner/repo.
2. Import recent history into Neo4j.
3. Ask a question using distinctive words from the behavior or change.
4. Review direct text matches and any linked context records in Evidence Engine. Open Graph Explorer in the same tab to see those matches and their direct graph connections.

The current question path uses keyword extraction and weighted match scoring. It returns up to 10 direct text matches and may add up to 10 PR/commit records linked to matched issues when those relationships exist in Neo4j. It does not use an LLM to generate an explanation or prove historical intent. Review the original sources before drawing conclusions.

## Project layout

- ../PROJECT_GUIDE.md — detailed product, architecture, graph, setup, deployment, and evidence guide.
- frontend/ — Evidence Engine, Graph Explorer, Documentation, and shared styling.
- backend/ — FastAPI endpoints, GitHub ingestion, Neo4j importer, and retrieval.
- backend/data/ — bundled normalized dataset for `pallets/click`.
- ../Build-Log/ — the compiled Build Log and supporting screenshots.
- ../Build-Summary.md — final project summary.

## Run the backend locally

Requirements: Python 3.10 or newer and a reachable Neo4j database.

1. Open a terminal in prototype/backend.
2. Create and activate a virtual environment, then install dependencies:

   - python -m venv .venv
   - On Windows PowerShell: ./.venv/Scripts/Activate.ps1
   - pip install -r requirements.txt

3. Create prototype/backend/.env with your own Neo4j credentials:

   - NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
   - NEO4J_USERNAME=neo4j
   - NEO4J_PASSWORD=your-password

   GITHUB_TOKEN is optional for public imports and may help when GitHub rate limits unauthenticated requests. Keep .env out of Git.

4. In Neo4j Browser, run prototype/backend/schema.cypher once to create the uniqueness constraints.
5. Start the API from prototype/backend with: uvicorn main:app --reload --port 8000

## Run the frontend locally

Serve the files in prototype/frontend with VS Code Live Server or another static web server. For example, from that directory, run: python -m http.server 5500

Open http://127.0.0.1:5500/index.html.

When opened on localhost, the Evidence Engine and Graph Explorer automatically use the local API at http://127.0.0.1:8000. On the hosted site, they use https://repoinsight-qjj0.onrender.com. The Documentation page also selects the local API when served on port 5500.

## Import limits and known constraints

- Imports are limited to recent public history: up to 20 recent commits, 10 merged pull requests, and 15 issues, with bounded extra detail requests. Commits attached to fetched PRs can increase the total commit count.
- The importer does not clone the complete repository history.
- Private repositories are not supported by the current endpoint.
- Keyword retrieval can miss relevant records or return unrelated matches.
- PR/commit context is added only when an imported pull request has a `REFERENCES_ISSUE` link to a directly matched issue. A PR or commit can appear in Graph Explorer without being a direct text match for the question.
- Matching text is not proof of why a change was made; inspect the source links.
- Neo4j-backed features require valid credentials and an available database.
- One manual demonstration and a two-participant exploratory stranger test are documented in Build-Log/Build-Log.md. Systematic retrieval evaluation and comparative search-time results are not established.

## Main files

- `backend/main.py` — API routes and repository-import limits.
- `backend/fetch_github_data.py` — GitHub REST API ingestion.
- `backend/import_sample.py` — normalized data import into Neo4j.
- `backend/rag_pipeline.py` — keyword retrieval and evidence response.
- `backend/schema.cypher` — Neo4j uniqueness constraints.
- `frontend/index.html` — Evidence Engine.
- `frontend/graph.html` — Graph Explorer.
- `frontend/docs.html` — interactive API documentation.
