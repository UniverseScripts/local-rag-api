from pydantic import BaseModel, Field
from typing import List, Optional

class IngestResponse(BaseModel):
    """
    Response model for document ingestion.
    """
    filename: str
    chunks_processed: int
    status: str = "success"

class ChatRequest(BaseModel):
    """
    Request model for the chat endpoint.
    """
    query: str = Field(..., description="The user's question.")
    collection_name: str = Field("default", description="The vector collection to query.")
    use_local: bool = Field(True, description="Whether to use the local LLM or fallback.")

class ChatResponse(BaseModel):
    """
    Response model for the chat endpoint.
    """
    answer: str
    sources: List[str]
    inference_time: float
