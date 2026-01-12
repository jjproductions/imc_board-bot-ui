
import os
from typing import Dict, Any, List, Tuple
from .retrieval import retrieve, search_collection
from .llm import answer as llm_answer
from ..models.dto import ChatRequest, ChatResponse, SearchRequest, SearchResponse
from ..core.config import settings
import logging


MAX_CONTEXT_CHARS = settings.MAX_CONTEXT_CHARS

def _build_context(chunks: List[SearchResponse], max_chars: int = MAX_CONTEXT_CHARS) -> Tuple[str, List[Dict[str, Any]]]:
    ctx_parts: List[str] = []
    sources: List[Dict[str, Any]] = []
    count = 0
    for ch in chunks:
        logging.getLogger("rag").debug(f"chunk={ch!r}")
        text = ch.text if getattr(ch, "text", None) is not None else ""
        piece = str(text).strip()
        if not piece:
            continue
        remaining = max_chars - count
        if len(piece) > remaining:
            piece = piece[: max(0, remaining)]
        ctx_parts.append(piece)
        count += len(piece)

        payload = ch.payload if getattr(ch, "payload", None) is not None else {}
        if not isinstance(payload, dict):
            payload = {}

        src: Dict[str, Any] = {}
        if getattr(ch, "score", None) is not None:
            src["score"] = ch.score

        title = payload.get("title") if payload.get("title") is not None else payload.get("section_title")
        if title is not None:
            src["title"] = title

        for key in ("section_id", "doc_id", "page"):
            val = payload.get(key)
            if val is not None:
                src[key] = val

        sources.append(src)

        if count >= max_chars:
            break

    return "\n\n".join(ctx_parts), sources

def rag(cRequest: ChatRequest) -> ChatResponse:
    retRequest: SearchRequest = SearchRequest(
        query=cRequest.question,
        top_k=cRequest.top_k,
    )
    chunks = retrieve(retRequest)
    context, _ = _build_context(chunks)

    if not context.strip():
        return ChatResponse(answer=settings.BOARD_POLICIES_IDK_RESPONSE, citations=[])

    ans = llm_answer(cRequest.question, context)

    def _extract_text(resp):
        if resp is None:
            return ""
        if isinstance(resp, str):
            return resp
        msg = getattr(resp, "message", None) or getattr(resp, "text", None) or getattr(resp, "content", None)
        if isinstance(msg, str):
            return msg
        if hasattr(msg, "content"):
            return getattr(msg, "content")
        if isinstance(resp, (list, tuple)) and len(resp) > 0:
            first = resp[0]
            if isinstance(first, str):
                return first
            if hasattr(first, "content"):
                return getattr(first, "content")
        return str(resp)

    answer_text = _extract_text(ans)

    citations = []
    for ch in chunks:
        text = getattr(ch, "text", "") or ""
        payload = getattr(ch, "payload", {}) or {}
        score = float(getattr(ch, "score", 0.0) or 0.0)
        citations.append({"score": score, "text": text, "payload": payload})

    return ChatResponse(answer=answer_text, citations=citations)





# ------------------
def search(query: str, top_k: int = 5, collection: str | None = None):
    return search_collection(query, top_k=top_k, collection=collection)


def answer_chat(req) -> Tuple[str, List[dict]]:
    # Build a simple context from retrieval of the last user message
    last_user = None
    for m in reversed(req.messages):
        if m.role == "user":
            last_user = m.content
            break

    context = None
    citations = []
    if last_user:
        hits = search_collection(last_user, top_k=req.top_k, collection=req.collection)
        citations = hits
        # join top texts as context
        context = "\n---\n".join(h["text"] for h in hits)

    # Call LLM stub
    answer = llm_answer([m.dict() for m in req.messages], context=context)
    return answer, citations
