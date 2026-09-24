"""LLM y embeddings servidos por Ollama (Fase 2: T2.1, T2.2, T2.3)."""

import httpx
import ollama
import pytest
from fastapi.testclient import TestClient

from app.agents.llm import build_chat_model, invoke_llm
from app.core.config import ConfigError, load_settings
from app.core.ollama import ModelUnavailableError, missing_models, ollama_errors
from app.main import create_app
from app.vectorstore.embeddings import build_embeddings, embed_query
from tests.conftest import make_settings

# Puerto cerrado: simula "Ollama apagado" sin tener que apagarlo.
DEAD_OLLAMA = "http://127.0.0.1:9"


# --- Configuración (sin Ollama) -------------------------------------------------------------

def test_chat_model_is_built_from_settings():
    s = make_settings(llm_model="qwen2.5:3b", llm_temperature=0.1, ollama_base_url="http://ollama:11434")
    llm = build_chat_model(s)
    assert (llm.model, llm.temperature, llm.base_url) == ("qwen2.5:3b", 0.1, "http://ollama:11434")
    assert llm.keep_alive == s.ollama_keep_alive
    assert not llm.format


def test_json_mode_forces_json_output():
    assert build_chat_model(make_settings(), json_mode=True).format == "json"


def test_embeddings_are_built_from_settings():
    s = make_settings(embedding_model="paraphrase-multilingual", ollama_base_url="http://ollama:11434")
    emb = build_embeddings(s)
    assert (emb.model, emb.base_url) == ("paraphrase-multilingual", "http://ollama:11434")


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


def test_llm_call_with_ollama_down_raises_503_error():
    llm = build_chat_model(make_settings(ollama_base_url=DEAD_OLLAMA, llm_timeout_seconds=5))
    with pytest.raises(ModelUnavailableError):
        invoke_llm(llm, "hola")


def test_embedding_call_with_ollama_down_raises_503_error():
    emb = build_embeddings(make_settings(ollama_base_url=DEAD_OLLAMA, llm_timeout_seconds=5))
    with pytest.raises(ModelUnavailableError):
        embed_query(emb, "hola")


def test_model_unavailable_reaches_the_client_as_uniform_503(settings):
    app = create_app(settings)

    @app.get("/needs-llm")
    def needs_llm():
        invoke_llm(build_chat_model(make_settings(ollama_base_url=DEAD_OLLAMA, llm_timeout_seconds=5)), "hola")

    response = TestClient(app).get("/needs-llm")
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


@pytest.mark.ollama
def test_configured_models_are_downloaded(real_settings):
    s = real_settings
    assert missing_models(s.ollama_base_url, [s.llm_model, s.embedding_model]) == []
    assert missing_models(s.ollama_base_url, ["modelo-que-no-existe:1b"]) == ["modelo-que-no-existe:1b"]


@pytest.mark.ollama
def test_embedding_dimension_matches_settings(real_settings):
    vector = embed_query(build_embeddings(real_settings), "¿Qué lleva un Negroni?")
    assert len(vector) == real_settings.embedding_dim


@pytest.mark.ollama
def test_llm_answers_in_spanish(real_settings):
    answer = invoke_llm(build_chat_model(real_settings), "Responde solo con la palabra: hola")
    assert "hola" in answer.lower()
