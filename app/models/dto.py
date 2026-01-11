from pydantic import BaseModel
from typing import List, Dict, Optional


class Message(BaseModel):
    role: str
    content: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    collection: Optional[str] = None


class Hit(BaseModel):
    score: float
    text: str
    payload: Dict


class SearchResponse(BaseModel):
    hits: List[Hit]


class ChatRequest(BaseModel):
    messages: List[Message]
    top_k: int = 5
    collection: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    citations: List[Hit] = []
