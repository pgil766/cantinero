"""Modelo de lenguaje local (Ollama) usado por los nodos del agente (AGENTS.md §6.1)."""

from typing import Any

from langchain_core.callbacks import AsyncCallbackManagerForLLMRun, CallbackManagerForLLMRun
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult
from langchain_ollama import ChatOllama

from app.core.config import Settings
from app.core.ollama import ollama_errors


class LocalChatModel(ChatOllama):
    """ChatOllama con dos garantías para CUALQUIER forma de uso (invoke, cadenas LCEL, nodos de LangGraph):

    - Sin streaming: así el timeout del cliente cubre la respuesta completa. Con streaming, cada token
      reinicia el reloj y una respuesta larga nunca dispararía el timeout.
    - Errores de Ollama traducidos a ModelUnavailableError (HTTP 503), nunca a un 500.
    """

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        kwargs.setdefault("stream", False)
        with ollama_errors(self.model):
            return super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: AsyncCallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        kwargs.setdefault("stream", False)
        with ollama_errors(self.model):
            return await super()._agenerate(messages, stop=stop, run_manager=run_manager, **kwargs)


def build_chat_model(settings: Settings, *, json_mode: bool = False) -> LocalChatModel:
    """Modelo configurado desde el entorno.

    json_mode=True obliga al modelo a responder JSON (clasificador de intención, validadores); esas
    respuestas son cortas, así que se limita más el número de tokens.
    """
    extra = {"format": "json"} if json_mode else {}
    return LocalChatModel(
        model=settings.llm_model,
        base_url=settings.ollama_base_url,
        temperature=settings.llm_temperature,
        num_predict=settings.llm_json_num_predict if json_mode else settings.llm_num_predict,
        keep_alive=settings.ollama_keep_alive,
        client_kwargs={"timeout": settings.llm_timeout_seconds},
        **extra,
    )


def invoke_llm(llm: ChatOllama, messages: list[BaseMessage] | str) -> str:
    """Atajo: llama al modelo y devuelve solo el texto."""
    return str(llm.invoke(messages).content)
