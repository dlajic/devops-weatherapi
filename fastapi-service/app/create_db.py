from app.db.database import engine, Base
import app.models  # noqa: F401  # wichtig: import triggert Model-Registrierung

Base.metadata.create_all(bind=engine)
