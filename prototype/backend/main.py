from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# 1. Define explicit response models with descriptive fields
class MessageResponse(BaseModel):
    message: str = Field(..., example="Welcome to CodeInsight API")
    status: str = Field(..., example="active")

class HealthResponse(BaseModel):
    status: str = Field(..., example="healthy")

# 2. Instantiate the app with rich metadata
app = FastAPI(
    title="CodeInsight API",
    description="Backend API services for CodeInsight Evidence Engine & Graph Explorer.",
    version="1.0.0",
    docs_url=None
)

# 3. Define endpoints with detailed descriptions
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

# 4. Documentation page utilizing the exact frontend stylesheet and structure
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
      </div>
    </main>
  </div>
</body>
</html>
"""
    return HTMLResponse(content=html_content)
