from app.models.dto import Message
from app.services import retrieval, llm
from typing import List, Tuple


def search(query: str, top_k: int = 5, collection: str | None = None):
    return retrieval.search_collection(query, top_k=top_k, collection=collection)


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
        hits = retrieval.search_collection(last_user, top_k=req.top_k, collection=req.collection)
        citations = hits
        # join top texts as context
        context = "\n---\n".join(h["text"] for h in hits)

    # Call LLM stub
    answer = llm.generate_answer([m.dict() for m in req.messages], context=context)
    return answer, citations
