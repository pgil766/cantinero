"""Pipeline de ingesta (AGENTS.md §13, RF-DOC-1..6, T3.5, T3.6).

validar → registrar ('processing') → extraer → fragmentar → embeddings → guardar fragmentos y marcar
'ready' (una transacción) → resultado para confirmar al usuario.

Si algo falla después de registrar el documento, queda en 'failed' con un error legible y sin fragmentos
a medias. El error se propaga para que la API responda con su código (409, 413, 415, 422, 503).
"""

import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from sqlalchemy import Engine

from app.core.errors import AppError
from app.db.repositories import documents as documents_repo
from app.services.ingestion.loaders import MIME_TYPES, UnsupportedFormatError, extension_of, load_document
from app.services.ingestion.splitter import split_sections
from app.vectorstore.store import VectorStore

logger = logging.getLogger(__name__)


class FileTooLargeError(AppError):
    def __init__(self, max_mb: int) -> None:
        super().__init__(f"El archivo supera el tamaño máximo de {max_mb} MB.", code="file_too_large", status_code=413)


class ContentMismatchError(AppError):
    def __init__(self, filename: str) -> None:
        super().__init__(f"El contenido de '{filename}' no corresponde a su extensión.",
                         code="content_mismatch", status_code=415)


@dataclass(frozen=True)
class IngestionResult:
    document_id: UUID
    filename: str
    status: str
    chunk_count: int


@dataclass(frozen=True)
class IngestionConfig:
    chunk_size: int
    chunk_overlap: int
    max_upload_mb: int

    @classmethod
    def from_settings(cls, settings) -> "IngestionConfig":
        return cls(settings.chunk_size, settings.chunk_overlap, settings.max_upload_mb)


def validate_file(path: Path, filename: str, max_upload_mb: int) -> str:
    """Valida extensión, tamaño y que el contenido corresponda al formato. Devuelve el MIME canónico.

    No se confía en el MIME que manda el navegador (varía entre sistemas: un .csv puede llegar como
    application/vnd.ms-excel): se revisan los primeros bytes del archivo."""
    ext = extension_of(filename)
    if ext not in MIME_TYPES:
        raise UnsupportedFormatError(filename)
    if path.stat().st_size > max_upload_mb * 1024 * 1024:
        raise FileTooLargeError(max_upload_mb)

    head = path.read_bytes()[:4096]
    looks_valid = {
        ".pdf": head.startswith(b"%PDF-"),
        ".docx": head.startswith(b"PK\x03\x04"),  # un DOCX es un ZIP
    }.get(ext, b"\x00" not in head)  # formatos de texto: sin bytes nulos (no es un binario renombrado)
    if not looks_valid:
        raise ContentMismatchError(filename)
    return MIME_TYPES[ext]


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def ingest_file(path: Path, filename: str, owner_id: str | None, *, engine: Engine, store: VectorStore,
                config: IngestionConfig) -> IngestionResult:
    """Procesa un archivo completo. owner_id=None → documento global (seed, solo lectura)."""
    mime_type = validate_file(path, filename, config.max_upload_mb)
    with engine.begin() as conn:
        document_id = documents_repo.insert_processing(
            conn, filename=filename, mime_type=mime_type, size_bytes=path.stat().st_size,
            sha256=sha256_of(path), owner_id=owner_id,
        )

    try:
        sections = load_document(path, filename)
        chunks = split_sections(sections, config.chunk_size, config.chunk_overlap)
        if not chunks:
            raise AppError(f"El documento '{filename}' no tiene texto suficiente para indexar.",
                           code="unreadable_document", status_code=422)
        vectors = store.embed_chunks(chunks)  # lo lento, fuera de la transacción
        with engine.begin() as conn:
            store.add_chunks(conn, document_id, chunks, vectors)
            documents_repo.mark_ready(conn, document_id, len(chunks))
    except Exception as exc:
        reason = exc.detail if isinstance(exc, AppError) else "Error interno al procesar el documento."
        logger.exception("Falló la ingesta de %s (%s)", filename, document_id) if not isinstance(exc, AppError) \
            else logger.warning("Falló la ingesta de %s (%s): %s", filename, document_id, reason)
        with engine.begin() as conn:
            documents_repo.mark_failed(conn, document_id, reason)
        raise

    logger.info("Documento indexado: %s → %d fragmentos (%s)", filename, len(chunks), document_id)
    return IngestionResult(document_id=document_id, filename=filename, status="ready", chunk_count=len(chunks))
