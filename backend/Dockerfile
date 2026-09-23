FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dependencias primero, para aprovechar la caché de capas de Docker.
# Cuando se agreguen embeddings (Fase 2), PyTorch debe instalarse en versión CPU:
#   pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app ./app
COPY migrations ./migrations
COPY scripts ./scripts

RUN useradd --create-home --uid 1000 cantinero
USER cantinero

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4)"

# Aplica migraciones pendientes y arranca la API.
CMD ["sh", "-c", "python -m scripts.migrate && exec uvicorn app.main:create_app --factory --host 0.0.0.0 --port 8000"]
