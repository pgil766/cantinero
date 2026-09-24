"""Errores de dominio y formato uniforme de errores de la API: {"detail": ..., "code": ...}."""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger(__name__)

HTTP_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "method_not_allowed",
    409: "conflict",
    413: "payload_too_large",
    415: "unsupported_media_type",
    422: "validation_error",
    500: "internal_error",
    503: "service_unavailable",
}


class AppError(Exception):
    """Error de negocio que la API devuelve tal cual al cliente."""

    def __init__(self, detail: str, code: str, status_code: int = 400) -> None:
        super().__init__(detail)
        self.detail = detail
        self.code = code
        self.status_code = status_code


def error_response(status_code: int, detail: str, code: str | None = None, **extra) -> JSONResponse:
    body = {"detail": detail, "code": code or HTTP_CODES.get(status_code, "error"), **extra}
    return JSONResponse(status_code=status_code, content=body)


class UnhandledErrorMiddleware(BaseHTTPMiddleware):
    """Convierte cualquier excepción no controlada en un 500 uniforme.

    Se registra ANTES que CORSMiddleware (queda por dentro de él). Un manejador para Exception
    registrado con exception_handler correría en ServerErrorMiddleware, por fuera de CORS, y el
    navegador recibiría el 500 sin cabeceras CORS: el frontend no podría leer el mensaje.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            logger.exception("Error no controlado en %s %s: %s", request.method, request.url.path, exc)
            return error_response(500, "Ocurrió un error interno. Intenta de nuevo más tarde.")


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _app_error(_: Request, exc: AppError) -> JSONResponse:
        return error_response(exc.status_code, exc.detail, exc.code)

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        response = error_response(exc.status_code, str(exc.detail))
        if exc.headers:
            response.headers.update(exc.headers)
        return response

    @app.exception_handler(RequestValidationError)
    async def _validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        errors = [
            {"field": ".".join(str(part) for part in err["loc"][1:]), "message": err["msg"]}
            for err in exc.errors()
        ]
        return error_response(422, "Los datos enviados no son válidos.", errors=errors)
