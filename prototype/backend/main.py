from dotenv import load_dotenv

# MUST be executed before importing rag_pipeline to load .env variables into os.environ
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from rag_pipeline import rag_pipeline


app = FastAPI(
    title="Why The Code Is Like This - AI Evidence Service",
    description="Backend API servicing natural language 'Why' queries over repository context.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionPayload(BaseModel):
    question: str = Field(..., example="Why was Neo4j chosen over PostgreSQL for indexing repository entities?")

class AnswerResponse(BaseModel):
    question: str
    answer: str
    evidence_found: bool
    sources: list

@app.get("/")
def health_check():
    return {"status": "ok", "service": "RAG AI Evidence Engine"}

@app.post("/api/ask", response_model=AnswerResponse)
def ask_why_question(payload: QuestionPayload):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question prompt cannot be empty.")
    
    try:
        result = rag_pipeline.answer_question(payload.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Execute server locally using: uvicorn main:app --reload
