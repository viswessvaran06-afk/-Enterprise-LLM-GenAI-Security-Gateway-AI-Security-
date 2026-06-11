from fastapi import FastAPI
from app.routes.gateway import router

app = FastAPI(title="Enterprise AI Security Gateway")

app.include_router(router, prefix="/api/v1")

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Enterprise AI Security Gateway"
    }