"""LLM y embeddings servidos por Ollama (Fase 2: T2.1, T2.2, T2.3)."""

import math

import httpx
import ollama
import pytest
from fastapi.testclient import TestClient
from langchain_ollama import OllamaEmbeddings

from app.agents.llm import build_chat_model, invoke_llm
from app.core.config import ConfigError, load_settings
from app.core.ollama import ModelUnavailableError, missing_models, ollama_errors
from app.main import create_app
from app.vectorstore.embeddings import build_embeddings
from tests.conftest import REQUIRED, make_settings

# Puerto cerrado: simula "Ollama apagado" sin tener que apagarlo.
DEAD_OLLAMA = "http://127.0.0.1:9"


# --- Configuración (sin Ollama) -------------------------------------------------------------

def test_chat_model_is_built_from_settings():
    s = make_settings(llm_model="qwen2.5:3b", llm_temperature=0.1, ollama_base_url="http://ollama:11434",
                      llm_timeout_seconds=90, llm_num_predict=400)
    llm = build_chat_model(s)
    assert (llm.model, llm.temperature, llm.base_url) == ("qwen2.5:3b", 0.1, "http://ollama:11434")
    assert llm.num_predict == 400
    assert llm.client_kwargs == {"timeout": 90}
    assert llm.keep_alive == s.ollama_keep_alive
    assert not llm.format


def test_json_mode_forces_json_and_a_shorter_token_limit():
    llm = build_chat_model(make_settings(llm_json_num_predict=128), json_mode=True)
    assert llm.format == "json"
    assert llm.num_predict == 128


def test_embeddings_are_built_from_settings():
    s = make_settings(embedding_model="bge-m3", ollama_base_url="http://ollama:11434",
                      embedding_batch_size=16, embedding_timeout_seconds=45)
    emb = build_embeddings(s)
    assert (emb.model, emb.base_url, emb.batch_size) == ("bge-m3", "http://ollama:11434", 16)
    assert emb.client_kwargs == {"timeout": 45}


@pytest.mark.parametrize("field", ["llm_model", "embedding_model", "ollama_base_url"])
def test_empty_model_or_url_is_rejected_at_startup(field):
    with pytest.raises(ConfigError, match=field.upper()):
        load_settings(_env_file=None, **{**REQUIRED, field: ""})


def test_embed_documents_is_sent_in_batches(monkeypatch):
    calls: list[int] = []

    def fake_parent(self, texts):
        calls.append(len(texts))
        return [[0.0] for _ in texts]

    monkeypatch.setattr(OllamaEmbeddings, "embed_documents", fake_parent)
    vectors = build_embeddings(make_settings(embedding_batch_size=32)).embed_documents(["texto"] * 70)
    assert calls == [32, 32, 6]
    assert len(vectors) == 70


# --- Traducción de errores a 503 (T2.3, sin Ollama) -----------------------------------------

@pytest.mark.parametrize(
    ("error", "expected_text"),
    [
        (ConnectionError("Failed to connect to Ollama"), "No se pudo conectar"),
        (httpx.ConnectError("refused"), "No se pudo conectar"),
        (httpx.ReadTimeout("timeout"), "tardó demasiado"),
        (ollama.ResponseError("model not found", 404), "no está disponible"),
        (ollama.ResponseError("boom", 500), "respondió con un error"),
    ],
)
def test_ollama_errors_become_model_unavailable(error, expected_text):
    with pytest.raises(ModelUnavailableError) as exc, ollama_errors("qwen2.5:3b"):
        raise error
    assert exc.value.status_code == 503
    assert exc.value.code == "model_unavailable"
    assert expected_text in exc.value.detail


def test_llm_invoke_with_ollama_down_raises_503_error():
    llm = build_chat_model(make_settings(ollama_base_url=DEAD_OLLAMA, llm_timeout_seconds=5))
    with pytest.raises(ModelUnavailableError):
        llm.invoke("hola")  # uso directo, como lo hará un nodo de LangGraph (sin funciones auxiliares)


