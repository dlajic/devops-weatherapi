from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database
from app.config import DATABASE_URL

Base = declarative_base()

# Verbindung über databases (asynchron, ideal für FastAPI)
database = Database(DATABASE_URL)

# Metadata-Objekt für spätere Modelle (Tabellen)
metadata = MetaData()

# Optional: Engine, falls man später mit sqlalchemy.sync arbeiten möchte
engine = create_engine(DATABASE_URL)

# SessionLocal für synchrones SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency für FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
