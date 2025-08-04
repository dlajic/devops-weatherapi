from fastapi.testclient import TestClient
from app.main import app


def test_healthcheck():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
