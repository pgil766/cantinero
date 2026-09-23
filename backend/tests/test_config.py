import pytest

from app.core.config import ConfigError, load_settings
from tests.conftest import REQUIRED, make_settings

ENV_VARS = [name.upper() for name in REQUIRED] + ["CHUNK_SIZE", "CHUNK_OVERLAP", "SIMILARITY_THRESHOLD"]


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)


def test_missing_required_variables_are_listed_in_a_clear_message():
    with pytest.raises(ConfigError) as exc:
        load_settings(_env_file=None)
    message = str(exc.value)
    assert "Faltan variables de entorno obligatorias" in message
    for name in ("DATABASE_URL", "KEYCLOAK_ISSUER", "KEYCLOAK_INTERNAL_URL"):
        assert name in message


def test_defaults_match_the_agreed_stack():
    s = make_settings()
    assert s.llm_model == "qwen2.5:3b"
    assert s.embedding_dim == 384
    assert s.keycloak_realm == "cantinero"
    assert s.keycloak_audience == "cantinero-api"


def test_values_are_read_from_environment(monkeypatch):
    for key, value in REQUIRED.items():
        monkeypatch.setenv(key.upper(), value)
    monkeypatch.setenv("SIMILARITY_THRESHOLD", "0.6")
    s = load_settings(_env_file=None)
    assert s.similarity_threshold == 0.6


def test_cors_origins_are_split_by_comma():
    s = make_settings(cors_origins="http://localhost:5173, https://cantinero.vercel.app ,")
    assert s.cors_origin_list == ["http://localhost:5173", "https://cantinero.vercel.app"]


def test_similarity_threshold_out_of_range_is_rejected():
    with pytest.raises(ConfigError, match="SIMILARITY_THRESHOLD"):
        load_settings(_env_file=None, **REQUIRED, similarity_threshold=1.5)


def test_chunk_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ConfigError, match="CHUNK_OVERLAP"):
        load_settings(_env_file=None, **REQUIRED, chunk_size=100, chunk_overlap=100)
