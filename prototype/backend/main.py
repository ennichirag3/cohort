import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi import HTTPException
from rag_pipeline import rag_pipeline

# 1. Define explicit response models with descriptive fields
class MessageResponse(BaseModel):
    message: str = Field(..., example="Welcome to CodeInsight API")
    status: str = Field(..., example="active")

class HealthResponse(BaseModel):
    status: str = Field(..., example="healthy")

class QueryRequest(BaseModel):
    question: str = Field(..., example="Why was Neo4j chosen over PostgreSQL for indexing repository entities?")
    repository: str | None = Field(
        default=None,
        max_length=200,
        example="pallets/click",
        description="Optional owner/repo filter. When omitted, evidence is searched across all imported repositories.",
    )

class RepositoryImportRequest(BaseModel):
    repository: str = Field(
        ...,
        min_length=3,
        max_length=500,
        example="https://github.com/pallets/click",
    )

class QueryResponse(BaseModel):
    answer: str
    sources: list[dict] = Field(default_factory=list)

# 2. Instantiate the app with rich metadata
app = FastAPI(
    title="CodeInsight API",
    description="Backend API services for CodeInsight Evidence Engine & Graph Explorer.",
    version="1.0.0",
    docs_url=None
)

# 3. Enable CORS middleware to allow communication from frontend (port 5500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Define standard endpoints
@app.get(
    "/", 
    tags=["Root"], 
    summary="Root Welcome Endpoint",
    description="Returns a welcoming status message confirming that the CodeInsight API backend is online and active.",
    response_model=MessageResponse
)
async def read_root():
    return {"message": "Welcome to CodeInsight API", "status": "active"}

@app.get(
    "/health", 
    tags=["System"], 
    summary="System Health Check",
    description="Performs a lightweight health check on the FastAPI application server to verify operational status.",
    response_model=HealthResponse
)
async def health_check():
    return {"status": "healthy"}


def parse_public_github_repository(value: str) -> tuple[str, str]:
    """Accept an owner/repo slug or HTTPS GitHub repository URL."""
    value = value.strip()
    if value.startswith("https://") or value.startswith("http://"):
        parsed = urlsplit(value)
        if (
            parsed.scheme != "https"
            or parsed.hostname != "github.com"
            or parsed.netloc.lower() != "github.com"
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
        ):
            raise HTTPException(
                status_code=422,
                detail="Enter a public GitHub repository URL such as https://github.com/owner/repo.",
            )
        parts = [part for part in parsed.path.strip("/").split("/") if part]
        if len(parts) != 2:
            raise HTTPException(
                status_code=422,
                detail="Use the repository URL only; remove tabs such as /issues or /pulls.",
            )
        owner, repo = parts
        if repo.endswith(".git"):
            repo = repo[:-4]
    else:
        parts = value.strip("/").split("/")
        if len(parts) != 2:
            raise HTTPException(
                status_code=422,
                detail="Enter owner/repo or a URL like https://github.com/owner/repo.",
            )
        owner, repo = parts
        if repo.endswith(".git"):
            repo = repo[:-4]

    if not re.fullmatch(r"[A-Za-z0-9_.-]+", owner) or not re.fullmatch(
        r"[A-Za-z0-9_.-]+", repo
    ):
        raise HTTPException(
            status_code=422,
            detail="The GitHub owner or repository name contains unsupported characters.",
        )
    return owner, repo


