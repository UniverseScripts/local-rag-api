import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_settings
from src.models.api_schemas import IngestResponse, ChatRequest, ChatResponse
from src.core.ingestion import ingest_file
from src.core.retrieval import retrieve_context
from src.core.generation import generate_answer

settings = get_settings()

app = FastAPI(
    title="Local RAG API",
    version="1.0.0",
    description="A privacy-first RAG backend using Ollama and ChromaDB."
)

# CORS Configuration
# In production, specify exact origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "app": "Local RAG API"}

@app.post("/api/v1/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)):
    """
    Ingests a document (PDF or TXT) into the vector database.
    """
    return ingest_file(file)

@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Chat with the ingested documents.
    """
    start_time = time.time()
    
    # 1. Retrieve Context
    context = retrieve_context(request.query, request.collection_name)
    
    # 2. Generate Answer
    result = generate_answer(request.query, context, request.use_local)
    
    inference_time = time.time() - start_time
    
    return ChatResponse(
        answer=result["answer"],
        sources=context,
        inference_time=inference_time
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=(settings.ENVIRONMENT == "development"))
