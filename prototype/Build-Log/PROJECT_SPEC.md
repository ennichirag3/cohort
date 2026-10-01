# Technical Specification: Why The Code Is Like This

## Architecture Overview
- **Frontend**: Single Page Application (HTML5, CSS3 Glassmorphism, JavaScript ES6 Fetch API).
- **Backend Service**: FastAPI server running on Uvicorn (`http://127.0.0.1:8000`).
- **Orchestration**: LangChain (`PromptTemplate` | `ChatOpenAI`).
- **Graph Database**: Neo4j AuraDB.
- **Model**: OpenAI `gpt-4o-mini` with `temperature=0.0`.
