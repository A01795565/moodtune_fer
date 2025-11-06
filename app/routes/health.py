from fastapi.responses import JSONResponse
from fastapi import FastAPI

from ..src.model import ModelManager


def register_health(app: FastAPI, mm: ModelManager) -> None:
    @app.get("/health")
    async def health():
        try:
            mm.ensure_model()
            return {"status": "ok"}
        except Exception as e:
            return JSONResponse({"status": "error", "error": str(e)}, status_code=500)

