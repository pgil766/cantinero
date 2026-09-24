"""Migraciones sobre una BD temporal del Postgres de docker compose (ver tests/database.py)."""

import uuid

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.db.migrations import EmbeddingDimMismatch, apply_migrations, verify_embedding_dim
from tests.database import temporary_database

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def db():
    with temporary_database("cantinero_test_migrations") as migrated:
        yield migrated


def test_app_role_is_not_superuser(db):
    with db.engine.connect() as conn:
        is_super = conn.execute(text("SELECT usesuper FROM pg_user WHERE usename = current_user")).scalar_one()
    assert is_super is False


def test_migrations_create_schema_and_are_idempotent(db):
    assert db.first_run == ["001_init", "002_embedding_dim_768", "003_embedding_dim_1024"]
    assert apply_migrations(db.engine) == []  # la segunda vez no hace nada

    with db.engine.connect() as conn:
        tables = set(
            conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            ).scalars()
        )
    assert {"documents", "chunks", "conversations", "messages", "schema_migrations"} <= tables


def test_percent_signs_in_migrations_are_kept_literally(db, tmp_path):
    (tmp_path / "900_percent.sql").write_text(
        "CREATE TABLE pct_test (v TEXT);\n"
        "INSERT INTO pct_test VALUES ('40% vol.');\n"
        "DO $$ BEGIN IF (SELECT count(*) FROM pct_test WHERE v LIKE '%vol%') <> 1 THEN "
        "RAISE EXCEPTION 'LIKE falló: %', 1; END IF; END $$;\n",
        encoding="utf-8",
    )
    assert apply_migrations(db.engine, tmp_path) == ["900_percent"]
    with db.engine.connect() as conn:
        assert conn.execute(text("SELECT v FROM pct_test")).scalar_one() == "40% vol."


def test_embedding_dim_is_verified_against_the_column(db):
    verify_embedding_dim(db.engine, 1024)
    with pytest.raises(EmbeddingDimMismatch, match="VECTOR\\(1024\\)"):
        verify_embedding_dim(db.engine, 768)  # dimensión del modelo anterior: debe fallar


def _insert_document(conn, *, is_global: bool, owner_id: str | None, sha: str = "abc", status: str = "ready"):
    conn.execute(
        text(
            "INSERT INTO documents (filename, mime_type, size_bytes, sha256, is_global, owner_id, status) "
            "VALUES ('a.pdf', 'application/pdf', 10, :sha, :g, :o, :s)"
        ),
        {"sha": sha, "g": is_global, "o": owner_id, "s": status},
    )


def test_global_documents_cannot_have_owner_and_private_ones_must(db):
    with pytest.raises(IntegrityError), db.engine.begin() as conn:
        _insert_document(conn, is_global=True, owner_id="user-a")
    with pytest.raises(IntegrityError), db.engine.begin() as conn:
        _insert_document(conn, is_global=False, owner_id=None)


def test_same_file_is_unique_per_owner_but_allowed_across_owners(db):
    sha = uuid.uuid4().hex
    with db.engine.begin() as conn:
        _insert_document(conn, is_global=False, owner_id="user-a", sha=sha)
        _insert_document(conn, is_global=False, owner_id="user-b", sha=sha)
    with pytest.raises(IntegrityError), db.engine.begin() as conn:
        _insert_document(conn, is_global=False, owner_id="user-a", sha=sha)


def test_a_failed_upload_does_not_block_retrying_the_same_file(db):
    sha = uuid.uuid4().hex
    with db.engine.begin() as conn:
        _insert_document(conn, is_global=False, owner_id="user-a", sha=sha, status="failed")
        _insert_document(conn, is_global=False, owner_id="user-a", sha=sha, status="processing")


def test_deleting_a_document_deletes_its_chunks(db):
    with db.engine.begin() as conn:
        doc_id = conn.execute(
            text(
                "INSERT INTO documents (filename, mime_type, size_bytes, sha256, is_global) "
                "VALUES ('seed.md', 'text/markdown', 5, :sha, TRUE) RETURNING id"
            ),
            {"sha": uuid.uuid4().hex},
        ).scalar_one()
        conn.execute(
            text(
                "INSERT INTO chunks (document_id, chunk_index, content, embedding) "
                "VALUES (:d, 0, 'Negroni', :e)"
            ),
            {"d": doc_id, "e": "[" + ",".join(["0.1"] * 1024) + "]"},
        )
        conn.execute(text("DELETE FROM documents WHERE id = :d"), {"d": doc_id})
        remaining = conn.execute(
            text("SELECT count(*) FROM chunks WHERE document_id = :d"), {"d": doc_id}
        ).scalar_one()
    assert remaining == 0
