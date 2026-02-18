from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    """
    Verifies that the health check endpoint returns 200 OK and expected status.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "app": "Local RAG API"}
