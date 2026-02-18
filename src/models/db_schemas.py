from pydantic import BaseModel
from typing import Dict, Any, Optional

class DocumentMetadata(BaseModel):
    """
    Metadata stored with the vector in ChromaDB.
    """
    source: str
    page: Optional[int] = None
    # Add other metadata fields as needed
    
class ChromaDocument(BaseModel):
    """
    Represents a document stored in ChromaDB.
    """
    id: str
    content: str
    metadata: DocumentMetadata
