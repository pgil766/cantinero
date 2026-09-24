"""BD temporal para pruebas de integración, sobre el Postgres de docker compose.

Reproduce el escenario real: el superusuario crea la BD y la extensión vector (como db/init/01-init.sh)
y las migraciones las aplica el rol SIN privilegios de la aplicación.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

import pytest
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import OperationalError

from app.core.config import ConfigError, load_settings
from app.db.migrations import apply_migrations


class _AdminEnv(BaseSettings):
    """Credenciales de superusuario del .env (solo para preparar la BD de prueba)."""

    model_config = SettingsConfigDict(env_file=("../.env", ".env"), extra="ignore")
    postgres_user: str
    postgres_password: str


@dataclass
class MigratedDb:
    engine: Engine
    first_run: list[str]


@contextmanager
def temporary_database(name: str) -> Iterator[MigratedDb]:
    """Crea la BD `name` con todas las migraciones aplicadas y la borra al salir (o omite la prueba)."""
    try:
        app_url = make_url(load_settings().database_url)
        admin_env = _AdminEnv()
    except (ConfigError, ValidationError):
        pytest.skip("No hay .env con DATABASE_URL y POSTGRES_USER/POSTGRES_PASSWORD")

    admin_url = app_url.set(username=admin_env.postgres_user, password=admin_env.postgres_password)
    admin = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    try:
        with admin.connect() as conn:
            conn.execute(text(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))
            conn.execute(text(f'CREATE DATABASE "{name}" OWNER "{app_url.username}"'))
    except OperationalError:
        pytest.skip("PostgreSQL no disponible (docker compose up -d postgres)")

    admin_db = create_engine(admin_url.set(database=name), isolation_level="AUTOCOMMIT")
    with admin_db.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    admin_db.dispose()

    engine = create_engine(app_url.set(database=name))
    try:
        yield MigratedDb(engine=engine, first_run=apply_migrations(engine))
    finally:
        engine.dispose()
        with admin.connect() as conn:
            conn.execute(text(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))
        admin.dispose()
