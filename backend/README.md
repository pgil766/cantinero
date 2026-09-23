# Backend de Cantinero (FastAPI)

API REST del agente. La arquitectura y las decisiones están en el [`AGENTS.md`](../AGENTS.md) de la raíz.

## Ejecutar en local (PowerShell)

Requisitos: Docker Desktop corriendo, `uv`, y el archivo `.env` en la raíz del repositorio (copiar `.env.example`).

```powershell
# 1. Infraestructura (desde la raíz del repositorio)
docker compose up -d postgres keycloak

# 2. Entorno de Python (desde backend/)
cd backend
uv venv --python 3.12
uv pip sync requirements.txt requirements-dev.txt

# 3. Migraciones y servidor
.\.venv\Scripts\python.exe -m scripts.migrate
.\.venv\Scripts\python.exe -m uvicorn app.main:create_app --factory --reload
```

- API: http://127.0.0.1:8000 · Documentación interactiva: http://127.0.0.1:8000/docs
- Consola de Keycloak: http://localhost:8080/auth (usuario y contraseña en `KC_BOOTSTRAP_ADMIN_*` del `.env`)

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest               # todas
.\.venv\Scripts\python.exe -m pytest -m "not integration"   # sin base de datos
```

Las pruebas de integración crean y borran una BD temporal `cantinero_test`; se omiten si PostgreSQL no está disponible.

## Dependencias

Las directas se declaran en `requirements.in` / `requirements-dev.in` y se fijan con:

```powershell
uv pip compile requirements.in -o requirements.txt --python-version 3.12
uv pip compile requirements-dev.in -o requirements-dev.txt --python-version 3.12
```

## Docker

```powershell
docker compose up -d --build backend    # aplica migraciones al iniciar y expone :8000
```
