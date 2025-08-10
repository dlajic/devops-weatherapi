from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes  # router handler
import uvicorn
import os

app = FastAPI(
    title="DevOps Demo API",
    description="Example Service with FastAPT & SQLite",
    version="1.0.0",
)

allowed = [f"https://{os.getenv('DOMAIN','devops-weatherapi.dev')}"]
# optional also www:
allowed.append(f"https://www.{os.getenv('DOMAIN','devops-weatherapi.dev')}")

# for CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,
    allow_methods=["GET", "OPTIONS"],  # for Portfolio: read-only enough
    allow_headers=["*"],
)

# add routes
app.include_router(routes.router)


# Optional: Root-Route
@app.get("/")
def read_root():
    return {"message": "FastAPI running"}


# Local start (if directly python main.py)
if __name__ == "__main__":
    uvicorn.run("main_app", host="0.0.0.0", port=8000, reload=True)

# for fastapi docs: http://127.0.0.1:8000/docs
