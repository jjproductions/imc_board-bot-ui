
from typing import Dict, List
from qdrant_client import QdrantClient
from .embeddings import embed, embed_text
from ..core.config import settings
from ..models.dto import SearchRequest, Hit

_client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY or None)


def retrieve(sRequest: SearchRequest) -> List[Hit]:
    """Perform a vector search in Qdrant and return simple Hit objects.

    Note: `QdrantClient.retrieve()` is for fetching by ids; use `search()` for vector
    similarity queries.
    """
    top_k = sRequest.top_k or settings.TOP_K_DEFAULT
    qvec = embed(sRequest.query)
    res = _client.query_points(
        collection_name=settings.QDRANT_COLLECTION,
        query=qvec,
        limit=top_k,
        with_payload=True,
        # score_threshold=0.3,
    )

    out: List[Hit] = []
    for p in res:
        payload = getattr(p, "payload", {}) or {}
        if not isinstance(payload, dict):
            payload = {}
        text = payload.get(settings.TEXT_PAYLOAD_KEY, "")
        if not isinstance(text, str):
            text = str(text)
        score = getattr(p, "score", None)
        score = float(score) if score is not None else 0.0
        out.append(Hit(text=text, score=score, payload=payload))
    return out




def search_collection(query: str, top_k: int = 5, collection: str | None = None) -> List[Dict]:
    """Placeholder retrieval that returns synthetic hits for demonstration.

    In a real implementation this would query Qdrant with the query embedding.
    """
    collection = collection or settings.QDRANT_COLLECTION
    qvec = embed_text(query)
    hits = []
    for i in range(min(top_k, 10)):
        hits.append({
            "score": 1.0 - (i * 0.1),
            "text": f"Fake retrieved snippet for '{query}' (hit {i+1})",
            "payload": {"source_id": f"doc-{i+1}", "collection": collection},
        })
    return hits
