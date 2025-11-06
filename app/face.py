import os
from typing import Tuple

import cv2
import numpy as np
from fastapi import HTTPException


class FaceDetector:
    def __init__(self) -> None:
        cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        self.cascade = cv2.CascadeClassifier(cascade_path)

    def detect_largest(self, bgr: np.ndarray) -> Tuple[int, int, int, int]:
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(48, 48))
        if len(faces) == 0:
            raise HTTPException(status_code=422, detail="No se detectó rostro. Por favor sube otra imagen.")
        x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
        return int(x), int(y), int(w), int(h)

