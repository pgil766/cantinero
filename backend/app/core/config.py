"""Configuración del backend leída de variables de entorno (AGENTS.md §15.2)."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # En local se lee el .env de la raíz del repositorio (el backend corre desde backend/).
        # En Docker las variables llegan por env_file del compose y estos archivos no existen.
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Aplicación ---
    app_env: Literal["development", "production", "test"] = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173"

    # --- Base de datos ---
    database_url: str

    # --- Keycloak ---
    keycloak_issuer: str
    keycloak_internal_url: str
    keycloak_realm: str = "cantinero"
    keycloak_audience: str = "cantinero-api"

    # --- Modelo local ---
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "qwen2.5:3b"
    llm_temperature: float = Field(0.1, ge=0.0, le=2.0)
    llm_timeout_seconds: int = Field(120, gt=0)

    # --- Embeddings y RAG ---
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    embedding_dim: int = Field(384, gt=0)
    chunk_size: int = Field(900, gt=0)
    chunk_overlap: int = Field(150, ge=0)
    retrieval_top_k: int = Field(5, gt=0)
    similarity_threshold: float = Field(0.45, ge=0.0, le=1.0)
    chat_history_turns: int = Field(6, ge=0)
    max_upload_mb: int = Field(20, gt=0)

    @model_validator(mode="after")
    def _check_chunking(self) -> "Settings":
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP debe ser menor que CHUNK_SIZE")
        return self

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


class ConfigError(RuntimeError):
    """Configuración inválida o incompleta, con un mensaje legible para el equipo."""


def load_settings(**overrides) -> Settings:
    """Crea Settings y traduce los errores de validación a un mensaje claro en español."""
    try:
        return Settings(**overrides)
    except ValidationError as exc:
        missing = [str(err["loc"][0]).upper() for err in exc.errors() if err["type"] == "missing"]
        invalid = [
            f"{str(err['loc'][0]).upper() if err['loc'] else 'CONFIG'}: {err['msg']}"
            for err in exc.errors()
            if err["type"] != "missing"
        ]
        parts = []
        if missing:
            parts.append("Faltan variables de entorno obligatorias: " + ", ".join(missing))
        if invalid:
            parts.append("Variables con valores inválidos: " + "; ".join(invalid))
        raise ConfigError(". ".join(parts) + ". Revisa el archivo .env (ver .env.example).") from None


@lru_cache
def get_settings() -> Settings:
    return load_settings()
