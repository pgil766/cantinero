"""Aplica las migraciones pendientes a la BD de DATABASE_URL.

Uso (desde backend/):  python -m scripts.migrate
"""

from app.core.logging import configure_logging
from app.db.migrations import apply_migrations
from app.db.session import get_engine


def main() -> None:
    configure_logging()
    applied = apply_migrations(get_engine())
    print(f"Migraciones aplicadas: {', '.join(applied)}" if applied else "La BD ya está al día.")


if __name__ == "__main__":
    main()
