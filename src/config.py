from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings.
    These values are read from environment variables, creating a "12-factor" app.
    """
    # API Configuration
    API_PORT: int = 8000
    API_HOST: str = "0.0.0.0"
    ENVIRONMENT: str = "development"

    # LLM Configuration
    LLM_MODEL_NAME: str = "llama3"
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # Vector DB Configuration
    CHROMA_DB_DIR: str = "chroma_db"
    COLLECTION_NAME: str = "rag_collection"

    # Fallback (Optional)
    OPENAI_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache()
def get_settings():
    """
    Creates a singleton instance of the settings.
    """
    return Settings()
