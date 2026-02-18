# Local RAG API (Open Source Edition)

A strictly local, privacy-first RAG (Retrieval Augmented Generation) backend.
It allows you to ingest PDF/TXT documents and chat with them using **Ollama** and **ChromaDB**.

**Status:** core-logic

## Features
* **FastAPI:** Async endpoints for `/ingest` and `/chat`.
* **ChromaDB:** Local vector storage.
* **Ollama:** Uses local LLMs (Llama 3, Mistral, etc).
* **Privacy:** No data leaves your machine.

## Prerequisites (Manual Setup)
Since this is the source version, you must manage the infrastructure yourself:
1.  **Install Ollama:** [Download here](https://ollama.com) and run `ollama serve`.
2.  **Install ChromaDB:** You must run a local Chroma instance or install the python client.
3.  **Python 3.10+:** Ensure your venv is active.

## Quick Start (Source)

```bash
# 1. Install Dependencies
pip install -r requirements.txt

# 2. Pull the Embedding Model (Manual)
ollama pull llama3
ollama pull nomic-embed-text

# 3. Run the API
uvicorn src.main:app --reload
```

## 🚀 Want the "One-Click" Docker Version?
I maintain a Production-Ready Starter Kit that includes:

✅ Full Docker Compose (Orchestrates API + Chroma + Ollama).

✅ Production Dockerfile (Optimized, lightweight).

✅ Environment Configs (Pre-set for Llama 3).

✅ One-Command Run (docker-compose up).

[👉 Get the Dockerized Starter Kit on Gumroad ($27)](https://galacticgamer62.gumroad.com/l/local-rag-api)
