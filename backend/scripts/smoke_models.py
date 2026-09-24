"""Prueba de humo del LLM y los embeddings: responde, mide latencia y memoria.

Uso (desde backend/):
    python -m scripts.smoke_models            # como está configurado (GPU si Ollama la tiene)
    python -m scripts.smoke_models --cpu      # LLM y embeddings solo en CPU (num_gpu=0): aproxima la VM
"""

import argparse
import time

import ollama

from app.agents.llm import build_chat_model, invoke_llm
from app.core.config import get_settings
from app.core.ollama import missing_models
from app.vectorstore.embeddings import build_embeddings

QUESTION = "Responde en español en una sola frase: ¿qué es un cóctel?"
# Fragmentos de tamaño realista (~900 caracteres) para medir la indexación.
CHUNK = ("El Negroni es un cóctel italiano que se prepara con gin, vermut rojo y Campari en partes iguales. " * 9)[:900]


def _loaded_models(client: ollama.Client) -> str:
    return ", ".join(
        f"{m.model} ({m.size / 1e9:.1f} GB, {m.size_vram / 1e9:.1f} GB en GPU)" for m in client.ps().models
    ) or "ninguno"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpu", action="store_true", help="LLM y embeddings solo en CPU (num_gpu=0)")
    args = parser.parse_args()

    s = get_settings()
    client = ollama.Client(host=s.ollama_base_url, timeout=s.llm_timeout_seconds)
    print(f"Ollama: {s.ollama_base_url} | LLM: {s.llm_model} | embeddings: {s.embedding_model}"
          f" | modo: {'solo CPU' if args.cpu else 'por defecto'}")

    missing = missing_models(s.ollama_base_url, [s.llm_model, s.embedding_model])
    if missing:
        raise SystemExit(f"Faltan modelos en Ollama: {', '.join(missing)}")

    cpu_only = {"num_gpu": 0} if args.cpu else {}
    llm = build_chat_model(s).model_copy(update=cpu_only)
    embeddings = build_embeddings(s, **cpu_only)

    # --- LLM: primera llamada (incluye carga del modelo) y segunda (modelo ya en memoria) ---
    for attempt in ("en frío", "en caliente"):
        start = time.perf_counter()
        response = llm.invoke(QUESTION)
        elapsed = time.perf_counter() - start
        meta = response.response_metadata
        speed = ""
        if meta.get("eval_count") and meta.get("eval_duration"):
            speed = f" | {meta['eval_count'] / (meta['eval_duration'] / 1e9):.1f} tokens/s"
        print(f"LLM {attempt}: {elapsed:.1f} s{speed} → {str(response.content).strip()[:110]}")

    # --- Embeddings: una pregunta y un lote de 64 fragmentos de ~900 caracteres ---
    for attempt in ("en frío", "en caliente"):
        start = time.perf_counter()
        vector = embeddings.embed_query("¿Qué lleva un Negroni?")
        print(f"Embedding de consulta {attempt}: {time.perf_counter() - start:.2f} s | dimensión {len(vector)}")
    start = time.perf_counter()
    embeddings.embed_documents([CHUNK] * 64)
    elapsed = time.perf_counter() - start
    print(f"Indexación: 64 fragmentos de ~900 caracteres en {elapsed:.1f} s ({elapsed / 64 * 1000:.0f} ms/fragmento)")

    print(f"Modelos cargados: {_loaded_models(client)}")
    if args.cpu:
        # Libera los modelos cargados en CPU (keep_alive=0) para que el próximo uso vuelva a la GPU.
        client.generate(model=s.llm_model, prompt="", keep_alive=0)
        client.embed(model=s.embedding_model, input="x", keep_alive=0)
        print("Modelos descargados de memoria (el próximo uso vuelve a la configuración por defecto).")


if __name__ == "__main__":
    main()
