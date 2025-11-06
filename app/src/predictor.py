import io
from typing import Dict, Tuple

import numpy as np
from fastapi import HTTPException
from PIL import Image
import cv2

from .model import ModelManager
from .face import FaceDetector


FERPLUS_LABELS = [
    "neutral", "happiness", "surprise", "sadness", "anger", "disgust", "fear", "contempt"
]


class FerPredictor:
    def __init__(self, mm: ModelManager, fd: FaceDetector) -> None:
        self.mm = mm
        self.fd = fd

    @staticmethod
    def _load_image_rgb(img_bytes: bytes) -> np.ndarray:
        try:
            img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Imagen inválida: {e}")
        return np.array(img)

    def _preprocess(self, bgr: np.ndarray) -> np.ndarray:
        x, y, w, h = self.fd.detect_largest(bgr)
        face = bgr[y : y + h, x : x + w]
        if face.size == 0:
            raise HTTPException(status_code=422, detail="Recorte de rostro inválido. Reintenta con otra imagen.")
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (64, 64), interpolation=cv2.INTER_AREA)
        return resized.astype(np.float32)[None, None, :, :]

    @staticmethod
    def _map_logits(logits: np.ndarray) -> Tuple[str, float]:
        exps = np.exp(logits - np.max(logits))
        probs = exps / np.sum(exps)
        joy = float(probs[FERPLUS_LABELS.index("happiness")])
        sadness = float(probs[FERPLUS_LABELS.index("sadness")])
        anger = float(probs[FERPLUS_LABELS.index("anger")] + probs[FERPLUS_LABELS.index("disgust")])
        groups = {"joy": joy, "sadness": sadness, "anger": anger}
        emotion = max(groups, key=groups.get)
        return emotion, float(max(0.0, min(1.0, groups[emotion])))

    def predict(self, img_bytes: bytes) -> Dict[str, object]:
        if not img_bytes or len(img_bytes) < 32:
            raise HTTPException(status_code=400, detail="Imagen vacía o corrupta.")
        rgb = self._load_image_rgb(img_bytes)
        bgr = rgb[:, :, ::-1]
        inp = self._preprocess(bgr)
        sess, input_name = self.mm.get_session()
        outputs = sess.run(None, {input_name: inp})
        if not outputs:
            raise RuntimeError("Inferencia sin salida")
        logits = outputs[0].reshape(-1)
        emotion, confidence = self._map_logits(logits)
        return {
            "emotion": emotion,
            "confidence": round(float(confidence), 4),
            "model_version": "onnx-ferplus-8:cpu",
        }
