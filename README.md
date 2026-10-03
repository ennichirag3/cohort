# Why The Code Is Like This

An evidence explorer for public GitHub repository history. Import a bounded set of commits, merged pull requests, and issues into Neo4j, then search for matching records and inspect their original source links.

## Hosted app

[https://cohort-do0y.onrender.com](https://cohort-do0y.onrender.com)

The frontend includes Evidence Engine, Graph Explorer, and Documentation pages.

## What it does

1. Enter a public GitHub repository URL or owner/repo.
2. Import recent history into Neo4j.
3. Ask a question using distinctive words from the behavior or change.
4. Review matching records and source links in Evidence Engine, or explore stored relationships in Graph Explorer.

The current question path uses keyword extraction and match scoring. It returns matching repository records; it does not use an LLM to generate an explanation or prove historical intent. Review the original sources before drawing conclusions.

## Project layout

- prototype/frontend/ — Evidence Engine, Graph Explorer, Documentation, and shared styling.
- prototype/backend/ — FastAPI endpoints, GitHub ingestion, Neo4j importer, and retrieval.
- prototype/backend/data/ — sample and final normalized datasets for pallets/click.
- Build-Log/ — Activities 1–6 and the project specification.
- Build-Summary.md — final project summary.

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

The frontend's Evidence Engine and Graph Explorer currently point to the hosted backend at https://repoinsight-qjj0.onrender.com. To use a locally running backend, change the API_BASE_URL in app.js and the graph API base in graph.html to http://127.0.0.1:8000. The Documentation page selects the local API when served on port 5500.

## Import limits and known constraints

- Imports are limited to recent public history: up to 20 commits, 10 merged pull requests, and 15 issues, with bounded extra detail requests.
- The importer does not clone the complete repository history.
- Private repositories are not supported by the current endpoint.
- Keyword retrieval can miss relevant records or return unrelated matches.
- Matching text is not proof of why a change was made; inspect the source links.
- Neo4j-backed features require valid credentials and an available database.
- User testing and comparative search-time results are not documented in the project files.

## Main files

- prototype/backend/main.py — API routes and repository-import limits.
- prototype/backend/fetch_github_data.py — GitHub REST API ingestion.
- prototype/backend/import_sample.py — normalized data import into Neo4j.
- prototype/backend/rag_pipeline.py — keyword retrieval and evidence response.
- prototype/backend/schema.cypher — Neo4j uniqueness constraints.
- prototype/frontend/index.html — Evidence Engine.
- prototype/frontend/graph.html — Graph Explorer.
- prototype/frontend/docs.html — API documentation.