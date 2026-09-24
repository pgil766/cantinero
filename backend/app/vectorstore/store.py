"""Almacén vectorial en PostgreSQL + pgvector (AGENTS.md §10.2, RT-VDB-1..4, T3.4).

- Guarda cada fragmento con su embedding y lo asocia a su documento (RT-VDB-1, RT-VDB-2).
- Busca por similitud coseno filtrando SIEMPRE a "documentos globales + documentos del usuario" (D9).
- Devuelve la similitud normalizada a 0..1 (1 = idéntico), calculada en un único lugar.
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from langchain_core.embeddings import Embeddings
from sqlalchemy import Connection, Engine, text

from app.services.ingestion.splitter import Chunk

logger = logging.getLogger(__name__)

# Con un índice HNSW, pgvector aplica el WHERE DESPUÉS de recorrer el índice (≈ ef_search candidatos):
# si muchos vecinos son fragmentos privados de otros usuarios, llegarían menos de top_k resultados.
# iterative_scan (pgvector ≥ 0.8) sigue buscando hasta completar top_k. relaxed_order puede desordenar
# levemente los resultados, por eso se reordenan en Python.
DEFAULT_SEARCH_SETTINGS = {"hnsw.iterative_scan": "relaxed_order", "hnsw.ef_search": "100"}


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: str
    document_id: str
    filename: str
    is_global: bool
    content: str
    score: float  # similitud coseno normalizada a 0..1
    metadata: dict[str, Any] = field(default_factory=dict)


def to_pgvector(vector: list[float]) -> str:
    return "[" + ",".join(f"{x:.7g}" for x in vector) + "]"


def cosine_distance_to_similarity(distance: float) -> float:
    """pgvector devuelve DISTANCIA coseno (0..2). Similitud = 1 - distancia, acotada a 0..1."""
    return max(0.0, min(1.0, 1.0 - float(distance)))


class VectorStore:
    def __init__(self, engine: Engine, embeddings: Embeddings,
                 search_settings: dict[str, str] | None = None) -> None:
        self.engine = engine
        self.embeddings = embeddings
        self.search_settings = {**DEFAULT_SEARCH_SETTINGS, **(search_settings or {})}

    # --- Escritura (dentro de la transacción de la ingesta) -------------------------------------

    def embed_chunks(self, chunks: list[Chunk]) -> list[list[float]]:
        """Calcula los embeddings (lo lento). Se llama FUERA de la transacción de la BD."""
        return self.embeddings.embed_documents([c.content for c in chunks]) if chunks else []

    def add_chunks(self, conn: Connection, document_id: UUID | str, chunks: list[Chunk],
                   vectors: list[list[float]] | None = None) -> int:
        """Inserta los fragmentos con sus embeddings (si no se pasan, los calcula)."""
        if not chunks:
            return 0
        if vectors is None:
            vectors = self.embed_chunks(chunks)
        conn.execute(
            text(
                "INSERT INTO chunks (document_id, chunk_index, content, metadata, embedding) "
                "VALUES (:document_id, :chunk_index, :content, CAST(:metadata AS JSONB), CAST(:embedding AS vector))"
            ),
            [
                {
                    "document_id": str(document_id),
                    "chunk_index": c.index,
                    "content": c.content,
                    "metadata": json.dumps(c.metadata, ensure_ascii=False),
                    "embedding": to_pgvector(v),
                }
                for c, v in zip(chunks, vectors, strict=True)
            ],
        )
        return len(chunks)

    def delete_document_chunks(self, conn: Connection, document_id: UUID | str) -> int:
        result = conn.execute(text("DELETE FROM chunks WHERE document_id = :d"), {"d": str(document_id)})
        return result.rowcount

    # --- Búsqueda -----------------------------------------------------------------------------

    def search(self, query: str, user_id: str, top_k: int, min_score: float = 0.0) -> list[RetrievedChunk]:
        """Los top_k fragmentos más similares entre los globales y los del usuario, con score ≥ min_score."""
        query_vector = to_pgvector(self.embeddings.embed_query(query))
        with self.engine.begin() as conn:
            for name, value in self.search_settings.items():
                conn.execute(text("SELECT set_config(:name, :value, true)"), {"name": name, "value": value})
            rows = conn.execute(
                text(
                    "SELECT c.id, c.document_id, d.filename, d.is_global, c.content, c.metadata, "
                    "       c.embedding <=> CAST(:q AS vector) AS distance "
                    "FROM chunks c JOIN documents d ON d.id = c.document_id "
                    "WHERE d.status = 'ready' AND (d.is_global OR d.owner_id = :user_id) "
                    "ORDER BY c.embedding <=> CAST(:q AS vector) "
                    "LIMIT :top_k"
                ),
                {"q": query_vector, "user_id": user_id, "top_k": top_k},
            ).all()

        results = [
            RetrievedChunk(
                chunk_id=str(r.id),
                document_id=str(r.document_id),
                filename=r.filename,
                is_global=r.is_global,
                content=r.content,
                score=cosine_distance_to_similarity(r.distance),
                metadata=r.metadata or {},
            )
            for r in rows
        ]
        results.sort(key=lambda r: r.score, reverse=True)
        logger.info("Búsqueda: %d candidatos, scores=%s, umbral=%.2f",
                    len(results), [round(r.score, 3) for r in results], min_score)
        return [r for r in results if r.score >= min_score]
