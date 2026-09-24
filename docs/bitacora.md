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

## 2026-09-23 · Revisión · Revisión independiente de la Fase 1 (13 hallazgos)

Un revisor independiente (agente de IA sin el contexto de la implementación) revisó la Fase 1 y verificó cada
hallazgo ejecutando código contra el entorno. Todos se corrigieron o quedaron anotados en la tarea donde aplican:

| # | Sev. | Hallazgo | Corrección |
|---|------|----------|-----------|
| 1 | Media | El aplicador de migraciones interpretaba `%` como marcador de parámetro (`'40% vol.'` se guardaba alterado sin error) | Ejecutar el SQL con el cursor de psycopg sin parámetros; prueba con `%`, `LIKE` y `RAISE` |
| 2 | Media | El contenedor del backend recibía todo el `.env` (contraseñas de admin de Keycloak y de superusuario) | El backend recibe solo sus variables (§15.2) en `environment:` |
| 3 | Media | El backend se conectaba a Postgres como **superusuario** | Rol `cantinero_app` sin privilegios, dueño de la BD; pgvector lo crea el superusuario en el init |
| 4 | Media | Los 500 salían sin cabeceras CORS (el frontend no podría leer el mensaje) | Middleware de errores por dentro de CORS; prueba que verifica la cabecera |
| 5 | Media | En Docker, `OLLAMA_BASE_URL` y `KEYCLOAK_INTERNAL_URL` apuntaban al propio contenedor | `http://keycloak:8080/auth` y `host.docker.internal:11434` (verificado con conexiones reales) |
| 6 | Baja | Las pruebas de migraciones dependían del orden de ejecución | El *fixture* aplica las migraciones |
| 7 | Baja | Un documento `failed` bloquearía reintentar la misma subida | Índice único parcial `WHERE status <> 'failed'`; 409 ante `UniqueViolation` (T3.6) |
| 8 | Baja | HNSW + filtro por usuario puede devolver menos de `top_k` | `hnsw.iterative_scan` (anotado en T3.4 y T4.8) |
| 9 | Baja | Sin `APP_ENV`, `/docs` quedaba público | `APP_ENV` obligatoria |
| 10 | Baja | Contraseñas con caracteres especiales rompían el init | Variables de psql (`:'pw'`); contraseñas alfanuméricas documentadas |
| 11 | Baja | El healthcheck de Postgres daba "sano" durante el init | `pg_isready -h 127.0.0.1` |
| 12 | Baja | `requirements.txt` se había resuelto solo para Windows (faltaba `uvloop` para Linux) | `uv pip compile --universal` |
| 13 | Baja | Imagen de Python sin versión exacta, variables faltantes en `.env.example`, dimensión del vector sin validar | `python:3.12.14-slim`, variables agregadas, `verify_embedding_dim` en `scripts.migrate` |

Resultado: 23 pruebas en verde (antes 17). Para aplicar el cambio de roles se recreó el volumen de desarrollo
(estaba vacío: 0 documentos, solo el realm `master`).

## 2026-09-23 · Problema · Ventanas "Elegir una aplicación" en Windows

- **Qué pasó:** aparecían muchas ventanas "Elegir una aplicación" (12 en un momento), de a varias a la vez.
- **Causa:** el plugin de Warp para Claude Code ejecuta scripts `.sh` en cada evento (por ejemplo, después de
  cada herramienta). En Windows, `.sh` está asociado a `sh_auto_file`, sin programa, así que cada ejecución
  abre ese diálogo. En este equipo el plugin tampoco funciona.
- **Solución:** pendiente de decisión (desactivar el plugin o asociar `.sh` a Git Bash). No afecta al proyecto.

## 2026-09-23 · Problema y decisión · Smart App Control bloquea Sentence Transformers → embeddings de Ollama (D13)

- **Qué pasó:** al importar `sentence_transformers` en el portátil apareció
  `ImportError: DLL load failed ... Una directiva de Control de aplicaciones bloqueó este archivo`.
- **Causa:** *Smart App Control* de Windows 11 bloquea binarios sin firma o sin reputación. Bloqueó un
  módulo compilado de `scikit-learn`, dependencia de `sentence-transformers`. No es un problema del código; en
  Linux (Docker y la VM) no ocurre.
- **Opciones evaluadas:** (1) embeddings servidos por Ollama; (2) correr el backend siempre en Docker;
  (3) apagar Smart App Control, descartado porque Windows no permite volver a activarlo.
- **Decisión (D13):** **embeddings de Ollama** con `paraphrase-multilingual` (768 dimensiones), que es el modelo
  `paraphrase-multilingual-mpnet-base-v2` de Sentence Transformers servido por Ollama. El Anexo D del enunciado
  lo contempla ("Sentence Transformers o embeddings de Ollama").
- **Ventajas adicionales:** un solo servicio (Ollama) sirve LLM y embeddings; el backend deja de necesitar
  PyTorch: la imagen pasó de varios GB (estimado con torch CPU) a **~80 MB** y el backend usa menos RAM.
- **Verificación semántica:** para "¿Qué lleva un Negroni?", la similitud con un texto del Negroni fue **0.57**,
  y con textos de mezcal y sushi, **0.24 y 0.27**. Separa bien lo relevante.
- **Cambios:** migración `002_embedding_dim_768.sql` (VECTOR(384) → VECTOR(768)). `OLLAMA_KEEP_ALIVE` pasó a
  segundos enteros (1800), porque `OllamaEmbeddings` no acepta el formato `"30m"` (`ChatOllama` sí).

## 2026-09-23 · Nota · Mediciones del modelo local (T2.5)

Medido con `python -m scripts.smoke_models` (pregunta corta; portátil **conectado a corriente**):

| Escenario | LLM en frío | LLM en caliente | Velocidad | Embedding | RAM del modelo |
|-----------|-------------|-----------------|-----------|-----------|----------------|
| Nativo, **GPU** RTX 3050 6 GB | 1.5 s | 1.1 s | — | 0.01–0.05 s | qwen 2.2 GB (100% en GPU) |
| Nativo, **solo CPU** (Ryzen 7 7445HS, 12 hilos; `num_gpu=0`) | 14.9 s | 4.2 s | **11.4 tokens/s** | 0.05 s | qwen 2.2 GB (en RAM) |
| Backend **en Docker** → Ollama nativo (`host.docker.internal`) | 4.1 s | 5.1 s | — | 0.04–0.09 s | — |

- La primera medición del proyecto (116 s) estaba muy deprimida: el portátil estaba con batería y descargando
  `llama3.1:8b` a la vez.
- **Implicación para la VM (Fase 8):** la VM no tiene GPU. Con 2 vCPU se esperan 3–4 veces menos tokens/s que
  con los 12 hilos del portátil y, con el contexto largo del RAG, 40–70 s por respuesta. Probablemente convenga
  una VM de **4 vCPU**; decidirlo midiendo en la Fase 8.

## 2026-09-23 · Nota · Python 3.12 para el proyecto

- El equipo tiene Python 3.13 instalado, pero se usa **Python 3.12** (vía `uv`) en local y en Docker para evitar
  incompatibilidades de PyTorch y LangChain con la versión más reciente.
