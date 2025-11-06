FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la app completa (incluye paquete app/, app.py y run.py)
COPY . .

EXPOSE 8081
# Ejecuta como en moodtune_api mediante run.py
CMD ["python", "run.py"]
