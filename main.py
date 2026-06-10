from fastapi import FastAPI

app = FastAPI(
    title="Enterprise AI Security Gateway"
)

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Enterprise AI Security Gateway"
    }