"""Almacén vectorial (T3.4): insertar → buscar → borrar, filtro por usuario y puntaje normalizado."""

import math
import uuid

import pytest
from langchain_core.embeddings import Embeddings
from sqlalchemy import text

from app.services.ingestion.splitter import Chunk
from app.vectorstore.store import VectorStore, cosine_distance_to_similarity
from tests.database import temporary_database

pytestmark = pytest.mark.integration

DIM = 1024


def unit(*weights: float) -> list[float]:
    """Vector de DIM dimensiones con los primeros componentes dados, normalizado."""
    v = list(weights) + [0.0] * (DIM - len(weights))
    norm = math.sqrt(sum(x * x for x in v))
    return [x / norm for x in v]


class FakeEmbeddings(Embeddings):
    """Embeddings deterministas: cada texto conocido tiene un vector fijo; así se controla la similitud."""

    def __init__(self, vectors: dict[str, list[float]]) -> None:
        self.vectors = vectors
        self.calls = 0

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        self.calls += 1
        return [self.vectors[t] for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self.vectors[text]


@pytest.fixture(scope="module")
def engine():
    with temporary_database("cantinero_test_store") as db:
        yield db.engine


@pytest.fixture(autouse=True)
def clean(engine):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM documents"))


def add_document(engine, store, chunks: dict[str, list[float]], *, owner: str | None, status: str = "ready") -> str:
    """Crea un documento (global si owner es None) con un fragmento por texto."""
    store.embeddings.vectors.update(chunks)
    with engine.begin() as conn:
        doc_id = conn.execute(
            text(
                "INSERT INTO documents (filename, mime_type, size_bytes, sha256, is_global, owner_id, status) "
                "VALUES (:f, 'text/markdown', 1, :sha, :g, :o, :s) RETURNING id"
            ),
            {"f": f"doc-{uuid.uuid4().hex[:6]}.md", "sha": uuid.uuid4().hex, "g": owner is None, "o": owner, "s": status},
        ).scalar_one()
        store.add_chunks(conn, doc_id, [Chunk(i, t, {"n": i}) for i, t in enumerate(chunks)])
    return str(doc_id)


QUERY = "¿Qué lleva un Negroni?"


def make_store(engine, **kwargs) -> VectorStore:
    return VectorStore(engine, FakeEmbeddings({QUERY: unit(1, 0)}), **kwargs)


def test_distance_is_normalized_to_similarity():
    assert cosine_distance_to_similarity(0.0) == 1.0
    assert cosine_distance_to_similarity(0.25) == 0.75
    assert cosine_distance_to_similarity(1.4) == 0.0  # opuestos: acotado a 0


def test_insert_search_and_delete_round_trip(engine):
    store = make_store(engine)
    doc = add_document(engine, store, {"Negroni: gin, vermut y Campari": unit(1, 0.1),
                                       "Mezcal: agave cocido": unit(0, 1)}, owner=None)

    results = store.search(QUERY, user_id="user-a", top_k=5)
    assert [r.content for r in results] == ["Negroni: gin, vermut y Campari", "Mezcal: agave cocido"]
    assert results[0].score == pytest.approx(0.995, abs=0.01)
    assert results[0].score > results[1].score
    assert results[0].document_id == doc and results[0].is_global and results[0].metadata == {"n": 0}

    with engine.begin() as conn:
        assert store.delete_document_chunks(conn, doc) == 2
    assert store.search(QUERY, user_id="user-a", top_k=5) == []


def test_min_score_filters_low_similarity(engine):
    store = make_store(engine)
    add_document(engine, store, {"Negroni": unit(1, 0.1), "Sushi": unit(0.2, 1)}, owner=None)
    results = store.search(QUERY, user_id="user-a", top_k=5, min_score=0.5)
    assert [r.content for r in results] == ["Negroni"]


def test_user_sees_global_and_own_documents_but_never_other_users(engine):
    store = make_store(engine)
    add_document(engine, store, {"global": unit(1, 0.3)}, owner=None)
    add_document(engine, store, {"de A": unit(1, 0.2)}, owner="user-a")
    add_document(engine, store, {"de B": unit(1, 0.1)}, owner="user-b")

    seen_by_a = {r.content for r in store.search(QUERY, user_id="user-a", top_k=10)}
    assert seen_by_a == {"global", "de A"}


def test_documents_not_ready_are_not_searched(engine):
    store = make_store(engine)
    add_document(engine, store, {"procesando": unit(1, 0)}, owner=None, status="processing")
    add_document(engine, store, {"fallido": unit(1, 0)}, owner="user-a", status="failed")
    assert store.search(QUERY, user_id="user-a", top_k=5) == []


# Con pocos datos PostgreSQL ordena todo de forma exacta y nunca usa el índice HNSW; en producción, con
# miles de fragmentos, sí lo usa. Estas opciones obligan a recorrer el índice HNSW, como pasará en producción.
FORCE_HNSW = {"enable_seqscan": "off", "enable_sort": "off"}


def _starvation_scenario(engine, search_settings: dict[str, str]) -> list[str]:
    store = make_store(engine, search_settings=search_settings)
    add_document(engine, store, {f"privado de B {i}": unit(1, 0.001 * i) for i in range(300)}, owner="user-b")
    add_document(engine, store, {f"global {i}": unit(1, 0.8 + 0.1 * i) for i in range(3)}, owner=None)
    return sorted(r.content for r in store.search(QUERY, user_id="user-a", top_k=3))


def test_many_similar_private_chunks_of_another_user_do_not_starve_results(engine):
    """Hallazgo 8 de la revisión de la Fase 1: con HNSW, el filtro se aplica después de recorrer el índice.
    300 fragmentos privados de B casi idénticos a la pregunta no deben dejar a A sin sus 3 resultados."""
    assert _starvation_scenario(engine, FORCE_HNSW) == ["global 0", "global 1", "global 2"]


def test_without_iterative_scan_the_user_filter_starves_results(engine):
    """Control negativo: documenta por qué existe hnsw.iterative_scan. Sin él, A no recibe nada."""
    no_iterative = {**FORCE_HNSW, "hnsw.iterative_scan": "off", "hnsw.ef_search": "40"}
    assert _starvation_scenario(engine, no_iterative) == []


def test_embeddings_are_requested_once_per_document(engine):
    store = make_store(engine)
    add_document(engine, store, {f"t{i}": unit(1, i) for i in range(5)}, owner=None)
    assert store.embeddings.calls == 1
