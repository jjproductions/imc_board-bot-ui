from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ..core.config import settings

class Hit(BaseModel):
    score: float
    text: str
    payload: Dict

class ChatRequest(BaseModel):
    question: str
    top_k: int | None = settings.TOP_K_DEFAULT

class ChatResponse(BaseModel):
    answer: str
    citations: List[Hit] = []






class Message(BaseModel):
    role: str
    content: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    collection: Optional[str] = None

class SearchResponse(BaseModel):
    hits: List[Hit]



