"""Embeddings locales servidos por Ollama con bge-m3 (AGENTS.md §6.1, D13)."""

from langchain_ollama import OllamaEmbeddings

from app.core.config import Settings
from app.core.ollama import ollama_errors


class LocalEmbeddings(OllamaEmbeddings):
    """OllamaEmbeddings que:

    - envía los textos en lotes de `batch_size` (una sola petición con todo un PDF grande podría superar
      el timeout, sobre todo en la VM sin GPU);
    - traduce los errores de Ollama a ModelUnavailableError (HTTP 503) en cualquier forma de uso.
    """

    batch_size: int = 32

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        with ollama_errors(self.model):
            for i in range(0, len(texts), self.batch_size):
                vectors.extend(super().embed_documents(texts[i : i + self.batch_size]))
        return vectors

    def embed_query(self, text: str) -> list[float]:
        with ollama_errors(self.model):
            return super().embed_query(text)

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        with ollama_errors(self.model):
            for i in range(0, len(texts), self.batch_size):
                vectors.extend(await super().aembed_documents(texts[i : i + self.batch_size]))
        return vectors

    async def aembed_query(self, text: str) -> list[float]:
        with ollama_errors(self.model):
            return await super().aembed_query(text)


def build_embeddings(settings: Settings, **overrides) -> LocalEmbeddings:
    """Objeto de embeddings de LangChain. Usar SIEMPRE el mismo modelo para indexar y consultar."""
    params = {
        "model": settings.embedding_model,
        "base_url": settings.ollama_base_url,
        "keep_alive": settings.ollama_keep_alive,
        "batch_size": settings.embedding_batch_size,
        "client_kwargs": {"timeout": settings.embedding_timeout_seconds},
        **overrides,
    }
    return LocalEmbeddings(**params)
