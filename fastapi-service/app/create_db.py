# app/create_db.py
from app.db.database import engine, Base
import app.models 

Base.metadata.create_all(bind=engine)
