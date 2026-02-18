from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from src.config import get_settings

settings = get_settings()

def retrieve_context(query: str, collection_name: str = "default", k: int = 3) -> List[str]:
    """
    Retrieves the top k most relevant document chunks for the given query.
    """
    # Initialize embeddings (must match ingestion)
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Initialize Vector Store
    vector_store = Chroma(
        persist_directory=settings.CHROMA_DB_DIR,
        embedding_function=embeddings,
        collection_name=settings.COLLECTION_NAME
    )
    
    # Perform similarity search
    results = vector_store.similarity_search(query, k=k)
    
    # Extract page content
    context = [doc.page_content for doc in results]
    
    return context
