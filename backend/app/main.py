"""Punto de entrada de la API de Cantinero.

Ejecutar con:  uvicorn app.main:create_app --factory --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import health
from app.core.config import Settings, get_settings
from app.core.errors import UnhandledErrorMiddleware, register_exception_handlers
from app.core.logging import configure_logging
from app.core.ollama import register_ollama_exception_handlers

API_PREFIX = "/api/v1"


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    # En producción no se publica la documentación interactiva (AGENTS.md §10.1).
    docs_enabled = not settings.is_production
    app = FastAPI(
        title="Cantinero API",
        description="API del agente de coctelería y destilados (LangGraph + RAG).",
        version="0.1.0",
        docs_url="/docs" if docs_enabled else None,
        redoc_url=None,
        openapi_url="/openapi.json" if docs_enabled else None,
    )

    # Orden: el último middleware agregado es el más externo. UnhandledErrorMiddleware queda por
    # dentro de CORS para que los 500 también lleven cabeceras CORS.
    app.add_middleware(UnhandledErrorMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
    register_exception_handlers(app)
    register_ollama_exception_handlers(app)

    # /health queda fuera de /api/v1: es la única ruta pública (excepción justificada, T4.9).
    app.include_router(health.router)
    return app
