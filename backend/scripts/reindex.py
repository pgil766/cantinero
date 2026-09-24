"""Recalcula los embeddings de TODOS los fragmentos con el modelo actual (T3.7, AGENTS.md §6.1).

Se usa al cambiar a otro modelo de embeddings de la MISMA dimensión (el texto de cada fragmento está
guardado en la BD, así que no hacen falta los archivos originales). Si la dimensión cambia, primero va
una migración (como la 003) y después se recargan los documentos: el seed con
`python -m scripts.ingest_seed --replace` y los de los usuarios, volviéndolos a subir.

Uso (desde backend/):  python -m scripts.reindex
"""

import time

from sqlalchemy import text

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.migrations import verify_embedding_dim
from app.db.session import get_engine
from app.vectorstore.embeddings import build_embeddings
from app.vectorstore.store import to_pgvector


def main() -> None:
    configure_logging("WARNING")
    settings = get_settings()
    engine = get_engine()
    verify_embedding_dim(engine, settings.embedding_dim)
    embeddings = build_embeddings(settings)

    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, content FROM chunks ORDER BY document_id, chunk_index")).all()
    print(f"Reindexando {len(rows)} fragmentos con '{settings.embedding_model}'...")

    start = time.perf_counter()
    batch = settings.embedding_batch_size
    for i in range(0, len(rows), batch):
        part = rows[i : i + batch]
        vectors = embeddings.embed_documents([r.content for r in part])
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE chunks SET embedding = CAST(:e AS vector) WHERE id = :id"),
                [{"id": r.id, "e": to_pgvector(v)} for r, v in zip(part, vectors, strict=True)],
            )
        print(f"  {min(i + batch, len(rows))}/{len(rows)}")
    print(f"Listo en {time.perf_counter() - start:.1f} s.")


if __name__ == "__main__":
    main()
