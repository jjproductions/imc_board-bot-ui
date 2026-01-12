from fastapi import FastAPI
from .routes.chat import router as chat_router
from .core.config import settings

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
app.include_router(chat_router, prefix="/api", tags=["chat"])



@app.get("/")
def root():
    return {"service": settings.APP_NAME, "status": "ok"}
