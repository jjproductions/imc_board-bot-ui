from fastapi import FastAPI
from app.routes import router as routes
from app.core.config import settings

app = FastAPI(title="IMC Board Policy Chat")
app.include_router(routes)


@app.get("/")
def root():
    return {"service": "imc-board-query", "status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
