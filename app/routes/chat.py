from fastapi import APIRouter
from app.models.dto import SearchRequest, SearchResponse, ChatRequest, ChatResponse
from app.services import rag

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "query/chat", "ready": True}


@router.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    hits = rag.search(req.query, top_k=req.top_k, collection=req.collection)
    return SearchResponse(hits=hits)


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    answer, citations = rag.answer_chat(req)
    return ChatResponse(answer=answer, citations=citations)
