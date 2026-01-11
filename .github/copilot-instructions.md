# Copilot Project Instructions & Preferences

> Owner: Jonathan Bagby  
> Context: Docling → FastAPI → Qdrant RAG stack

This document captures architectural and coding preferences for building and operating a retrieval pipeline using **FastAPI**, **Docling**-parsed documents, **Qdrant**, and **BAAI/bge-m3** embeddings. It is intended for consistent implementation across services, PRs, and automation.

---

## 1) Core Philosophy

- **Separate concerns**: **query/chat**. Scale, secure, and deploy them independently.
- **Clear contracts**: Use Pydantic models per service; keep schemas versionable and documented.
- **Reliability first**: The query/chat service must remain online even if ingestion evolves or fails.
- **Observability & security**: monitor latencies and errors for search/chat.

---

## 2) Tech Stack Defaults

- **Language**: Python 3.11+
- **Framework**: FastAPI + Uvicorn
- **Vector DB**: Qdrant (HTTP API)
- **Embeddings**: `BAAI/bge-m3` (1024-dim), normalized embeddings, cosine similarity
- **Tokenization (chunking)**: `transformers` tokenizer for `bge-m3`
- **Runtime packaging**: Docker per service; optional `docker-compose` to wire Qdrant + services
- **LLM**: Default to Ollama chat, model: llama3.1:8b-instruct-q4_K_M

---

## 3) High-Level Architecture

```


Frontend → sends requests to FastAPI.
FastAPI (app/main.py, routes/chat.py)
  Receives ChatRequest and returns ChatResponse.
  Calls the RAG pipeline.
RAG Query Service (services/)
  Embeddings (embeddings.py): BAAI/bge-m3 normalized vectors.
  Retrieval (retrieval.py): queries Qdrant board-policies, returns RetrievedChunk.
  RAG Composer (rag.py): builds context, aggregates sources, calls LLM.
  LLM (llm.py): Ollama llama3.1:8b-instruct-q4_K_M.
Qdrant: Collection board-policies with payload key text

```

---

## 4) Repository Structure

```
.env
requirements.txt
README.md
app/
  __init__.py
  main.py
  models/
    __init__.py
    dto.py
  routes/
    __init__.py
    chat.py
  services/
    __init__.py
    embeddings.py (BAAI/bge-m3 + normalization)
    retrieval.py (Qdrant search, unnamed vectors)
    llm.py (Ollama chat, model: llama3.1:8b-instruct-q4_K_M)
    rag.py (build context + answer composition)
```

---

## 5) API Contracts

### Query/Chat Service

- `GET /health` → basic health & model info
- `POST /search` → body: `SearchRequest`; returns `SearchResponse`
- `POST /chat` → body: `ChatRequest`; returns `{answer, citations}` (LLM-free scaffold)

**SearchRequest / Response (summary)**

- `query: str`, `top_k: int = 5`, `collection?: str`, `filter_by_source_id?: str`
- `hits: List[{score: float, text: str, payload: Dict}]`

**ChatRequest (summary)**

- `messages: [{role: "user"|"assistant"|"system", content: str}]`
- `top_k: int = 5`, `collection?: str`, `source_filter?: str`

---

## 6) Embedding & Qdrant Configuration

**Embedding model defaults**

- Model: `BAAI/bge-m3` (multilingual)
- Dimension: `1024`
- Normalization: **on** (`normalize_embeddings=True`)
- Distance: **cosine** in Qdrant

**Environment variables**

```bash
# common
export QDRANT_URL=http://localhost:6333
export QDRANT_API_KEY=        # optional for local
export QDRANT_COLLECTION=board-policies

# embeddings (defaults)
export EMBEDDING_MODEL=BAAI/bge-m3
export EMBEDDING_DIM=1024
```

**Collection creation**

- If switching models/dim, **recreate** collection with matching `VectorParams(size=EMBEDDING_DIM, distance=cosine)`.

---

## 7) Chunking Strategy (Docling → Text Chunks)

- **Heading-aware context**: Maintain a stack of headings (`H1..H6`) and assign a `section_path` like `H1 > H2 > ...` to each chunk.
- **Token-aware windowing**: Use the model tokenizer; default `max_tokens=300` with `overlap_tokens=50` between windows.
- **Tables**: Convert tables (`meta.rows`) to **Markdown** if possible; otherwise, fall back to `text`.
- **Page boundaries**: Flush buffers on `page_break` to reduce cross-page context mixing.
- **Payload**: Store `source_id`, `title`, `pages`, `section_path`, `block_ids`, `tokens`, `overlap_from_previous`, `embedding_model`.

---

## 8) Deployment & Local Dev

```

```

**Local run**

```bash
# Terminal A
cd ingestion && uvicorn main:app --reload --port 8001

# Terminal B
cd query && uvicorn main:app --reload --port 8002
```

---

## 9) Security, Observability, and Ops

- **Auth**: Make ingestion private. Add API key / OAuth dependencies to `Routes/ingestion.py`.
- **Rate limiting**: Apply to query endpoints as needed.
- **Logging**: Log query latency, `top_k`, and document IDs on search/chat.
- **Metrics**: Export Prometheus counters/histograms for ingestion duration and query latency.

---

## 10) Optional Enhancements

- **Score threshold**: enable score_threshold (e.g., 0.3) in Qdrant search to filter weak matches.
- **Streaming**: switch to ollama.chat(..., stream=True) and add SSE/websocket route.
- **Observability**: log top scores/chunk IDs; add /debug/retrieval route for traceability.
- **Caching**: memoize embeddings for frequent questions (in-memory or Redis).
- **Auth & rate limiting**: add API key or JWT, per-user quotas

---

## 11) Quick Reference Commands

```bash

# Search
curl -X POST http://localhost:8002/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"What is the dress code?"}'
```

---

## 12) Style & Code Organization

- Endpoints live under `Routes/` per service.
- Pydantic models live under `models/` per service.
- Configuration and dependency singletons live under `core/` (`config.py`, `deps.py`).
- Avoid cross-service imports unless moved to a shared `common/` package.
- Keep code blocks in Markdown fenced sections; avoid code in tables.

---

**This document is the source of truth for service layout and runtime defaults.**  
If preferences change (e.g., embedding model, llm, or router structure), update this file and reference the change in PR descriptions.
