from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes  # router handler
import uvicorn

app = FastAPI(
    title="DevOps Demo API",
    description="Example Service with FastAPT & SQLite",
    version="1.0.0",
)

# for CORS (Cross-Origin Resource Sharing), tell him access is ok from every point
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
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
