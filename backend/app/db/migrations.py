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
            conn.exec_driver_sql(path.read_text(encoding="utf-8"))
            conn.execute(text("INSERT INTO schema_migrations (version) VALUES (:v)"), {"v": version})
        logger.info("Migración aplicada: %s", version)
        applied_now.append(version)

    return applied_now
