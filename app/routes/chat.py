from fastapi import APIRouter
from ..models.dto import ChatRequest, ChatResponse, SearchRequest, SearchResponse
from ..services import rag

router = APIRouter()
@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # call the rag service function (module `rag` is not callable)
    return rag.rag(req)


@router.get("/health")
def health():
    return {"status": "ok", "service": "query/chat", "ready": True}


# ---------------------------
@router.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    hits = rag.search(req.query, top_k=req.top_k, collection=req.collection)
    return SearchResponse(hits=hits)
