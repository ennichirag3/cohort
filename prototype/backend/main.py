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

# 5. Main GraphRAG Query Endpoint
@app.post(
    "/api/ask",
    tags=["GraphRAG"],
    summary="Execute Architectural Query",
    description="Searches Neo4j for graph evidence related to the question.",
    response_model=QueryResponse,
)
def ask_question(body: QueryRequest):
    try:
        evidence = rag_pipeline.fetch_graph_evidence(body.question)
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Could not retrieve evidence from Neo4j: {exc}",
        ) from exc

    sources = []

    for record in evidence:
        title = (
            record.get("title")
            or record.get("summary")
            or record.get("message")
            or record.get("description")
            or str(record.get("identifier", "Graph evidence"))
        )

        sources.append(
            {
                "type": record.get("entity_type", "Evidence"),
                "title": title,
                "url": record.get("source_url") or record.get("url"),
                "excerpt": record.get("summary")
                or record.get("description")
                or record.get("message")
                or title,
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

# 6. Graph Explorer Topology Endpoint
@app.get(
    "/api/graph",
    tags=["GraphRAG"],
    summary="Get Knowledge Graph Topology",
    description="Retrieves nodes and edges for the Graph Explorer visualizer."
)
async def get_graph_topology():
    return {
        "nodes": [
            {"id": "decision_1", "label": "Decision Node", "type": "Decision", "detail": "Neo4j Choice"},
            {"id": "commit_1", "label": "Commit #a1b2c3d", "type": "Commit"},
            {"id": "pr_1", "label": "PR #14 GraphRAG", "type": "PullRequest"},
            {"id": "file_1", "label": "rag_pipeline.py", "type": "File"},
            {"id": "index_1", "label": "Neo4j Vector Index", "type": "Index"}
        ],
        "edges": [
            {"source": "decision_1", "target": "commit_1", "relation": "JUSTIFIED_BY"},
            {"source": "decision_1", "target": "pr_1", "relation": "IMPLEMENTED_IN"},
            {"source": "decision_1", "target": "index_1", "relation": "STORED_IN"},
            {"source": "decision_1", "target": "file_1", "relation": "DEPENDS_ON"}
        ]
    }

# 7. Custom Documentation page utilizing the exact frontend stylesheet and structure
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CodeInsight - API Documentation</title>
  <link rel="stylesheet" href="http://127.0.0.1:5500/prototype/frontend/styles.css">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
  <style>
    .navbar {
      position: sticky !important;
      top: 0 !important;
      z-index: 9999 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      background: rgba(9, 8, 20, 0.85) !important;
      backdrop-filter: blur(12px) !important;
    }
    .logo-text {
      color: #ffffff !important;
    }
    .logo-text b {
      color: #38bdf8 !important;
    }
    .doc-container {
      max-width: 900px;
      width: 100%;
      margin: 40px auto;
      padding: 0 24px;
    }
    .hero-header {
      text-align: center;
      margin-bottom: 40px;
    }
    .glass-card {
      background: rgba(18, 16, 38, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 28px;
      margin-bottom: 20px;
      backdrop-filter: blur(16px);
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.35);
    }
    .endpoint-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }
    .method-badge {
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 4px 10px;
      border-radius: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 600;
    }
    .endpoint-path {
      font-family: 'JetBrains Mono', monospace;
      font-size: 15px;
      color: #ffffff;
      font-weight: 600;
      letter-spacing: -0.02em;
    }
    .endpoint-desc {
      color: #94a3b8;
      font-size: 14px;
      margin-bottom: 20px;
      line-height: 1.5;
    }
    .response-section-title {
      font-size: 11px;
      font-weight: 700;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 8px;
    }
    pre {
      background: rgba(9, 8, 20, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 10px;
      padding: 16px;
      margin: 0;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      color: #38bdf8;
      overflow-x: auto;
    }
    pre .key { color: #c084fc; }
    pre .str { color: #34d399; }
  </style>
</head>
<body>
  <!-- Ambient Gradient Background Glows -->
  <div class="ambient-glow glow-1"></div>
  <div class="ambient-glow glow-2"></div>

  <div class="app-container">
    <!-- Navbar -->
    <nav class="navbar">
      <a href="http://127.0.0.1:5500/prototype/frontend/index.html" class="logo" style="text-decoration: none;">
        <span class="logo-icon">⚡</span>
        <span class="logo-text">CODE<b>INSIGHT</b></span>
      </a>
      <div class="nav-links">
        <a href="http://127.0.0.1:5500/prototype/frontend/index.html" class="nav-item">Evidence Engine</a>
        <a href="http://127.0.0.1:5500/prototype/frontend/graph.html" class="nav-item">Graph Explorer</a>
        <a href="http://127.0.0.1:8000/docs" class="nav-item active">Documentation</a>
      </div>
    </nav>

    <!-- Main Section -->
    <main class="hero-section" style="flex: 1;">
      <div class="hero-header">
        <span class="tag-badge">API REFERENCE v1.0.0</span>
        <h1 class="hero-title">CodeInsight API Documentation</h1>
        <p class="hero-subtitle">Explore operational backend endpoints powering the Evidence Engine and Graph Explorer.</p>
      </div>

      <div class="doc-container" style="margin: 0 auto; padding: 0;">
        <!-- Endpoint Card 1: Root -->
        <div class="glass-card">
          <div class="endpoint-header">
            <span class="method-badge">GET</span>
            <span class="endpoint-path">/</span>
          </div>
          <div class="endpoint-desc">Returns a welcoming status message confirming that the CodeInsight API backend is online and active.</div>
          <div class="response-section-title">Response Example (200 OK)</div>
          <pre>{
  <span class="key">"message"</span>: <span class="str">"Welcome to CodeInsight API"</span>,
  <span class="key">"status"</span>: <span class="str">"active"</span>
}</pre>
        </div>

        <!-- Endpoint Card 2: Health -->
        <div class="glass-card">
          <div class="endpoint-header">
            <span class="method-badge">GET</span>
            <span class="endpoint-path">/health</span>
          </div>
          <div class="endpoint-desc">Performs a lightweight health check on the FastAPI application server to verify operational status.</div>
          <div class="response-section-title">Response Example (200 OK)</div>
          <pre>{
  <span class="key">"status"</span>: <span class="str">"healthy"</span>
}</pre>
        </div>

        <!-- Endpoint Card 3: Ask -->
        <div class="glass-card">
          <div class="endpoint-header">
            <span class="method-badge">POST</span>
            <span class="endpoint-path">/api/ask</span>
          </div>
          <div class="endpoint-desc">Accepts an architectural question, queries the Neo4j GraphRAG pipeline, and returns a synthesized response with evidence.</div>
          <div class="response-section-title">Response Example (200 OK)</div>
          <pre>{
  <span class="key">"answer"</span>: <span class="str">"Processed query regarding architectural decisions..."</span>,
  <span class="key">"sources"</span>: [<span class="str">"main.py"</span>, <span class="str">"rag_pipeline.py"</span>]
}</pre>
        </div>
      </div>
    </main>
  </div>
</body>
</html>
"""
    return HTMLResponse(content=html_content)
