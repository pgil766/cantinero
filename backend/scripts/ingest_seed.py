"""Carga la base de conocimiento inicial (data/seed/) como documentos GLOBALES (T3.7, AGENTS.md §13.4).

Usa el mismo pipeline que el endpoint de subida, sin duplicar lógica.

Uso (desde backend/):
    python -m scripts.ingest_seed              # agrega lo que falte (los ya cargados se omiten: 409)
    python -m scripts.ingest_seed --replace    # borra TODOS los documentos globales y los vuelve a cargar
    python -m scripts.ingest_seed --dir ruta   # otra carpeta
"""

import argparse
import sys
import time
from pathlib import Path

from sqlalchemy import text

from app.core.config import get_settings
from app.core.errors import AppError
from app.core.logging import configure_logging
from app.db.repositories.documents import DuplicateDocumentError
from app.db.session import get_engine
from app.services.ingestion.loaders import SUPPORTED_EXTENSIONS
from app.services.ingestion.pipeline import IngestionConfig, ingest_file
from app.vectorstore.embeddings import build_embeddings
from app.vectorstore.store import VectorStore

DEFAULT_SEED_DIR = Path(__file__).resolve().parents[2] / "data" / "seed"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, default=DEFAULT_SEED_DIR)
    parser.add_argument("--replace", action="store_true", help="borra los documentos globales antes de cargar")
    args = parser.parse_args()

    configure_logging("WARNING")
    settings = get_settings()
    engine = get_engine()
    store = VectorStore(engine, build_embeddings(settings))
    config = IngestionConfig.from_settings(settings)

    if args.replace:
        with engine.begin() as conn:
            removed = conn.execute(text("DELETE FROM documents WHERE is_global")).rowcount
        print(f"Documentos globales borrados: {removed}")

    files = sorted(p for p in args.dir.iterdir() if p.suffix.lower() in SUPPORTED_EXTENSIONS)
    print(f"Cargando {len(files)} archivos de {args.dir} con '{settings.embedding_model}'...")
    loaded = skipped = failed = total_chunks = 0
    start = time.perf_counter()
    for path in files:
        try:
            result = ingest_file(path, path.name, None, engine=engine, store=store, config=config)
        except DuplicateDocumentError:
            skipped += 1
            print(f"  = {path.name}: ya estaba cargado")
        except AppError as exc:
            failed += 1
            print(f"  ✗ {path.name}: {exc.detail}")
        else:
            loaded += 1
            total_chunks += result.chunk_count
            print(f"  ✓ {path.name}: {result.chunk_count} fragmentos")

    print(f"Listo en {time.perf_counter() - start:.1f} s: {loaded} cargados ({total_chunks} fragmentos), "
          f"{skipped} ya estaban, {failed} con error.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