def test_embeddings_with_ollama_down_raise_503_error():
    emb = build_embeddings(make_settings(ollama_base_url=DEAD_OLLAMA, embedding_timeout_seconds=5))
    with pytest.raises(ModelUnavailableError):
        emb.embed_query("hola")
    with pytest.raises(ModelUnavailableError):
        emb.embed_documents(["hola", "chao"])


def test_model_unavailable_reaches_the_client_as_uniform_503(settings):
    app = create_app(settings)

    @app.get("/needs-llm")
    def needs_llm():
        build_chat_model(make_settings(ollama_base_url=DEAD_OLLAMA, llm_timeout_seconds=5)).invoke("hola")

    response = TestClient(app).get("/needs-llm")
    assert response.status_code == 503
    assert response.json()["code"] == "model_unavailable"


@pytest.mark.parametrize(
    "error", [ollama.ResponseError("model not found", 404), httpx.ConnectError("refused"), ConnectionError("x")]
)
def test_untranslated_ollama_errors_still_reach_the_client_as_503(settings, error):
    """Red de seguridad: un error de Ollama que escape sin traducir no debe salir como 500."""
    app = create_app(settings)

    @app.get("/raw")
    def raw():
        raise error

    response = TestClient(app, raise_server_exceptions=False).get("/raw")
    assert response.status_code == 503
    assert response.json()["code"] == "model_unavailable"


# --- Con Ollama real (se omiten si no está corriendo) ---------------------------------------

@pytest.fixture(scope="module")
def real_settings():
    try:
        s = load_settings()
    except ConfigError:
        pytest.skip("No hay .env")
    try:
        httpx.get(f"{s.ollama_base_url}/api/version", timeout=3).raise_for_status()
    except httpx.HTTPError:
        pytest.skip(f"Ollama no está disponible en {s.ollama_base_url}")
    return s


def _cos(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


@pytest.mark.ollama
def test_configured_models_are_downloaded(real_settings):
    s = real_settings
    assert missing_models(s.ollama_base_url, [s.llm_model, s.embedding_model]) == []
    assert missing_models(s.ollama_base_url, ["modelo-que-no-existe:1b"]) == ["modelo-que-no-existe:1b"]


@pytest.mark.ollama
def test_embedding_dimension_matches_settings(real_settings):
    vector = build_embeddings(real_settings).embed_query("¿Qué lleva un Negroni?")
    assert len(vector) == real_settings.embedding_dim


@pytest.mark.ollama
def test_embeddings_read_the_whole_chunk_not_only_its_beginning(real_settings):
    """Regresión del truncamiento de paraphrase-multilingual (~500 caracteres): dos fragmentos de ~900
    caracteres que solo difieren al FINAL deben tener embeddings distintos."""
    base = ("El Negroni se prepara con gin, vermut rojo y Campari en partes iguales. " * 11)[:800]
    a = base + " Se sirve en vaso old fashioned con una rodaja de naranja."
    b = base + " El mezcal se elabora con agave cocido en hornos de tierra."
    va, vb = build_embeddings(real_settings).embed_documents([a, b])
    assert _cos(va, vb) < 0.99


@pytest.mark.ollama
def test_unknown_model_raises_503_error(real_settings):
    llm = build_chat_model(real_settings).model_copy(update={"model": "modelo-que-no-existe:1b"})
    with pytest.raises(ModelUnavailableError, match="no está disponible"):
        llm.invoke("hola")


@pytest.mark.ollama
def test_llm_is_called_without_streaming_and_respects_the_token_limit(real_settings, monkeypatch):
    seen: list[dict] = []
    original = ollama.Client.chat

    def spy(self, *args, **kwargs):
        seen.append(kwargs)
        return original(self, *args, **kwargs)

    monkeypatch.setattr(ollama.Client, "chat", spy)
    llm = build_chat_model(real_settings).model_copy(update={"num_predict": 16})
    response = llm.invoke("Escribe una lista de 50 cócteles clásicos, uno por línea.")

    assert seen and seen[0]["stream"] is False
    assert response.response_metadata["eval_count"] <= 16
    assert invoke_llm(build_chat_model(real_settings), "Responde con una sola palabra: ¿de qué color es el cielo?")
