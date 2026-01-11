from fastapi import APIRouter

router = APIRouter()

from .chat import router as chat_router

router.include_router(chat_router, prefix="")
