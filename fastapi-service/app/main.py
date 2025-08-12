from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes  # router handler
import uvicorn
import os

app = FastAPI(
    title="DevOps Demo API",
    description="Example Service with FastAPI & Postgres",
    version="1.2.0",
)

# Prüfen, ob wir im DEV- oder PROD-Modus laufen
env = os.getenv("ENV", "prod")

if env == "dev":
    # Lokale Entwicklung → localhost erlauben
    allowed = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost",
        "http://127.0.0.1",
    ]
else:
    # Produktion → nur Domain erlauben
    allowed = [
        f"https://{os.getenv('DOMAIN','devops-weatherapi.dev')}",
        f"https://www.{os.getenv('DOMAIN','devops-weatherapi.dev')}",
    ]

# Middleware für CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# API-Routen einbinden
app.include_router(routes.router)

# Root-Route
@app.get("/")
def read_root():
    return {"message": "FastAPI running"}

# Start für lokalen Modus
if __name__ == "__main__":
    uvicorn.run("main", host="0.0.0.0", port=8000, reload=True)