@app.post(
    "/api/repositories",
    tags=["GitHub Ingestion"],
    summary="Import a public GitHub repository",
    description=(
        "Fetches a bounded window of recent public commits, merged pull requests, "
        "and issues, then imports them into Neo4j. A token is optional for public "
        "repositories, but can help when GitHub's unauthenticated API rate limit is reached."
    ),
)
def add_github_repository(body: RepositoryImportRequest):
    owner, repo = parse_public_github_repository(body.repository)
    backend_dir = Path(__file__).parent
    fetch_script = backend_dir / "fetch_github_data.py"

    try:
        with tempfile.TemporaryDirectory(prefix="codeinsight-github-") as temp_dir:
            output_path = Path(temp_dir) / "repository.json"
            command = [
                sys.executable,
                str(fetch_script),
                "--owner", owner,
                "--repo", repo,
                "--commits", "20",
                "--pull-requests", "10",
                "--issues", "15",
                "--commit-details", "8",
                "--linked-issue-details", "5",
                "--output", str(output_path),
            ]
            result = subprocess.run(
                command,
                cwd=backend_dir,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )
            if result.returncode != 0:
                message = (result.stderr or result.stdout or "GitHub ingestion failed.").strip()
                raise HTTPException(status_code=502, detail=message[-1500:])

            with output_path.open(encoding="utf-8") as dataset_file:
                data = json.load(dataset_file)

        from import_sample import import_repository_data

        import_repository_data(data)
    except subprocess.TimeoutExpired as exc:
        raise HTTPException(
            status_code=504,
            detail="GitHub took too long to respond. Try again in a moment.",
        ) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Could not save repository data to Neo4j: {exc}",
        ) from exc

    return {
        "status": "imported",
        "repository": data["repository"]["id"],
        "counts": {
            "commits": len(data.get("commits", [])),
            "pull_requests": len(data.get("pull_requests", [])),
            "issues": len(data.get("issues", [])),
        },
        "message": f"Imported recent public history for {owner}/{repo} into Neo4j.",
    }

# 5. Main GraphRAG Query Endpoint
@app.post(
    "/api/ask",
    tags=["GraphRAG"],
    summary="Execute Architectural Query",
    description="Searches Neo4j for graph evidence related to the question, optionally limited to one imported repository.",
    response_model=QueryResponse,
)
def ask_question(body: QueryRequest):
    try:
        evidence = rag_pipeline.fetch_graph_evidence(
            body.question,
            repository=body.repository,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Could not retrieve evidence from Neo4j: {exc}",
        ) from exc

    sources = []

    for record in evidence:
        detail = (
            record.get("detail")
            or record.get("summary")
            or record.get("description")
            or record.get("message")
            or record.get("body")
            or ""
        )
        title = (
            record.get("title")
            or (detail.splitlines()[0][:180] if detail else None)
            or str(record.get("identifier", "Graph evidence"))
        )

        sources.append(
            {
                "type": record.get("entity_type", "Evidence"),
                "title": title,
                "url": record.get("source_url") or record.get("url"),
                "excerpt": detail or title,
                "detail": detail or title,
                "identifier": str(record.get("identifier", "")),
                "author": record.get("author", "Unknown"),
                "date": str(record.get("date", "N/A")),
            }
        )

    if not sources:
        answer = (
            "I couldn't find matching evidence in the Neo4j graph. "
            "Try asking with specific words that appear in a commit, issue, or pull request."
        )
    else:
        answer = (
            f"I found {len(sources)} matching record(s) in the Neo4j graph. "
            "Review the sources for the supporting evidence."
        )

    return {"answer": answer, "sources": sources}

