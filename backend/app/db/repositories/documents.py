"""Acceso a la tabla documents (AGENTS.md §10.2)."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from psycopg.errors import UniqueViolation
from sqlalchemy import Connection, text
from sqlalchemy.exc import IntegrityError

from app.core.errors import AppError


class DuplicateDocumentError(AppError):
    def __init__(self, filename: str) -> None:
        super().__init__(f"El documento '{filename}' ya está en tu base de conocimiento.",
                         code="duplicate_document", status_code=409)


@dataclass(frozen=True)
class DocumentRow:
    id: UUID
    filename: str
    mime_type: str
    size_bytes: int
    sha256: str
    is_global: bool
    owner_id: str | None
    status: str
    error: str | None
    chunk_count: int
    created_at: datetime


_COLUMNS = "id, filename, mime_type, size_bytes, sha256, is_global, owner_id, status, error, chunk_count, created_at"


def insert_processing(conn: Connection, *, filename: str, mime_type: str, size_bytes: int, sha256: str,
                      owner_id: str | None) -> UUID:
    """Crea el documento en estado 'processing'. owner_id=None → documento global (seed).

    Antes borra los intentos fallidos del mismo archivo y dueño: un documento 'failed' no bloquea el
    reintento (el índice único ignora los fallidos) y así no quedan filas fallidas repetidas."""
    conn.execute(
        text("DELETE FROM documents WHERE status = 'failed' AND sha256 = :sha "
             "AND owner_id IS NOT DISTINCT FROM :owner"),
        {"sha": sha256, "owner": owner_id},
    )
    try:
        with conn.begin_nested():  # si choca con el índice único, solo se deshace este INSERT
            return conn.execute(
                text("INSERT INTO documents (filename, mime_type, size_bytes, sha256, is_global, owner_id) "
                     "VALUES (:filename, :mime, :size, :sha, :is_global, :owner) RETURNING id"),
                {"filename": filename, "mime": mime_type, "size": size_bytes, "sha": sha256,
                 "is_global": owner_id is None, "owner": owner_id},
            ).scalar_one()
    except IntegrityError as exc:
        if isinstance(exc.orig, UniqueViolation):  # mismo archivo ya subido (o dos subidas a la vez)
            raise DuplicateDocumentError(filename) from exc
        raise


def mark_ready(conn: Connection, document_id: UUID, chunk_count: int) -> None:
    conn.execute(text("UPDATE documents SET status = 'ready', error = NULL, chunk_count = :n WHERE id = :id"),
                 {"n": chunk_count, "id": document_id})


def mark_failed(conn: Connection, document_id: UUID, error: str) -> None:
    conn.execute(text("UPDATE documents SET status = 'failed', error = :e, chunk_count = 0 WHERE id = :id"),
                 {"e": error[:500], "id": document_id})


def get(conn: Connection, document_id: UUID) -> DocumentRow | None:
    row = conn.execute(text(f"SELECT {_COLUMNS} FROM documents WHERE id = :id"), {"id": document_id}).first()
    return DocumentRow(*row) if row else None


def list_visible(conn: Connection, user_id: str) -> list[DocumentRow]:
    """Documentos globales y los del usuario (D9); primero los propios, luego los más recientes."""
    rows = conn.execute(
        text(f"SELECT {_COLUMNS} FROM documents WHERE is_global OR owner_id = :u "
             "ORDER BY is_global, created_at DESC"),
        {"u": user_id},
    ).all()
    return [DocumentRow(*r) for r in rows]


def delete(conn: Connection, document_id: UUID) -> None:
    """Borra el documento; sus fragmentos se borran en cascada (ON DELETE CASCADE)."""
    conn.execute(text("DELETE FROM documents WHERE id = :id"), {"id": document_id})
