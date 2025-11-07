# MoodTune FER Service (ONNX)

Servicio de reconocimiento de emociones faciales (FER) para CU‑01.

Implementa un endpoint HTTP que recibe una imagen (`multipart/form-data`) y devuelve
una emoción en el dominio del API de MoodTune: `joy | sadness | anger`, con una
confianza (0–1) y `model_version`.

## Arquitectura

- Modelo: ONNX Emotion FER+ (8 clases originales)
  - Fuente: onnx/models (Emotion FERPlus)
  - Clases originales: [neutral, happiness, surprise, sadness, anger, disgust, fear, contempt]
  - Mapeo a MoodTune: joy ← happiness; sadness ← sadness; anger ← anger|disgust (agrupado)
- Detección de rostro: OpenCV Haar Cascade (mayor rostro). Si no hay rostro → 422.
- Framework: FastAPI + Uvicorn

## Endpoints- GET /infer (informativo): devuelve detalles de uso del endpoint
- GET /health: verifica disponibilidad del servicio

## Ejecutar local

Opciones:

1) Python directo

```bash
cd moodtune_fer
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
# Ejecutar con run.py (similar a moodtune_api)
python run.py
```

2) Docker

```bash
cd moodtune_fer
cp .env.example .env
# Opcional: cambia FER_PUBLIC_PORT en .env si 8081 está ocupado
docker compose up --build
```

## Configurar frontend

En `moodtune_frontend/.env` agrega:

```
VITE_FER_ENDPOINT_URL=http://localhost:8081/infer
```

La pantalla `/detect` usará este endpoint con `POST multipart/form-data`.
