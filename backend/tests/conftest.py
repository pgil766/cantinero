import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app

REQUIRED = {
    "app_env": "test",
    "database_url": "postgresql+psycopg://user:pass@localhost:5432/test",
    "keycloak_issuer": "http://localhost:8080/auth/realms/cantinero",
    "keycloak_internal_url": "http://localhost:8080/auth",
}


def make_settings(**overrides) -> Settings:
    """Settings de prueba que NO leen el .env del equipo."""
    return Settings(_env_file=None, **{**REQUIRED, **overrides})


@pytest.fixture
def settings() -> Settings:
    return make_settings()


@pytest.fixture
def client(settings: Settings) -> TestClient:
    return TestClient(create_app(settings), raise_server_exceptions=False)
