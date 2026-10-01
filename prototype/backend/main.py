from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# 1. Instantiate the app first
app = FastAPI(docs_url=None)

# 2. Define standard endpoints so the OpenAPI spec isn't empty
@app.get("/", tags=["Root"], summary="Root Endpoint")
async def read_root():
    return {"message": "Welcome to CodeInsight API", "status": "active"}

@app.get("/health", tags=["System"], summary="Health Check")
async def health_check():
    return {"status": "healthy"}

# 3. Custom Swagger UI route returning raw HTML (no get_swagger_ui_html helper needed)
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>CodeInsight - API Documentation</title>
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
            * {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                box-sizing: border-box;
            }
            body {
                background: #090814 !important;
                color: #e2e8f0 !important;
                margin: 0;
                padding: 0;
            }
            /* Top Navigation Bar */
            .custom-navbar {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 14px 32px;
                background: rgba(18, 16, 38, 0.85);
                backdrop-filter: blur(12px);
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                position: sticky;
                top: 0;
                z-index: 99999;
            }
            .nav-brand {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 16px;
                font-weight: 700;
                color: #ffffff;
                text-decoration: none;
            }
            .nav-links {
                display: flex;
                gap: 12px;
            }
            .nav-btn {
                padding: 6px 14px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                color: #e2e8f0;
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.12);
                text-decoration: none;
            }
            .nav-btn:hover {
                background: rgba(139, 92, 246, 0.3);
                color: #ffffff;
            }

            /* Swagger UI Custom Dark Glassmorphism */
            .swagger-ui .topbar { display: none !important; }
            .swagger-ui { 
                width: 90% !important; 
                max-width: 1100px !important; 
                margin: 30px auto !important; 
            }
            .swagger-ui .info .title { color: #ffffff !important; font-weight: 800 !important; }
            .swagger-ui .info p, .swagger-ui .info a { color: #94a3b8 !important; }
            .swagger-ui .opblock-tag { color: #c084fc !important; border-bottom: 1px solid rgba(255,255,255,0.08) !important; }
            
            .swagger-ui .opblock, .swagger-ui section.models { 
                background: rgba(18, 16, 38, 0.75) !important; 
                border: 1px solid rgba(255, 255, 255, 0.08) !important; 
                border-radius: 10px !important; 
            }

            /* Clean up schema boxes */
            .swagger-ui section.models h4,
            .swagger-ui .model-box, 
            .swagger-ui .model-title, 
            .swagger-ui span.model-title { 
                background: transparent !important; 
                color: #f1f5f9 !important;
                box-shadow: none !important;
            }

            .swagger-ui .model-title, 
            .swagger-ui .opblock-summary-path { 
                font-family: 'JetBrains Mono', monospace !important;
            }
            .swagger-ui .model-toggle:after { filter: invert(100%); }
        </style>
    </head>
    <body>
        <!-- Top Navigation Bar -->
        <nav class="custom-navbar">
            <a href="#" class="nav-brand">
                <span>⚡</span> CODE<b>INSIGHT</b>
            </a>
            <div class="nav-links">
                <a href="http://127.0.0.1:5500/prototype/frontend/index.html" class="nav-btn">← Evidence Engine</a>
                <a href="http://127.0.0.1:5500/prototype/frontend/graph.html" class="nav-btn">Graph Explorer</a>
            </div>
        </nav>

        <!-- Swagger UI Root Container -->
        <div id="swagger-ui"></div>

        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            window.onload = () => {
                window.ui = SwaggerUIBundle({
                    url: '/openapi.json',
                    dom_id: '#swagger-ui',
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIBundle.SwaggerUIStandalonePreset
                    ],
                    layout: "BaseLayout",
                    deepLinking: true
                });
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
