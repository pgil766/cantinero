#!/bin/bash
# Arranca Ollama y descarga (una sola vez, quedan en el volumen) los modelos que usa Cantinero.
set -euo pipefail

ollama serve &
server_pid=$!

until ollama list >/dev/null 2>&1; do sleep 1; done

for model in "$LLM_MODEL" "$EMBEDDING_MODEL"; do
  if ollama list | awk 'NR>1 {print $1}' | grep -qx -e "$model" -e "$model:latest"; then
    echo "Modelo ya disponible: $model"
  else
    echo "Descargando modelo: $model"
    ollama pull "$model"
  fi
done

wait "$server_pid"
