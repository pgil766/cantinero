"""Prueba de humo del LLM y los embeddings: responde, mide latencia y memoria.

Uso (desde backend/):
    python -m scripts.smoke_models            # como está configurado (GPU si Ollama la tiene)
    python -m scripts.smoke_models --cpu      # fuerza CPU (num_gpu=0): aproxima la VM sin GPU
"""

import argparse
import time

import ollama

from app.agents.llm import build_chat_model, invoke_llm
from app.core.config import get_settings
from app.core.ollama import missing_models, ollama_errors
from app.vectorstore.embeddings import build_embeddings, embed_query

QUESTION = "Responde en español en una sola frase: ¿qué es un cóctel?"


def _loaded_models(client: ollama.Client) -> str:
    return ", ".join(
        f"{m.model} ({m.size / 1e9:.1f} GB, {m.size_vram / 1e9:.1f} GB en GPU)" for m in client.ps().models
    ) or "ninguno"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpu", action="store_true", help="forzar CPU (num_gpu=0)")
    args = parser.parse_args()

    s = get_settings()
    client = ollama.Client(host=s.ollama_base_url, timeout=s.llm_timeout_seconds)
    print(f"Ollama: {s.ollama_base_url} | LLM: {s.llm_model} | embeddings: {s.embedding_model}")

    missing = missing_models(s.ollama_base_url, [s.llm_model, s.embedding_model])
    if missing:
        raise SystemExit(f"Faltan modelos en Ollama: {', '.join(missing)}")

    # --- LLM: primera llamada (incluye carga del modelo) y segunda (modelo ya en memoria) ---
    for attempt in ("en frío", "en caliente"):
        start = time.perf_counter()
        if args.cpu:
            with ollama_errors(s.llm_model):
                r = client.generate(
                    model=s.llm_model, prompt=QUESTION, keep_alive=s.ollama_keep_alive,
                    options={"num_gpu": 0, "temperature": s.llm_temperature},
                )
            answer, tokens_s = r.response, r.eval_count / (r.eval_duration / 1e9)
            extra = f" | {tokens_s:.1f} tokens/s"
        else:
            answer, extra = invoke_llm(build_chat_model(s), QUESTION), ""
        print(f"LLM {attempt}: {time.perf_counter() - start:.1f} s{extra} → {answer.strip()[:120]}")

    # --- Embeddings ---
    embeddings = build_embeddings(s)
    for attempt in ("en frío", "en caliente"):
        start = time.perf_counter()
        vector = embed_query(embeddings, "¿Qué lleva un Negroni?")
        print(f"Embedding {attempt}: {time.perf_counter() - start:.2f} s | dimensión {len(vector)}")

    print(f"Modelos cargados: {_loaded_models(client)}")


if __name__ == "__main__":
    main()
