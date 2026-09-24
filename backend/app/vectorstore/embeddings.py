"""Embeddings locales servidos por Ollama (AGENTS.md §6.1)."""

from langchain_ollama import OllamaEmbeddings

from app.core.config import Settings
from app.core.ollama import ollama_errors


def build_embeddings(settings: Settings) -> OllamaEmbeddings:
    """Objeto de embeddings de LangChain. Usar SIEMPRE el mismo modelo para indexar y consultar."""
    return OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_base_url,
        keep_alive=settings.ollama_keep_alive,
        client_kwargs={"timeout": settings.llm_timeout_seconds},
    )


def embed_query(embeddings: OllamaEmbeddings, text: str) -> list[float]:
    with ollama_errors(embeddings.model):
        return embeddings.embed_query(text)


def embed_documents(embeddings: OllamaEmbeddings, texts: list[str]) -> list[list[float]]:
    with ollama_errors(embeddings.model):
        return embeddings.embed_documents(texts)