# 6. Live Graph Explorer endpoint backed by Neo4j
@app.get(
    "/api/graph",
    tags=["GraphRAG"],
    summary="Get Knowledge Graph Topology",
    description="Retrieves real Neo4j nodes and relationships for Graph Explorer.",
)
def get_graph_topology(q: str | None = None):
    if not rag_pipeline.driver:
        return {"status": "Neo4j disconnected", "nodes": [], "edges": []}

    search_term = q.strip().lower() if q and q.strip() else None

    cypher_query = """
    MATCH (n)-[rel]->(m)
    WHERE $search_term IS NULL
       OR any(value IN [
            toLower(coalesce(n.id, "")),
            toLower(coalesce(n.title, "")),
            toLower(coalesce(n.message, "")),
            toLower(coalesce(n.name, "")),
            toLower(coalesce(n.path, "")),
            toLower(coalesce(n.body, "")),
            toLower(coalesce(n.summary, "")),
            toLower(coalesce(n.description, ""))
       ] WHERE value CONTAINS $search_term)
       OR any(value IN [
            toLower(coalesce(m.id, "")),
            toLower(coalesce(m.title, "")),
            toLower(coalesce(m.message, "")),
            toLower(coalesce(m.name, "")),
            toLower(coalesce(m.path, "")),
            toLower(coalesce(m.body, "")),
            toLower(coalesce(m.summary, "")),
            toLower(coalesce(m.description, ""))
       ] WHERE value CONTAINS $search_term)
    RETURN
        elementId(n) AS source_id,
        labels(n)[0] AS source_type,
        coalesce(n.name, n.title, n.message, n.id, n.path, "Node") AS source_label,
        coalesce(n.id, n.sha, n.number, elementId(n)) AS source_key,
        coalesce(n.message, n.title, n.body, n.summary, n.description, n.path, "") AS source_detail,
        coalesce(n.author, n.author_login, n.user, "Unknown") AS source_author,
        coalesce(n.date, n.committed_at, n.created_at, "") AS source_date,
        coalesce(n.url, n.source_url, n.html_url, "") AS source_url,
        coalesce(n.path, "") AS source_path,
        elementId(m) AS target_id,
        labels(m)[0] AS target_type,
        coalesce(m.name, m.title, m.message, m.id, m.path, "Node") AS target_label,
        coalesce(m.id, m.sha, m.number, elementId(m)) AS target_key,
        coalesce(m.message, m.title, m.body, m.summary, m.description, m.path, "") AS target_detail,
        coalesce(m.author, m.author_login, m.user, "Unknown") AS target_author,
        coalesce(m.date, m.committed_at, m.created_at, "") AS target_date,
        coalesce(m.url, m.source_url, m.html_url, "") AS target_url,
        coalesce(m.path, "") AS target_path,
        type(rel) AS relation
    LIMIT 100
    """

    nodes = []
    edges = []
    added_nodes = set()

    try:
        with rag_pipeline.driver.session() as session:
            records = session.run(cypher_query, search_term=search_term)

            for record in records:
                source_id = str(record["source_id"])
                target_id = str(record["target_id"])

                if source_id not in added_nodes:
                    nodes.append({
                        "id": source_id,
                        "label": str(record["source_label"]),
                        "type": str(record["source_type"]),
                        "details": {
                            "id": str(record["source_key"]),
                            "text": str(record["source_detail"] or ""),
                            "author": str(record["source_author"] or "Unknown"),
                            "date": str(record["source_date"] or ""),
                            "url": str(record["source_url"] or ""),
                            "path": str(record["source_path"] or ""),
                        },
                    })
                    added_nodes.add(source_id)

                if target_id not in added_nodes:
                    nodes.append({
                        "id": target_id,
                        "label": str(record["target_label"]),
                        "type": str(record["target_type"]),
                        "details": {
                            "id": str(record["target_key"]),
                            "text": str(record["target_detail"] or ""),
                            "author": str(record["target_author"] or "Unknown"),
                            "date": str(record["target_date"] or ""),
                            "url": str(record["target_url"] or ""),
                            "path": str(record["target_path"] or ""),
                        },
                    })
                    added_nodes.add(target_id)

                edges.append({
                    "source": source_id,
                    "target": target_id,
                    "relation": str(record["relation"]),
                })

        return {"status": "connected", "nodes": nodes, "edges": edges}
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Could not load the Neo4j graph: {exc}",
        ) from exc

