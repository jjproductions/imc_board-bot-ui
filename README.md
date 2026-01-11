# IMC Board Query / Chat Service

This repository contains a FastAPI-based query/chat service scaffold implementing the architecture described in `.github/copilot-instructions.md`.

What I added
- `app/` FastAPI application
- `app/routes` endpoints: `/health`, `/search`, `/chat`
- `app/models/dto.py` Pydantic request/response models
- `app/services` stubs: `embeddings.py`, `retrieval.py`, `llm.py`, `rag.py`
- `app/core/config.py` environment-driven settings
- `requirements.txt`, `.env.example`

Run locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the app (development):

```bash
uvicorn app.main:app --reload --port 8002
```

Open `http://localhost:8002/health` to verify the service is up.

API endpoints
- `GET /health` — basic health check
- `POST /search` — body: `SearchRequest` → returns `SearchResponse`
- `POST /chat` — body: `ChatRequest` → returns `ChatResponse`

Architecture (high level)

```
Frontend → FastAPI (/chat, /search)
  - routes/chat.py -> orchestrates RAG
  - services/embeddings.py -> embedding generator (placeholder)
  - services/retrieval.py -> Qdrant retrieval stub
  - services/llm.py -> LLM provider stub (replace with Ollama/OpenAI)
  - services/rag.py -> builds context + calls LLM
Qdrant (external) - collection: board-policies
```

Next steps you might want:
- Wire real Qdrant calls into `app/services/retrieval.py`
- Integrate Ollama or another LLM provider into `app/services/llm.py`
- Add unit tests and a `docker-compose` for local Qdrant
# imc_board-bot-ui
Chat Bot UI
