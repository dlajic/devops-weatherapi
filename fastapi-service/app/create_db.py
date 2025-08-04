# app/create_db.py
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)
