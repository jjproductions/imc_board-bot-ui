from fastapi import FastAPI
from .routes.chat import router as chat_router
from .core.config import settings
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
app.include_router(chat_router, prefix="/api", tags=["chat"])

logging.getLogger("app").info(f"Loading ENV from: {settings.model_config.get('env_file')}")
logging.getLogger("app").info(f"LLM Model: {settings.LLM_MODEL}")

@app.get("/")
def root():
    return {"service": settings.APP_NAME, "status": "ok"}
