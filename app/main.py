from fastapi import FastAPI
from app.routes.gitlab import router as gitlab_router

app = FastAPI(
    title="GitLab Webhook API",
    description="API para receber eventos do GitLab",
    version="0.1.0"
)

app.include_router(gitlab_router)

@app.get("/")
def health_check():
    return {"status": "ok"}
