# Bitácora del proyecto Cantinero

Registro de decisiones técnicas, problemas y soluciones. Alimenta las secciones 8 (modelo local),
12 (despliegue) y 14 (problemas y conclusiones) del documento técnico.

Formato de cada entrada: **fecha · tipo (Decisión / Problema / Nota) · descripción · solución o motivo**.

---

## 2026-09-23 · Decisión · Definiciones iniciales del proyecto (D1–D12)

| Decisión | Valor | Motivo |
|----------|-------|--------|
| Nombre | Cantinero | — |
| Dominio | Coctelería y destilados | Material abundante en español (IBA, Wikipedia, TheCocktailDB); datos estructurados (recetas) que prueban bien el control de alucinaciones; permite dar un uso real a la validación de intención (consumo responsable) |
| Modalidad | Pareja, sin roles fijos | — |
| Autenticación | Keycloak | Es la solución recomendada por el docente (§2.1 del enunciado) |
| Base de datos | PostgreSQL + pgvector en la VM | Recomendada en el Anexo D; Keycloak ya necesita PostgreSQL, así que un solo motor sirve para vectores, historial y Keycloak (con BD separadas). ChromaDB solo guardaría vectores y obligaría a tener otra BD para el historial |
| LLM | `qwen2.5:3b` (Ollama) | Primero se eligió `llama3.1:8b`, pero en una VM sin GPU necesitaría ~16 GB de RAM y tardaría 30–60 s por respuesta. `qwen2.5:3b` cabe en una VM de 8 GB junto a los demás servicios. `llama3.1:8b` se conserva solo como comparación local |
| Despliegue | Vercel + VM de Azure (Azure for Students) | Los planes gratuitos o baratos de Render, Railway y App Service (512 MB – 1 GB) no alcanzan para el LLM local más Keycloak. La VM está en la lista de proveedores del enunciado |
| Base de conocimiento | Por usuario (*seed* global + documentos privados) | El enunciado no exige que sea compartida |
| Multimedia (JPG/MP3/MP4) | Opcional | Se hace solo con los requisitos mínimos listos |
| Fechas | Sin cronograma | Decisión del equipo |

## 2026-09-23 · Problema · Carpeta del proyecto dentro de OneDrive

- **Qué pasó:** la carpeta del curso estaba en `OneDrive\Documentos\Universidad`. Sincronizar `node_modules` y
  `.venv` (decenas de miles de archivos) vuelve lento el equipo y genera bloqueos y conflictos.
- **Solución:** se movió toda la carpeta `Universidad` a `C:\Users\pgilm\Universidad` (447 archivos verificados
  con SHA256). El respaldo del código es GitHub.

## 2026-09-23 · Problema · Instalación de Ollama con winget

- **Qué pasó:** `winget install Ollama.Ollama` falló dos veces con `0x80072ee2` (tiempo de espera de red agotado);
  el instalador pesa ~1.5 GB.
- **Solución:** descarga directa desde `https://ollama.com/download/OllamaSetup.exe` con `curl` (reintentos y
  reanudación), verificación de la firma digital (Ollama Inc.) e instalación. Versión instalada: 0.34.3.

## 2026-09-23 · Nota · Prueba de los modelos sin RAG (evidencia para el documento técnico)

Pregunta: *"¿Qué ingredientes lleva un Negroni?"* (temperatura 0.1, sin contexto).

| Modelo | Respuesta | Correcta | Latencia (con batería) |
|--------|-----------|----------|------------------------|
| `qwen2.5:3b` | "gin, ron oscuro y un toque de azúcar… ginebra… ralladura" | ❌ **Alucinación** | 116 s (63 s de carga), 3.2 tokens/s |
| `llama3.1:8b` | "gin, Campari y sweet vermouth, 1:1:1" | ✅ | 48 s (30 s de carga), 10.9 tokens/s |

- **Conclusión:** el modelo pequeño, usado solo, inventa recetas con total seguridad. Esto justifica la
  arquitectura RAG y las capas de control de alucinaciones (sección 10 del documento técnico).
- **Rendimiento:** las cifras están deprimidas. El portátil estaba **con batería** (la RTX 3050 en estado P8) y
  descargando `llama3.1:8b` al mismo tiempo. Ollama sí usa la GPU NVIDIA (37/37 capas de qwen en la GPU; llama
  3.9 de 5.2 GB en la GPU). **Repetir las mediciones con el cargador conectado para la T6.4.**

## 2026-09-23 · Problema · Conexiones a "localhost" colgadas en Windows (Fase 1)

- **Qué pasó:** las pruebas de integración se quedaban colgadas más de 3 minutos. Un diagnóstico con
  `connect_timeout=5` mostró que conectar a `localhost:5432` tardaba 5 s y a `127.0.0.1:5432`, 0.04 s.
- **Causa:** en Windows, `localhost` resuelve primero a IPv6 (`::1`), pero Docker publica los puertos en
  `127.0.0.1` (IPv4). Cada conexión espera a que venza el intento por IPv6 antes de probar IPv4.
- **Solución:** `DATABASE_URL` y `KEYCLOAK_INTERNAL_URL` usan `127.0.0.1`. Se agregó `connect_timeout=10` al
  motor de SQLAlchemy para que un problema de red falle rápido. `KEYCLOAK_ISSUER` se mantiene con `localhost`
  porque debe coincidir con la URL que usa el navegador (será la causa de errores 401 si se cambia).

## 2026-09-23 · Decisión · Versiones de infraestructura (Fase 1)

- Keycloak **26.7.4** (`quay.io/keycloak/keycloak`) y pgvector **0.8.6 sobre PostgreSQL 17**
  (`pgvector/pgvector:0.8.6-pg17`): las últimas estables publicadas al 2026-09-23, fijadas para que el
  entorno local y la VM sean idénticos.
- Dependencias de Python fijadas con `uv pip compile` (FastAPI 0.141.1, SQLAlchemy 2.0.54, psycopg 3.3.6,
  pydantic-settings 2.15.0, pytest 9.1.1). Se usa `httpx2` porque Starlette marcó como obsoleto su
  `TestClient` con `httpx`.
- Migraciones: SQL versionado (`backend/migrations/NNN_*.sql`) con un aplicador propio de ~40 líneas en vez
  de Alembic. Es más simple, transparente y suficiente para el tamaño del proyecto.

## 2026-09-23 · Nota · Python 3.12 para el proyecto

- El equipo tiene Python 3.13 instalado, pero se usa **Python 3.12** (vía `uv`) en local y en Docker para evitar
  incompatibilidades de PyTorch y LangChain con la versión más reciente.
