import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.models import models  # ⬅️ Für DB-Cleanup

# 1. In-Memory-SQLite Engine
TEST_SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# 2. Neue Session Factory für Tests
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Setup: neue DB erstellen (nur einmal)
Base.metadata.create_all(bind=engine)

# 4. Override get_db für FastAPI
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 5. Client für Tests bereitstellen
@pytest.fixture
def client():
    return TestClient(app)

# 6. Cleanup Fixture – wird automatisch nach jedem Test ausgeführt
@pytest.fixture(autouse=True)
def clean_database():
    db = TestingSessionLocal()
    try:
        db.query(models.WeatherData).delete()
        db.commit()
    finally:
        db.close()
