import os
from dataclasses import dataclass


@dataclass(frozen=True)
class FerConfig:
    onnx_url: str = os.environ.get(
        "FER_ONNX_URL",
        "https://media.githubusercontent.com/media/onnx/models/main/validated/vision/body_analysis/emotion_ferplus/model/emotion-ferplus-8.onnx",
    )
    onnx_path: str = os.environ.get("FER_ONNX_PATH", os.path.join(os.path.dirname(__file__), "emotion-ferplus-8.onnx"))
    cors_origins: str = os.environ.get("FER_CORS_ORIGINS", "*")
