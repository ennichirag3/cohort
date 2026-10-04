import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
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
    allow_origins=[
        "https://cohort-do0y.onrender.com",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=False,
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
                "repository": record.get("repository") or body.repository or "",
                "match_reason": record.get("match_reason", "Direct keyword match"),
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
        direct_count = sum(
            source["match_reason"] == "Direct keyword match"
            for source in sources
        )
        related_count = len(sources) - direct_count
        answer = (
            f"I found {direct_count} direct text match(es) and "
            f"{related_count} linked context record(s) in the Neo4j graph. "
            "Review the sources for supporting evidence."
        )

    return {"answer": answer, "sources": sources}

# 6. Live Graph Explorer endpoint backed by Neo4j
@app.get(
    "/api/graph",
    tags=["GraphRAG"],
    summary="Get Knowledge Graph Topology",
    description="Retrieves real Neo4j nodes and relationships for Graph Explorer.",
)
def get_graph_topology(
    q: str | None = None,
    focus: str | None = Query(default=None, max_length=2000),
):
    if not rag_pipeline.driver:
        return {"status": "Neo4j disconnected", "nodes": [], "edges": []}

    search_term = q.strip().lower().rstrip("/") if q and q.strip() else None
    focus_ids = [value.strip().lower() for value in (focus or "").split(",") if value.strip()]

    cypher_query = """
    MATCH (n)-[rel]->(m)
    WITH n, rel, m,
         toLower(toString(coalesce(n.id, ""))) AS source_key,
         toLower(toString(coalesce(m.id, ""))) AS target_key
    WHERE $search_term IS NULL
       OR source_key = $search_term
       OR target_key = $search_term
       OR source_key STARTS WITH $search_term + "@"
       OR source_key STARTS WITH $search_term + "#"
       OR source_key STARTS WITH $search_term + ":"
       OR target_key STARTS WITH $search_term + "@"
       OR target_key STARTS WITH $search_term + "#"
       OR target_key STARTS WITH $search_term + ":"
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
    ORDER BY
        CASE WHEN source_key IN $focus_ids OR target_key IN $focus_ids THEN 0 ELSE 1 END,
        CASE type(rel)
            WHEN "HAS_PULL_REQUEST" THEN 0
            WHEN "HAS_ISSUE" THEN 1
            WHEN "HAS_COMMIT" THEN 2
            WHEN "INCLUDES_COMMIT" THEN 3
            WHEN "REFERENCES_ISSUE" THEN 4
            WHEN "CHANGED" THEN 5
            WHEN "AUTHORED_BY" THEN 6
            ELSE 7
        END,
        source_type, source_key, target_type, target_key
    LIMIT 150
    """

    nodes = []
    edges = []
    added_nodes = set()

    try:
        with rag_pipeline.driver.session() as session:
            records = session.run(
                cypher_query,
                search_term=search_term,
                focus_ids=focus_ids,
            )

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

# 7. Keep the backend docs URL as a same-tab entry point to the frontend documentation page.
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return RedirectResponse(url="https://cohort-do0y.onrender.com/docs.html", status_code=307)
