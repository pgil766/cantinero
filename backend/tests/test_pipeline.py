"""Pipeline de ingesta (T3.5) y duplicados (T3.6), sobre una BD temporal y embeddings falsos."""

import pytest
from sqlalchemy import text

from app.core.ollama import ModelUnavailableError
from app.db.repositories import documents as documents_repo
from app.db.repositories.documents import DuplicateDocumentError
from app.services.ingestion.loaders import UnsupportedFormatError
from app.services.ingestion.pipeline import (
    ContentMismatchError,
    FileTooLargeError,
    IngestionConfig,
    ingest_file,
)
from app.vectorstore.store import VectorStore
from tests.database import temporary_database
from tests.document_factory import make_pdf
from tests.test_store import DIM

pytestmark = pytest.mark.integration

CONFIG = IngestionConfig(chunk_size=300, chunk_overlap=50, max_upload_mb=1)


class HashEmbeddings:
    """Embeddings falsos: cualquier texto → vector fijo. Opcionalmente fallan (Ollama caído)."""

    def __init__(self, fail: bool = False) -> None:
        self.fail = fail

    def embed_documents(self, texts):
        if self.fail:
            raise ModelUnavailableError("No se pudo conectar con el modelo local.")
        return [[1.0] + [0.0] * (DIM - 1) for _ in texts]

    def embed_query(self, text):
        return self.embed_documents([text])[0]


@pytest.fixture(scope="module")
def engine():
    with temporary_database("cantinero_test_pipeline") as db:
        yield db.engine


@pytest.fixture(autouse=True)
def clean(engine):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM documents"))


def ingest(engine, path, filename, owner="user-a", fail=False):
    return ingest_file(path, filename, owner, engine=engine, store=VectorStore(engine, HashEmbeddings(fail)),
                       config=CONFIG)


def doc_rows(engine):
    with engine.connect() as conn:
        return conn.execute(text("SELECT filename, status, chunk_count, is_global, owner_id, error FROM documents")).all()


RECIPES = "nombre,ingredientes\nNegroni,gin; vermut rojo; Campari\nMojito,ron blanco; lima; hierbabuena\n"


def test_private_document_is_indexed_and_confirmed(engine, tmp_path):
    path = tmp_path / "recetas.csv"
    path.write_text(RECIPES, encoding="utf-8")

    result = ingest(engine, path, "recetas.csv")

    assert (result.status, result.chunk_count) == ("ready", 2)
    [row] = doc_rows(engine)
    assert (row.filename, row.status, row.chunk_count, row.is_global, row.owner_id) == (
        "recetas.csv", "ready", 2, False, "user-a")
    with engine.connect() as conn:
        assert conn.execute(text("SELECT count(*) FROM chunks")).scalar_one() == 2


def test_seed_document_without_owner_is_global(engine, tmp_path):
    path = tmp_path / "guia.pdf"
    path.write_bytes(make_pdf(["Técnica de agitado: se agita con hielo en la coctelera."]))
    ingest(engine, path, "guia.pdf", owner=None)
    [row] = doc_rows(engine)
    assert row.is_global and row.owner_id is None and row.status == "ready"


def test_same_file_twice_is_rejected_with_409(engine, tmp_path):
    path = tmp_path / "recetas.csv"
    path.write_text(RECIPES, encoding="utf-8")
    ingest(engine, path, "recetas.csv")
    with pytest.raises(DuplicateDocumentError) as exc:
        ingest(engine, path, "otra_copia.csv")
    assert exc.value.status_code == 409
    assert len(doc_rows(engine)) == 1


def test_same_file_is_allowed_for_a_different_user(engine, tmp_path):
    path = tmp_path / "recetas.csv"
    path.write_text(RECIPES, encoding="utf-8")
    ingest(engine, path, "recetas.csv", owner="user-a")
    ingest(engine, path, "recetas.csv", owner="user-b")
    assert len(doc_rows(engine)) == 2


def test_failure_leaves_document_failed_without_chunks_and_retry_succeeds(engine, tmp_path):
    path = tmp_path / "recetas.csv"
    path.write_text(RECIPES, encoding="utf-8")

    with pytest.raises(ModelUnavailableError):
        ingest(engine, path, "recetas.csv", fail=True)
    [row] = doc_rows(engine)
    assert (row.status, row.chunk_count) == ("failed", 0)
    assert "modelo local" in row.error
    with engine.connect() as conn:
        assert conn.execute(text("SELECT count(*) FROM chunks")).scalar_one() == 0

    ingest(engine, path, "recetas.csv")  # reintento: el 'failed' no bloquea y se reemplaza
    assert [(r.status, r.chunk_count) for r in doc_rows(engine)] == [("ready", 2)]


def test_unreadable_document_is_marked_failed_with_a_clear_reason(engine, tmp_path):
    path = tmp_path / "escaneado.pdf"
    path.write_bytes(make_pdf([""]))
    with pytest.raises(Exception, match="escaneada"):
        ingest(engine, path, "escaneado.pdf")
    [row] = doc_rows(engine)
    assert row.status == "failed" and "escaneada" in row.error


@pytest.mark.parametrize(
    ("filename", "content", "error"),
    [
        ("foto.jpg", b"\xff\xd8\xff", UnsupportedFormatError),
        ("falso.pdf", b"esto es texto, no un PDF", ContentMismatchError),
        ("falso.docx", b"texto plano", ContentMismatchError),
        ("binario.txt", b"MZ\x00\x00\x00", ContentMismatchError),
        ("enorme.txt", None, FileTooLargeError),  # se genera en la prueba: 1 MB + 1 byte
    ],
    ids=["formato", "pdf-falso", "docx-falso", "binario-renombrado", "demasiado-grande"],
)
def test_invalid_files_are_rejected_before_creating_a_document(engine, tmp_path, filename, content, error):
    path = tmp_path / filename
    path.write_bytes(content if content is not None else b"a" * (CONFIG.max_upload_mb * 1024 * 1024 + 1))
    with pytest.raises(error):
        ingest(engine, path, filename)
    assert doc_rows(engine) == []


def test_repository_lists_global_and_own_documents_only(engine, tmp_path):
    for owner, name in [(None, "seed.md"), ("user-a", "mio.md"), ("user-b", "ajeno.md")]:
        path = tmp_path / name
        path.write_text(f"# {name}\nContenido del documento {name} sobre coctelería.", encoding="utf-8")
        ingest(engine, path, name, owner=owner)
    with engine.connect() as conn:
        visible = [d.filename for d in documents_repo.list_visible(conn, "user-a")]
    assert visible == ["mio.md", "seed.md"]  # primero los propios