# 7. Project API documentation page
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CodeInsight API Documentation</title>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      color-scheme: dark;
      --bg-dark: #080914;
      --card-bg: rgba(20, 22, 45, 0.55);
      --card-border: rgba(255, 255, 255, 0.08);
      --primary-accent: #7a35ff;
      --secondary-accent: #00d2ff;
      --pink-accent: #e024a3;
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      min-height: 100vh;
      overflow-x: hidden;
      position: relative;
      background: var(--bg-dark);
      color: var(--text-main);
      font: 15px/1.6 'Plus Jakarta Sans', sans-serif;
    }
    a { color: var(--secondary-accent); }
    .ambient-glow { position: fixed; border-radius: 50%; filter: blur(120px); z-index: -1; pointer-events: none; opacity: .45; }
    .glow-1 { width: 500px; height: 500px; top: -100px; right: -100px; background: radial-gradient(circle, var(--primary-accent), transparent 70%); }
    .glow-2 { width: 450px; height: 450px; bottom: -50px; left: -100px; background: radial-gradient(circle, var(--pink-accent), transparent 70%); }
    .glow-3 { width: 350px; height: 350px; top: 40%; left: 30%; background: radial-gradient(circle, var(--secondary-accent), transparent 70%); }
    .app-container { max-width: 1100px; margin: 0 auto; padding: 1.5rem 2rem; }
    .navbar { display: flex; justify-content: space-between; align-items: center; gap: 1.5rem; padding: 1rem 0; margin-bottom: 2.5rem; }
    .logo { display: flex; align-items: center; gap: .5rem; font-size: 1.25rem; letter-spacing: .5px; white-space: nowrap; }
    .logo-icon { color: #ff8c42; }
    .logo-text b { color: var(--secondary-accent); }
    .nav-links { display: flex; gap: 2rem; align-items: center; background: rgba(255,255,255,.03); padding: .6rem 1.5rem; border: 1px solid var(--card-border); border-radius: 50px; backdrop-filter: blur(10px); }
    .nav-item { color: var(--text-muted); font-size: .9rem; text-decoration: none; white-space: nowrap; transition: color .25s ease, transform .25s ease; }
    .nav-item.active, .nav-item:hover { color: var(--text-main); transform: translateY(-1px); }
    main { animation: page-enter .55s cubic-bezier(.2,.75,.25,1) both; }
    .hero { max-width: 750px; margin: 0 auto 2rem; text-align: center; animation: page-enter .55s ease both; }
    .eyebrow { display: inline-block; color: #e9d5ff; background: linear-gradient(90deg,var(--primary-accent),var(--pink-accent)); padding: .25rem .75rem; border-radius: 20px; font-size: .75rem; font-weight: 800; letter-spacing: 1px; }
    h1 { margin: .8rem 0 1rem; font-size: clamp(2.4rem, 5vw, 3.5rem); line-height: 1.12; background: linear-gradient(180deg,#fff 0%,#a5b4fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    h2 { margin: 0 0 .75rem; font-size: 1.25rem; }
    p { margin: .7rem 0; color: var(--text-muted); }
    .card, .note { animation: page-enter .5s ease both; }
    .card { margin: 1rem 0; padding: 1.75rem; background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 16px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: 0 20px 40px rgba(0,0,0,.4); transition: border-color .25s ease, transform .25s ease, box-shadow .25s ease; }
    .card:hover { transform: translateY(-2px); border-color: rgba(122,53,255,.35); box-shadow: 0 24px 46px rgba(0,0,0,.42); }
    .endpoint { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; margin-bottom: 8px; }
    .method { color: #07131a; background: var(--secondary-accent); border-radius: 6px; padding: 3px 9px; font-size: 12px; font-weight: 800; }
    .method.post { background: #34d399; }
    code, pre, textarea { font: 13px/1.55 'JetBrains Mono', Consolas, monospace; }
    .path { color: var(--text-main); font-size: 16px; font-weight: 700; }
    .muted { color: var(--text-muted); }
    pre { overflow: auto; white-space: pre-wrap; overflow-wrap: anywhere; padding: 14px; color: #dbeafe; background: rgba(8,9,20,.88); border: 1px solid var(--card-border); border-radius: 10px; }
    textarea { width: 100%; min-height: 76px; resize: vertical; padding: 12px; color: var(--text-main); background: rgba(8,9,20,.88); border: 1px solid var(--card-border); border-radius: 9px; }
    textarea:focus, input:focus { outline: 2px solid rgba(122,53,255,.65); outline-offset: 2px; }
    button { margin-top: 10px; padding: 10px 15px; color: white; font-weight: 700; background: linear-gradient(90deg,var(--primary-accent),#0ea5e9); border: 0; border-radius: 9px; cursor: pointer; transition: transform .2s ease, box-shadow .2s ease, filter .2s ease; }
    button:hover { transform: translateY(-2px); filter: brightness(1.08); box-shadow: 0 0 24px rgba(0,210,255,.35); }
    button:active { transform: translateY(0); }
    .try-row { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
    .try-row input { flex: 1; min-width: 220px; padding: 10px 12px; color: var(--text-main); background: rgba(8,9,20,.88); border: 1px solid var(--card-border); border-radius: 9px; font: inherit; }
    .try-output { margin-top: 12px; }
    .note { margin: 1rem 0; padding: 1rem 1.2rem; color: var(--text-main); background: rgba(0,210,255,.06); border: 1px solid var(--card-border); border-left: 3px solid var(--secondary-accent); border-radius: 4px 12px 12px 4px; }
    .note strong { color: var(--secondary-accent); }
    @keyframes page-enter { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
    @media (max-width: 720px) { .app-container { padding: 1rem; } .navbar { align-items: flex-start; flex-direction: column; margin-bottom: 1.75rem; } .nav-links { width: 100%; justify-content: space-between; gap: .65rem; padding: .6rem .85rem; } .nav-item { font-size: .78rem; } .card { padding: 1.2rem; } }
    @media (prefers-reduced-motion: reduce) { *, *::before, *::after { scroll-behavior: auto !important; animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; } }
  </style>
</head>
<body>
  <div class="ambient-glow glow-1"></div>
  <div class="ambient-glow glow-2"></div>
  <div class="ambient-glow glow-3"></div>
  <div class="app-container">
  <nav class="navbar" aria-label="Main navigation">
    <div class="logo">
      <span class="logo-icon">⚡</span>
      <span class="logo-text">CODE<b>INSIGHT</b></span>
    </div>
    <div class="nav-links">
      <a href="http://127.0.0.1:5500/index.html" class="nav-item">Evidence Engine</a>
      <a href="http://127.0.0.1:5500/graph.html" class="nav-item">Graph Explorer</a>
      <a href="/docs" class="nav-item active" aria-current="page">Documentation</a>
    </div>
  </nav>
  <main>
    <section class="hero">
      <span class="eyebrow">API REFERENCE · VERSION 1.0</span>
      <h1>CodeInsight API</h1>
      <p>Endpoints used by the Evidence Engine and Graph Explorer. Try them here while the backend is running.</p>
      <p><a href="/openapi.json" target="_blank" rel="noopener">Open the machine-readable API schema</a></p>
    </section>

    <div class="note"><strong>Local setup:</strong> start FastAPI from <code>prototype/backend</code> with <code>python -m uvicorn main:app --reload</code>. Neo4j features need <code>NEO4J_URI</code>, <code>NEO4J_USERNAME</code>, and <code>NEO4J_PASSWORD</code> in <code>prototype/backend/.env</code>. For public GitHub imports, <code>GITHUB_TOKEN</code> is optional; add a fine-grained, read-only token there if you hit GitHub's unauthenticated rate limit. Keep <code>.env</code> private and out of Git.</div>

    <section class="card">
      <div class="endpoint"><span class="method">GET</span><span class="path">/</span></div>
      <p>Confirms the API is responding.</p>
      <pre>{
  "message": "Welcome to CodeInsight API",
  "status": "active"
}</pre>
      <button type="button" onclick="tryEndpoint('/', 'rootOutput')">Try GET /</button>
      <pre id="rootOutput" class="try-output" hidden></pre>
    </section>

    <section class="card">
      <div class="endpoint"><span class="method">GET</span><span class="path">/health</span></div>
      <p>Checks that the FastAPI process is responding. This check does not verify the Neo4j connection.</p>
      <pre>{ "status": "healthy" }</pre>
      <button type="button" onclick="tryEndpoint('/health', 'healthOutput')">Check API health</button>
      <pre id="healthOutput" class="try-output" hidden></pre>
    </section>

    <section class="card">
      <div class="endpoint"><span class="method post">POST</span><span class="path">/api/repositories</span></div>
      <p>Fetches a bounded sample of recent history from a public GitHub repository and imports it into Neo4j. Enter the repository URL or its <code>owner/repo</code> name. Public imports need no token, though GitHub may rate-limit repeated unauthenticated requests.</p>
      <p><strong>Example request</strong> (replace <code>owner/repo</code> with the public repository you want to import)</p>
      <pre>{ "repository": "owner/repo" }</pre>
      <p><strong>Example successful response</strong> (record counts vary)</p>
      <pre>{
  "status": "imported",
  "repository": "owner/repo",
  "counts": { "commits": 20, "pull_requests": 10, "issues": 15 },
  "message": "Imported recent public history for owner/repo into Neo4j."
}</pre>
      <p class="muted">Each import requests up to 20 commits, 10 merged pull requests, and 15 issues; GitHub may return fewer. This API reference shows examples, not live import status. Check the success message on the Evidence Engine; after a successful import, Graph Explorer focuses on that repository. An unsuccessful import does not change the selected graph.</p>
    </section>

    <section class="card">
      <div class="endpoint"><span class="method post">POST</span><span class="path">/api/ask</span></div>
      <p>Searches imported commit, pull request, and issue text for matching words. The Evidence Engine limits searches to the most recently imported repository; API requests can pass an optional <code>repository</code> field (owner/repo). If it is omitted, evidence is searched across all imported repositories. For best results, use a distinctive word from a commit, PR, or issue.</p>
      <p><strong>Request body</strong></p>
      <pre>{ "question": "empty string", "repository": "pallets/click" }</pre>
      <p><strong>Response shape</strong></p>
      <pre>{
  "answer": "I found 2 matching record(s) in the Neo4j graph. Review the sources for the supporting evidence.",
  "sources": [
    { "type": "Commit", "title": "Example commit message", "url": "https://github.com/...", "excerpt": "Example evidence" }
  ]
}</pre>
      <label for="askQuestion"><strong>Try a question</strong></label>
      <textarea id="askQuestion">empty string</textarea>
      <button type="button" onclick="tryAsk()">Send question</button>
      <pre id="askOutput" class="try-output" hidden></pre>
    </section>

    <section class="card">
      <div class="endpoint"><span class="method">GET</span><span class="path">/api/graph?q={optional text}</span></div>
      <p>Returns up to 100 Neo4j relationships as nodes and edges. Add <code>?q=psf%2Frequests</code> to filter for one repository and its related history, or use another text fragment to filter matching nodes. Graph Explorer uses the most recently imported repository after a successful import.</p>
      <pre>{
  "status": "connected",
  "nodes": [
    { "id": "node-id", "label": "Commit message", "type": "Commit", "details": { "id": "full-id", "text": "...", "author": "...", "date": "...", "url": "...", "path": "..." } }
  ],
  "edges": [ { "source": "node-id", "target": "other-node-id", "relation": "HAS_COMMIT" } ]
}</pre>
      <div class="try-row">
        <button type="button" onclick="tryGraph()">Load graph response</button>
        <input id="graphFilter" aria-label="Optional graph filter" placeholder="Optional filter, e.g. psf/requests">
      </div>
      <pre id="graphOutput" class="try-output" hidden></pre>
    </section>

    <p class="muted">Common errors: <code>422</code> means the request is invalid; <code>502</code> means GitHub rejected the fetch (including rate limits); <code>503</code> means Neo4j could not be reached; <code>504</code> means GitHub took too long. If GitHub rate-limits a public import, wait for its limit to reset or configure optional <code>GITHUB_TOKEN</code> in the ignored backend <code>.env</code> file, then restart FastAPI.</p>
  </main>
  </div>
  <script>
    async function tryEndpoint(path, outputId) {
      await showResponse(path, outputId);
    }

    async function tryAsk() {
      const question = document.getElementById('askQuestion').value.trim();
      const output = document.getElementById('askOutput');
      if (!question) {
        output.hidden = false;
        output.textContent = 'Enter a question first.';
        return;
      }
      await showResponse('/api/ask', 'askOutput', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
    }

    async function tryGraph() {
      const filter = document.getElementById('graphFilter').value.trim();
      const path = filter ? `/api/graph?q=${encodeURIComponent(filter)}` : '/api/graph';
      await showResponse(path, 'graphOutput');
    }

    async function showResponse(path, outputId, options = {}) {
      const output = document.getElementById(outputId);
      output.hidden = false;
      output.textContent = 'Loading…';
      try {
        const response = await fetch(path, options);
        const body = await response.json();
        output.textContent = `HTTP ${response.status}\n${JSON.stringify(body, null, 2)}`;
      } catch (error) {
        output.textContent = `Request failed: ${error.message}. Confirm the FastAPI server is running.`;
      }
    }
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)
