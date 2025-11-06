from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .src.config import FerConfig
from .src.model import ModelManager
from .src.face import FaceDetector
from .src.predictor import FerPredictor
from .routes.health import register_health
from .routes.infer import register_infer


def create_app() -> FastAPI:
    cfg = FerConfig()
    mm = ModelManager(cfg)
    fd = FaceDetector()
    predictor = FerPredictor(mm, fd)

    app = FastAPI(title="MoodTune FER Service", version="1.2.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in cfg.cors_origins.split(",") if o.strip()] or ["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_health(app, mm)
    register_infer(app, predictor)

    return app
