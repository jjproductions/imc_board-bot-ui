from sentence_transformers import SentenceTransformer
from ..core.config import settings
import hashlib
import math

# BAAI/bge-m3 with normalization
_model = SentenceTransformer(settings.EMBEDDING_MODEL)

def embed(text: str) -> list[float]:
    return _model.encode(text, normalize_embeddings=True).tolist()



def _hash_to_float(data: bytes) -> float:
    h = hashlib.blake2b(data, digest_size=8).digest()
    return int.from_bytes(h, "big") / ((1 << 64) - 1)




# ------------------
def embed_text(text: str) -> list[float]:
    """Deterministic placeholder embedding generator.

    Produces `settings.EMBEDDING_DIM` floats in [0,1) and normalizes them.
    """
    dim = settings.EMBEDDING_DIM
    vec = []
    salt = 0
    while len(vec) < dim:
        chunk = f"{salt}:{text}".encode("utf-8")
        # produce 8 bytes -> one float; repeat to reach dim
        val = _hash_to_float(chunk)
        vec.append(val)
        salt += 1

    # normalize
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]
