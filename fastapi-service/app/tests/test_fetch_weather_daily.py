import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from app.fetch_weather_daily import main
from app.db.database import SessionLocal
from app.models import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.database import Base

TEST_SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.mark.asyncio
@patch("app.fetch_weather_daily.httpx.AsyncClient")
async def test_main_fetches_multiple_cities(mock_async_client_class):
    # Dummy-Wetterdaten
    dummy_data = {
        "main": {"temp": 22.0, "humidity": 55}
    }

    # Mock-Setup
    mock_get = AsyncMock()
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = AsyncMock(return_value=dummy_data)
    mock_async_client_class.return_value.__aenter__.return_value.get = mock_get

    # DB vorbereiten (zählt Einträge vorher)
    db = TestingSessionLocal()
    db.query(models.WeatherData).delete()
    db.commit()

    # Test: main() ausführen
    await main(db=db)

    # DB prüfen: Einträge für ALLE Städte vorhanden
    entries = db.query(models.WeatherData).all()
    assert len(entries) == 16  # so viele Städte sind im STÄDTE-Array

    db.close()
