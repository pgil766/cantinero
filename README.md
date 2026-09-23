# Cantinero 🍸

Agente inteligente de **coctelería y destilados** construido con **LangChain**, **LangGraph** y **RAG**.
Responde preguntas sobre cócteles, destilados y técnicas de bar usando únicamente su base de
conocimiento, cita sus fuentes y rechaza lo que no sabe.

**Integrantes:** Pablo Gil · Emanuel Quintero

> 🚧 Proyecto en construcción. Este README se completa en la tarea T9.1 (ejecución local, despliegue,
> capturas, diagrama de arquitectura y fuentes de datos). El plan completo está en [`AGENTS.md`](AGENTS.md).

## Stack

| Capa | Tecnología |
|------|-----------|
| Backend | FastAPI (Python 3.12) |
| Agente | LangGraph + LangChain |
| LLM local | Ollama (`qwen2.5:3b`) |
| Embeddings | Sentence Transformers (`paraphrase-multilingual-MiniLM-L12-v2`) |
| Base vectorial | PostgreSQL + pgvector |
| Autenticación | Keycloak |
| Frontend | React + Vite + TypeScript |
| Despliegue | Vercel (frontend) · VM de Azure con Docker Compose (backend) |

## Estructura

Ver la sección 14 de [`AGENTS.md`](AGENTS.md).
