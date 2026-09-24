"""Manejo de errores y disponibilidad de Ollama (LLM y embeddings).

Cualquier falla al hablar con Ollama (servicio caído, modelo no descargado, tiempo agotado) se
traduce a ModelUnavailableError → HTTP 503 con un mensaje claro (AGENTS.md §10.1, RF-FE-6).
"""

import logging
from collections.abc import Iterator
from contextlib import contextmanager

import httpx
import ollama
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.errors import AppError, error_response

logger = logging.getLogger(__name__)


class ModelUnavailableError(AppError):
    def __init__(self, detail: str) -> None:
        super().__init__(detail, code="model_unavailable", status_code=503)


@contextmanager
def ollama_errors(model: str) -> Iterator[None]:
    """Envuelve una llamada a Ollama y traduce sus errores a ModelUnavailableError."""
    try:
        yield
    except ollama.ResponseError as exc:
        logger.error("Ollama respondió con error para el modelo %s: %s", model, exc)
        if exc.status_code == 404:
            raise ModelUnavailableError(
                f"El modelo '{model}' no está disponible en el servidor de modelos."
            ) from exc
        raise ModelUnavailableError("El modelo local respondió con un error. Intenta de nuevo.") from exc
    except httpx.TimeoutException as exc:
        logger.error("Tiempo agotado esperando a Ollama (modelo %s)", model)
        raise ModelUnavailableError(
            "El modelo local tardó demasiado en responder. Intenta de nuevo en un momento."
        ) from exc
    except (ConnectionError, httpx.HTTPError) as exc:
        logger.error("No se pudo conectar con Ollama (modelo %s): %s", model, exc)
        raise ModelUnavailableError(
            "No se pudo conectar con el modelo local. Intenta de nuevo en un momento."
        ) from exc


def register_ollama_exception_handlers(app: FastAPI) -> None:
    """Red de seguridad: si un error de Ollama escapa sin traducir (por ejemplo, desde una librería que
    llama al cliente por su cuenta), igual llega al cliente como 503 y no como 500."""

    async def _to_503(_: Request, exc: Exception) -> JSONResponse:
        logger.error("Error de Ollama no traducido: %r", exc)
        try:
            with ollama_errors("desconocido"):
                raise exc
        except ModelUnavailableError as translated:
            return error_response(503, translated.detail, translated.code)

    for exc_type in (ollama.ResponseError, httpx.TransportError, ConnectionError):
        app.add_exception_handler(exc_type, _to_503)


def missing_models(base_url: str, models: list[str], timeout: float = 5.0) -> list[str]:
    """Devuelve cuáles de los modelos pedidos no están descargados en Ollama."""
    with ollama_errors(", ".join(models)):
        available = {m.model for m in ollama.Client(host=base_url, timeout=timeout).list().models}
    # "qwen2.5:3b" aparece tal cual; "paraphrase-multilingual" aparece como "...:latest"
    return [m for m in models if m not in available and f"{m}:latest" not in available]
