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
    # Obligatoria a propósito: si faltara y el valor por defecto fuera "development", /docs quedaría
    # publicado en producción.
    app_env: Literal["development", "production", "test"]
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
    # min_length=1: una variable vacía en compose ("") debe fallar al arrancar, no en la primera pregunta.
    ollama_base_url: str = Field("http://127.0.0.1:11434", min_length=1)
    # Segundos que Ollama mantiene los modelos cargados en memoria tras usarlos (evita recargas lentas).
    # Entero: OllamaEmbeddings no acepta el formato "30m" (ChatOllama sí).
    ollama_keep_alive: int = Field(1800, ge=0)
    llm_model: str = Field("qwen2.5:3b", min_length=1)
    llm_temperature: float = Field(0.1, ge=0.0, le=2.0)
    # Tiempo máximo de la respuesta COMPLETA (el modelo se llama sin streaming).
    llm_timeout_seconds: int = Field(120, gt=0)
    # Tope de tokens por respuesta: evita respuestas desbocadas que ocupen Ollama por minutos.
    llm_num_predict: int = Field(512, gt=0)
    llm_json_num_predict: int = Field(128, gt=0)  # clasificador y validadores: respuestas cortas

    # --- Embeddings y RAG (servidos por Ollama) ---
    # bge-m3: multilingüe y lee fragmentos largos (8192 tokens). paraphrase-multilingual solo leía
    # ~500 caracteres e ignoraba el resto (ver docs/bitacora.md).
    embedding_model: str = Field("bge-m3", min_length=1)
    embedding_dim: int = Field(1024, gt=0)
    embedding_batch_size: int = Field(16, gt=0)
    embedding_timeout_seconds: int = Field(120, gt=0)  # por lote (en CPU, ~0.4 s o más por fragmento)
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
