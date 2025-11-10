# MoodTune FER Service (ONNX)

Servicio de reconocimiento de emociones faciales (FER) basado en ONNX Emotion FER+ con FastAPI + Uvicorn.

Devuelve una emoción en el dominio de MoodTune (`joy | sadness | anger`) con confianza (`0..1`) y `model_version`.

Arquitectura
- Modelo: ONNX Emotion FER+ (8 clases originales)
  - Clases originales: neutral, happiness, surprise, sadness, anger, disgust, fear, contempt
  - Mapeo a MoodTune: joy ← happiness; sadness ← sadness; anger ← anger|disgust (agrupado)
- Detección de rostro: OpenCV Haar Cascade (selecciona el rostro más grande). Si no hay rostro → 422.
- Framework: FastAPI + Uvicorn con CORS configurable.

Endpoints
- `POST /infer` Recibe imagen (`multipart/form-data`, campo `image`) y devuelve emoción.
- `GET /infer` Información de uso del endpoint (útil en navegador/health checks).
- `GET /health` Estado del servicio y del modelo.

Ejecutar en local (venv)
```
cd moodtune_fer
python -m venv .venv
# Linux/Mac: source .venv/bin/activate
# Windows:   .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Docker
```
cd moodtune_fer
cp .env.example .env
# Opcional: cambia FER_PUBLIC_PORT en .env si 8081 está ocupado
docker compose up --build
```
- Servicio: `http://localhost:8081`

Frontend
- En `moodtune_frontend/.env` añade:
```
VITE_FER_ENDPOINT_URL=http://localhost:8081/infer
```
La pantalla `/detect` usará este endpoint con `POST multipart/form-data`.

