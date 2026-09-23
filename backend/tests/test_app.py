from fastapi.testclient import TestClient

from app.core.errors import AppError
from app.main import create_app
from tests.conftest import make_settings


def test_health_returns_ok_without_data(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_unknown_route_uses_uniform_error_format(client):
    response = client.get("/api/v1/no-existe")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found", "code": "not_found"}


def test_app_error_is_returned_with_its_code_and_status(settings):
    app = create_app(settings)

    @app.get("/boom-app")
    def boom_app():
        raise AppError("El modelo no está disponible.", "llm_unavailable", status_code=503)

    response = TestClient(app).get("/boom-app")
    assert response.status_code == 503
    assert response.json() == {"detail": "El modelo no está disponible.", "code": "llm_unavailable"}


def test_unhandled_error_returns_500_without_leaking_details(settings):
    app = create_app(settings)

    @app.get("/boom")
    def boom():
        raise RuntimeError("secreto interno")

    response = TestClient(app, raise_server_exceptions=False).get("/boom")
    assert response.status_code == 500
    body = response.json()
    assert body["code"] == "internal_error"
    assert "secreto" not in body["detail"]


def test_validation_error_is_uniform_and_lists_fields(settings):
    app = create_app(settings)

    @app.get("/items")
    def items(limit: int):
        return {"limit": limit}

    response = TestClient(app).get("/items", params={"limit": "abc"})
    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "validation_error"
    assert body["errors"][0]["field"] == "limit"


def test_docs_are_available_in_development_only():
    dev = TestClient(create_app(make_settings(app_env="development")))
    prod = TestClient(create_app(make_settings(app_env="production")))
    assert dev.get("/docs").status_code == 200
    assert prod.get("/docs").status_code == 404
    assert prod.get("/openapi.json").status_code == 404


def test_cors_allows_only_configured_origins():
    client = TestClient(create_app(make_settings(cors_origins="http://localhost:5173")))
    preflight = {"Access-Control-Request-Method": "POST"}

    allowed = client.options("/health", headers={"Origin": "http://localhost:5173", **preflight})
    assert allowed.headers.get("access-control-allow-origin") == "http://localhost:5173"

    denied = client.options("/health", headers={"Origin": "https://malicioso.example", **preflight})
    assert "access-control-allow-origin" not in denied.headers
