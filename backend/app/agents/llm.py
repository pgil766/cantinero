"""Modelo de lenguaje local (Ollama) usado por los nodos del agente (AGENTS.md §6.1)."""

from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama

from app.core.config import Settings
from app.core.ollama import ollama_errors


def build_chat_model(settings: Settings, *, json_mode: bool = False) -> ChatOllama:
    """ChatOllama configurado desde el entorno.

    json_mode=True obliga al modelo a responder JSON (clasificador de intención, validadores).
    """
    extra = {"format": "json"} if json_mode else {}
    return ChatOllama(
        model=settings.llm_model,
        base_url=settings.ollama_base_url,
        temperature=settings.llm_temperature,
        keep_alive=settings.ollama_keep_alive,
        client_kwargs={"timeout": settings.llm_timeout_seconds},
        **extra,
    )


def invoke_llm(llm: ChatOllama, messages: list[BaseMessage] | str) -> str:
    """Llama al modelo y devuelve el texto; los errores de Ollama salen como ModelUnavailableError (503)."""
    with ollama_errors(llm.model):
        return str(llm.invoke(messages).content)
