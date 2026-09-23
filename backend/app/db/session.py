"""Conexión a PostgreSQL (SQLAlchemy 2 + psycopg 3)."""

from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


def build_engine(database_url: str) -> Engine:
    # pool_pre_ping evita usar conexiones muertas (reinicios de Postgres, VM que se apaga).
    # connect_timeout hace que un problema de red falle rápido en vez de colgar la petición.
    return create_engine(database_url, pool_pre_ping=True, connect_args={"connect_timeout": 10})


@lru_cache
def get_engine() -> Engine:
    return build_engine(get_settings().database_url)


@lru_cache
def _session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), expire_on_commit=False)


def get_session() -> Iterator[Session]:
    """Dependencia de FastAPI: una sesión por petición."""
    session = _session_factory()()
    try:
        yield session
    finally:
        session.close()
