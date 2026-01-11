from typing import List, Dict
from app.services.embeddings import embed_text
from app.core.config import settings


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
