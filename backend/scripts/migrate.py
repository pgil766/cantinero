"""Aplica las migraciones pendientes a la BD de DATABASE_URL y verifica la dimensión de los embeddings.

Uso (desde backend/):  python -m scripts.migrate
"""

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.migrations import apply_migrations, verify_embedding_dim
from app.db.session import get_engine


def main() -> None:
    configure_logging()
    engine = get_engine()
    applied = apply_migrations(engine)
    print(f"Migraciones aplicadas: {', '.join(applied)}" if applied else "La BD ya está al día.")
    verify_embedding_dim(engine, get_settings().embedding_dim)


if __name__ == "__main__":
    main()
