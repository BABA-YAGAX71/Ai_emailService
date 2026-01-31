from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Lazy initialization
vector = None

def _init_vector():
    global vector
    if vector is None:
        from app.services.vector_service import VectorService
        vector = VectorService()

class SearchRequest(BaseModel):
    query: str
    k: int = 5

@router.post("")
def semantic_search(req: SearchRequest):
    _init_vector()
    results = vector.search(req.query, req.k)
    return {"results": results}
