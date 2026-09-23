"""Aplica las migraciones sobre una BD temporal (cantinero_test) del Postgres de docker compose."""

import uuid

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError, OperationalError

from app.core.config import ConfigError, load_settings
from app.db.migrations import apply_migrations

pytestmark = pytest.mark.integration

TEST_DB = "cantinero_test"


@pytest.fixture(scope="module")
def engine():
    try:
        base_url = make_url(load_settings().database_url)
    except ConfigError:
        pytest.skip("No hay .env con DATABASE_URL")

    admin = create_engine(base_url, isolation_level="AUTOCOMMIT")
    try:
        with admin.connect() as conn:
            conn.execute(text(f'DROP DATABASE IF EXISTS "{TEST_DB}" WITH (FORCE)'))
            conn.execute(text(f'CREATE DATABASE "{TEST_DB}"'))
    except OperationalError:
        pytest.skip("PostgreSQL no disponible (docker compose up -d postgres)")

    test_engine = create_engine(base_url.set(database=TEST_DB))
    yield test_engine

    test_engine.dispose()
    with admin.connect() as conn:
        conn.execute(text(f'DROP DATABASE IF EXISTS "{TEST_DB}" WITH (FORCE)'))
    admin.dispose()


def test_migrations_create_schema_and_are_idempotent(engine):
    assert apply_migrations(engine) == ["001_init"]
    assert apply_migrations(engine) == []  # la segunda vez no hace nada

    with engine.connect() as conn:
        tables = set(
            conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            ).scalars()
        )
        dim = conn.execute(
            text(
                "SELECT atttypmod FROM pg_attribute "
                "WHERE attrelid = 'chunks'::regclass AND attname = 'embedding'"
            )
        ).scalar_one()

    assert {"documents", "chunks", "conversations", "messages", "schema_migrations"} <= tables
    assert dim == 384


def _insert_document(conn, *, is_global: bool, owner_id: str | None, sha: str = "abc"):
    conn.execute(
        text(
            "INSERT INTO documents (filename, mime_type, size_bytes, sha256, is_global, owner_id) "
            "VALUES ('a.pdf', 'application/pdf', 10, :sha, :g, :o)"
        ),
        {"sha": sha, "g": is_global, "o": owner_id},
    )


def test_global_documents_cannot_have_owner_and_private_ones_must(engine):
    with pytest.raises(IntegrityError), engine.begin() as conn:
        _insert_document(conn, is_global=True, owner_id="user-a")
    with pytest.raises(IntegrityError), engine.begin() as conn:
        _insert_document(conn, is_global=False, owner_id=None)


def test_same_file_is_unique_per_owner_but_allowed_across_owners(engine):
    sha = uuid.uuid4().hex
    with engine.begin() as conn:
        _insert_document(conn, is_global=False, owner_id="user-a", sha=sha)
        _insert_document(conn, is_global=False, owner_id="user-b", sha=sha)
    with pytest.raises(IntegrityError), engine.begin() as conn:
        _insert_document(conn, is_global=False, owner_id="user-a", sha=sha)


def test_deleting_a_document_deletes_its_chunks(engine):
    with engine.begin() as conn:
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
            {"d": doc_id, "e": "[" + ",".join(["0.1"] * 384) + "]"},
        )
        conn.execute(text("DELETE FROM documents WHERE id = :d"), {"d": doc_id})
        remaining = conn.execute(
            text("SELECT count(*) FROM chunks WHERE document_id = :d"), {"d": doc_id}
        ).scalar_one()
    assert remaining == 0
