import pytest
from unittest.mock import AsyncMock, patch
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.asyncio
@patch("app.api.routes.httpx.AsyncClient")
async def test_fetch_and_store_weather(mock_async_client_class, client):
    # 1. Dummy-Daten für Response
    dummy_data = {
        "main": {"temp": 18.5, "humidity": 65}
    }

    # 2. AsyncMock für .get
    mock_get = AsyncMock()
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = AsyncMock(return_value=dummy_data)

    # 3. mock_async_client_class() gibt ein Objekt mit .get() zurück
    mock_async_client_class.return_value.__aenter__.return_value.get = mock_get

    # 4. Testaufruf
    response = client.post("/weather/live/Berlin")
    assert response.status_code == 200
    result = response.json()

    # 5. Inhalt prüfen
    assert result["city"] == "Berlin"
    assert result["temperature"] == 18.5
