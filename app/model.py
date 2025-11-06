import os
import threading
from typing import Tuple

import onnxruntime as ort
import requests

from .config import FerConfig


class ModelManager:
    def __init__(self, cfg: FerConfig) -> None:
        self.cfg = cfg
        self._lock = threading.Lock()
        self._session = None
        self._input_name = None

    def ensure_model(self) -> None:
        path = self.cfg.onnx_path
        if os.path.exists(path) and os.path.getsize(path) > 1024 * 1024:
            return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        r = requests.get(self.cfg.onnx_url, timeout=60)
        if r.status_code != 200:
            raise RuntimeError(f"No se pudo descargar el modelo: {r.status_code}")
        with open(path, "wb") as f:
            f.write(r.content)

    def get_session(self) -> Tuple[ort.InferenceSession, str]:
        with self._lock:
            if self._session is None:
                self.ensure_model()
                sess = ort.InferenceSession(self.cfg.onnx_path, providers=["CPUExecutionProvider"])  # CPU only
                inputs = sess.get_inputs()
                if not inputs:
                    raise RuntimeError("Modelo ONNX inválido: sin inputs")
                self._session = sess
                self._input_name = inputs[0].name
            return self._session, self._input_name  # type: ignore

