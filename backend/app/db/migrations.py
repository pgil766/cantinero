"""Aplicador mínimo de migraciones SQL versionadas (backend/migrations/NNN_nombre.sql).

Cada archivo se aplica una sola vez, dentro de una transacción, y queda registrado en
la tabla schema_migrations.
"""

import logging
from pathlib import Path

from sqlalchemy import Engine, text

logger = logging.getLogger(__name__)

MIGRATIONS_DIR = Path(__file__).resolve().parents[2] / "migrations"


def apply_migrations(engine: Engine, migrations_dir: Path = MIGRATIONS_DIR) -> list[str]:
    """Aplica las migraciones pendientes en orden y devuelve las que se aplicaron."""
    files = sorted(migrations_dir.glob("*.sql"))
    applied_now: list[str] = []

    with engine.begin() as conn:
        conn.execute(
            text(
                "CREATE TABLE IF NOT EXISTS schema_migrations ("
                " version TEXT PRIMARY KEY,"
                " applied_at TIMESTAMPTZ NOT NULL DEFAULT now())"
            )
        )
        already = set(conn.execute(text("SELECT version FROM schema_migrations")).scalars())

    for path in files:
        version = path.stem
        if version in already:
            continue
        with engine.begin() as conn:
            # Se ejecuta con el cursor de psycopg y SIN parámetros: así los "%" del SQL
            # (LIKE '%x%', '40% vol.', RAISE ... %) llegan intactos. exec_driver_sql los
            # interpretaría como marcadores de parámetro.
            conn.connection.driver_connection.execute(path.read_text(encoding="utf-8"))
            conn.execute(text("INSERT INTO schema_migrations (version) VALUES (:v)"), {"v": version})
        logger.info("Migración aplicada: %s", version)
        applied_now.append(version)

    return applied_now


class EmbeddingDimMismatch(RuntimeError):
    pass


def verify_embedding_dim(engine: Engine, expected_dim: int) -> None:
    """Falla si EMBEDDING_DIM no coincide con la columna chunks.embedding (VECTOR(N))."""
    with engine.connect() as conn:
        actual = conn.execute(
            text(
                "SELECT atttypmod FROM pg_attribute "
                "WHERE attrelid = 'chunks'::regclass AND attname = 'embedding'"
            )
        ).scalar_one()
    if actual != expected_dim:
        raise EmbeddingDimMismatch(
            f"EMBEDDING_DIM={expected_dim} no coincide con la columna chunks.embedding VECTOR({actual}). "
            "Si cambiaste el modelo de embeddings, crea una migración que cambie la dimensión y "
            "reindexa todo con scripts/reindex.py."
        )
