from fastapi import FastAPI
from app.routes.gateway import router
from app.routes.dashboard import router as dashboard_router
from app.services.database import init_db

app = FastAPI(title="Enterprise AI Security Gateway")

@app.on_event("startup")
def startup():
    init_db()

app.include_router(router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Enterprise AI Security Gateway"
    }