import os
import shutil
from typing import List
from fastapi import UploadFile, HTTPException
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import get_settings

settings = get_settings()

def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        return destination
    finally:
        upload_file.file.close()

def ingest_file(file: UploadFile) -> dict:
    """
    Ingests a file (PDF or TXT), chunks it, and stores it in the vector database.
    """
    # 1. Save temp file
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)
    save_upload_file(file, file_path)
    
    try:
        # 2. Load file
        if file.filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file.filename.endswith(".txt"):
            loader = TextLoader(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF and TXT are supported.")
        
        documents = loader.load()
        
        # 3. Split text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)
        
        if not chunks:
            return {"filename": file.filename, "chunks_processed": 0, "status": "no content found"}

        # 4. Embed and Store
        # Using SentenceTransformer for reliable local embeddings
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Persist directory
        persist_directory = settings.CHROMA_DB_DIR
        
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=settings.COLLECTION_NAME,
            persist_directory=persist_directory
        )
        vector_store.persist()
        
        return {
            "filename": file.filename,
            "chunks_processed": len(chunks),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
