from fastapi import FastAPI
from app.api.v1.endpoints.assistant import router as assistant_router
from app.api.v1.endpoints.search import router as search_router

app = FastAPI(title="AI Email Assistant Backend")

app.include_router(assistant_router, prefix="/assistant", tags=["assistant"])
app.include_router(search_router, prefix="/search", tags=["search"])

@app.get("/")
def home():
    return {"status": "running", "service": "email-ai-backend"}
