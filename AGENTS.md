# AGENTS.md — Cantinero 🍸

## Agente inteligente de coctelería y destilados con LangChain, LangGraph y RAG

> **Lee este archivo completo antes de escribir una sola línea de código.**
> Es la fuente de verdad del proyecto: resume el enunciado oficial (`trabajo agente.pdf`), fija las
> decisiones del equipo y la arquitectura, divide el trabajo en tareas verificables y contiene el
> checklist de entrega. Si algo en el código contradice este archivo, gana este archivo (o se
> actualiza este archivo de forma explícita, dejando registro en `docs/bitacora.md`).

| | |
|---|---|
| **Proyecto** | Cantinero |
| **Integrantes** | Pablo Gil · Emanuel Quintero |
| **Dominio** | Coctelería y destilados (cócteles clásicos IBA, destilados, técnicas de bar, coctelería colombiana) |
| **Repositorio** | `cantinero` (GitHub, público) · carpeta local `C:\Users\pgilm\Universidad\Implementacion\trabajo_agentes` |
| **Stack** | FastAPI · LangGraph/LangChain · Ollama (`qwen2.5:3b`) · PostgreSQL + pgvector · Keycloak · React + Vite · Docker Compose |
| **Despliegue** | Frontend en **Vercel** · backend completo en una **VM de Azure** (Azure for Students) |

---

## Índice

0. [Cómo usar este archivo (reglas para agentes de IA)](#0-cómo-usar-este-archivo-reglas-para-agentes-de-ia)
1. [Contexto del proyecto](#1-contexto-del-proyecto)
2. [Decisiones del equipo](#2-decisiones-del-equipo)
3. [El dominio: Cantinero](#3-el-dominio-cantinero)
4. [Requisitos del enunciado (trazables)](#4-requisitos-del-enunciado-trazables)
5. [Evaluación: requisitos mínimos y rúbrica](#5-evaluación-requisitos-mínimos-y-rúbrica)
6. [Stack tecnológico](#6-stack-tecnológico)
7. [Arquitectura](#7-arquitectura)
8. [Diseño del agente LangGraph](#8-diseño-del-agente-langgraph)
9. [Control de alucinaciones](#9-control-de-alucinaciones)
10. [Diseño del backend (API, datos, seguridad)](#10-diseño-del-backend-api-datos-seguridad)
11. [Autenticación con Keycloak](#11-autenticación-con-keycloak)
12. [Diseño del frontend](#12-diseño-del-frontend)
13. [Pipeline de carga de documentos](#13-pipeline-de-carga-de-documentos)
14. [Estructura del repositorio](#14-estructura-del-repositorio)
15. [Variables de entorno](#15-variables-de-entorno)
16. [Despliegue: Vercel + VM de Azure](#16-despliegue-vercel--vm-de-azure)
17. [Plan de trabajo por fases (tareas)](#17-plan-de-trabajo-por-fases-tareas)
18. [Pruebas y evaluación del agente](#18-pruebas-y-evaluación-del-agente)
19. [Entregables: documento técnico, diapositivas y sustentación](#19-entregables-documento-técnico-diapositivas-y-sustentación)
20. [Riesgos y mitigaciones](#20-riesgos-y-mitigaciones)
21. [Entorno local de desarrollo](#21-entorno-local-de-desarrollo)
22. [CHECKLIST MAESTRO](#22-checklist-maestro)

---

## 0. Cómo usar este archivo (reglas para agentes de IA)

Estas reglas aplican a cualquier agente de IA (Claude Code, Codex, Cursor, etc.) y a los integrantes del equipo.

1. **Idioma.** Toda comunicación con el equipo, la interfaz de usuario, los mensajes del agente, los
   *prompts*, la documentación y los commits van en **español**. Los identificadores de código
   (variables, funciones, clases, rutas de la API) van en **inglés**.
2. **Trabaja por tareas.** Toma las tareas de la [sección 17](#17-plan-de-trabajo-por-fases-tareas) en orden.
   Cada tarea tiene un ID (`T3.4`) y un criterio de "hecho" (✔). No marques una tarea como hecha si no
   cumpliste su criterio **y lo verificaste ejecutándolo**.
3. **Actualiza el checklist.** Al terminar una tarea, marca `[x]` en la tarea y en la
   [sección 22](#22-checklist-maestro). Nunca marques algo que no probaste.
4. **Bitácora obligatoria.** Registra en `docs/bitacora.md` cada decisión técnica, problema encontrado
   y cómo se resolvió (fecha, qué pasó, solución). Esa bitácora alimenta las secciones 8, 12 y 14 del
   documento técnico, que exige **justificar el modelo, sus limitaciones y los problemas del despliegue**.
5. **Prohibido** construir el flujo del agente con herramientas visuales o *drag and drop* (n8n, Zapier,
   Make, Flowise, Botpress visual, Langflow o similares). El agente se construye **con código**, con
   LangChain y LangGraph. Violarlo reprueba el trabajo.
6. **Prohibido** usar como LLM del agente un modelo comercial en la nube (OpenAI, Anthropic, Gemini, etc.).
   El LLM y los embeddings corren **localmente** (Ollama y Sentence Transformers).
7. **Secretos.** Nunca subas `.env`, llaves, *tokens*, contraseñas ni el *client secret* de Keycloak al
   repositorio. Solo `.env.example` con valores de ejemplo. Antes de cada commit, revisa `git status` y
   `git diff --staged`.
8. **Commits pequeños y frecuentes**, con mensajes significativos en formato *Conventional Commits* en
   español: `feat(agent): agregar nodo de validación de contexto`. La rúbrica valora "commits frecuentes".
   **Prohibido** agregar firmas o marcas de IA en git:
   nada de `Co-Authored-By: Claude …`, "Generated with …" ni similares en commits o PRs.
9. **No inventes APIs.** LangChain, LangGraph, Keycloak y `keycloak-js` cambian seguido (nombres de
   variables de entorno, *flags*, métodos). Antes de usar una clase, función o variable, verifica la
   documentación vigente o la versión instalada. Fija versiones en `requirements.txt`, `package.json` y
   las imágenes de Docker una vez que algo funcione.
10. **Sin fechas.** El equipo decidió no trabajar con cronograma: el plan se ordena por **fases y
    prioridades**. No agregues fechas ni plazos.
11. **Responsable de la ejecución: Pablo.** Pablo lleva adelante todo el desarrollo. Emanuel figura como
    integrante en los entregables, pero ninguna tarea depende de él.
12. **Pruebas.** Toda lógica no trivial (chunking, loaders, enrutamiento del grafo, protección de endpoints,
    aislamiento entre usuarios) lleva prueba con `pytest`. Antes de dar algo por terminado, corre las pruebas.
13. **Entorno Windows.** El equipo desarrolla en Windows 11 con PowerShell. Los comandos documentados deben
    funcionar en PowerShell o indicar la alternativa con Docker. La VM de producción es Linux (Ubuntu).
14. **Tono del dominio.** Cantinero habla de alcohol: nunca promueve el consumo excesivo, no da consejos
    médicos y no atiende a menores (ver [3.4](#34-consumo-responsable-validación-de-intención-sensible)).

---

## 1. Contexto del proyecto

### 1.1 Qué hay que construir

Una **aplicación web completa** cuyo núcleo es un **agente inteligente** construido con **LangChain y
LangGraph**. El agente responde preguntas sobre **un dominio específico** (aquí: **coctelería y
destilados**) usando **exclusivamente** una base de conocimiento propia almacenada en una **base de datos
vectorial** (arquitectura **RAG**: *Retrieval Augmented Generation*).

Cada respuesta debe sustentarse en información **efectivamente recuperada** de la base vectorial y **no**
en el conocimiento paramétrico del modelo. Si no hay información suficiente, el agente **debe rechazar**
la pregunta de forma explícita.

### 1.2 Objetivo (literal del enunciado)

> Desarrollar una aplicación web que permita a un usuario autenticado interactuar con un agente
> inteligente capaz de responder preguntas fundamentadas en documentos y datos previamente cargados.

### 1.3 Componentes obligatorios

| # | Componente | Implementación en Cantinero |
|---|------------|-----------------------------|
| C1 | Backend con API protegida | FastAPI REST; **ningún endpoint** sin autenticación |
| C2 | Frontend funcional | React + Vite, interfaz tipo chatbot |
| C3 | Autenticación de usuarios | **Keycloak** (registro, login, sesión, logout) |
| C4 | Agente LangChain + LangGraph | `StateGraph` con validación de intención, recuperación, validación de contexto, generación y verificación |
| C5 | Modelo de lenguaje local | **Ollama** con `qwen2.5:3b` |
| C6 | Base de datos vectorial | **PostgreSQL + pgvector** |
| C7 | Carga de archivos | PDF, TXT, MD, CSV, DOCX (y JPG/MP3/MP4 opcionales) |
| C8 | Despliegue en la nube | **Vercel** (frontend) y **VM de Azure** (backend completo) |

### 1.4 Modalidad

En **pareja**: **Pablo Gil** y **Emanuel Quintero**. Pablo es el responsable de la ejecución del proyecto.

### 1.5 La frase de rechazo (constante del sistema)

Cuando no hay información suficiente, el agente responde **exactamente**:

```
No tengo suficiente información en mi base de conocimiento para responder esa pregunta.
```

Puede añadir: *"Si tienes un documento sobre este tema, puedes subirlo en la sección Documentos y
volver a preguntarme."* Define la frase **una sola vez** como constante (`REJECTION_MESSAGE`) en el
backend y reutilízala.

---

## 2. Decisiones del equipo

> Todas tomadas. Si alguna cambia, actualiza esta tabla **y** las secciones afectadas, y regístralo en la bitácora.

| ID | Decisión | Valor | Consecuencias |
|----|----------|-------|---------------|
| D1 | Nombre del proyecto | ✅ **Cantinero** | Repositorio `cantinero`, *realm* de Keycloak `cantinero`, marca en la UI |
| D2 | Integrantes | ✅ **Pablo Gil y Emanuel Quintero** (pareja); Pablo ejecuta el proyecto | Ambos en la portada del documento y en las diapositivas; ninguna tarea depende de Emanuel |
| D3 | Tema / dominio | ✅ **Coctelería y destilados** | Ver [sección 3](#3-el-dominio-cantinero) |
| D4 | Roles | ✅ **Sin roles fijos** | Las tareas se reparten sobre la marcha |
| D5 | Autenticación | ✅ **Keycloak** (recomendación del docente, §2.1) | Servicio extra en Docker Compose; frontend con `keycloak-js`; backend valida JWT con JWKS |
| D6 | Base de datos | ✅ **PostgreSQL + pgvector en la VM** (Docker), compartida con Keycloak en **bases de datos separadas** | Un solo motor para vectores, historial, metadatos y Keycloak; volúmenes persistentes y respaldos con `pg_dump` |
| D7 | LLM local | ✅ **`qwen2.5:3b` vía Ollama** | Cabe en una VM de 8 GB; `llama3.1:8b` solo como **comparación local** con GPU para justificar la elección |
| D8 | Despliegue | ✅ **Frontend en Vercel** · **backend en una VM de Azure** (≈ 8 GB RAM, Azure for Students) con Docker Compose | Todo el backend (API, Ollama, Postgres, Keycloak, Caddy) en la VM; túnel desde el portátil como respaldo |
| D9 | Base de conocimiento | ✅ **Por usuario** (el enunciado no exige que sea compartida) | *Seed* global de solo lectura + documentos **privados** de cada usuario; toda búsqueda filtra "global + propios" |
| D10 | Ubicación del repositorio | ✅ `C:\Users\pgilm\Universidad\Implementacion\trabajo_agentes` (**fuera de OneDrive**) | GitHub es el respaldo |
| D11 | Fechas | ✅ **Sin cronograma** | Plan por fases y prioridades |
| D12 | Formatos multimedia (JPG, JPEG, MP3, MP4) | ✅ **Opcionales** (Fase 10) | Solo cuando M1–M8 estén listos y desplegados |

---

## 3. El dominio: Cantinero

### 3.1 Propuesta

**Cantinero** es un "bartender virtual": responde preguntas sobre cócteles, destilados y técnicas de
bar, siempre fundamentado en su base de conocimiento, citando la fuente de cada respuesta y rechazando
lo que no sabe.

### 3.2 Alcance

| Dentro del alcance ✅ | Fuera del alcance ❌ |
|-----------------------|----------------------|
| Cócteles clásicos de la **IBA** (*Unforgettables*, *Contemporary Classics*, *New Era Drinks*): ingredientes, medidas, preparación, cristalería y guarnición | **Vinos** y **cervezas** (abren demasiado el tema) |
| **Destilados:** ron, tequila, mezcal, gin, vodka, whisky, brandy/cognac y pisco (origen, elaboración, tipos) | Consejos **médicos** o de **salud** |
| **Licores y modificadores:** vermut, amargos (Campari, Aperol, *bitters*), licores de café, triple sec, etc. | Precios, venta o dónde comprar |
| **Técnicas:** *shake*, *stir*, *build*, *muddle*, *layer*, *blend*; herramientas (coctelera, *jigger*, colador) | Recomendaciones a **menores de edad** |
| **Cristalería:** copa coupé, *highball*, *old fashioned*, copa martini, etc. | Cualquier tema no relacionado (recetas de comida, deportes, etc.) |
| **Historia** de cócteles y destilados famosos | — |
| **Coctelería colombiana:** aguardiente, **viche** del Pacífico, canelazo, chicha, refajo | — |

> ⚠️ **Normalización de medidas:** las fuentes mezclan **ml** y **oz**. En la base inicial, las recetas se
> guardan en **ml** con su equivalente en oz entre paréntesis (1 oz ≈ 30 ml). Documenta la convención.

### 3.3 Base de conocimiento inicial (*seed*)

Reunir en `data/seed/` (**20–40 documentos**) y citar las fuentes en el README:

| Fuente | Contenido | Formato sugerido |
|--------|-----------|------------------|
| Lista oficial de cócteles de la **IBA** (iba-world.com) | ~90 recetas oficiales | **CSV** (una fila por cóctel: nombre, categoría IBA, ingredientes con medidas, método, cristalería, guarnición) |
| **Wikipedia en español** (CC BY-SA) | Artículos de destilados, cócteles famosos, técnicas y cristalería | **Markdown** (un archivo por tema) |
| **TheCocktailDB** (API pública) | Recetas adicionales | **CSV** o JSON → CSV (revisar sus términos de uso) |
| Guías propias del equipo | Técnicas de bar, glosario, herramientas | **PDF** y **DOCX** (para probar esos formatos) |
| Coctelería colombiana | Aguardiente, canelazo, chicha, refajo | Markdown o PDF |

> 🎬 **Documento reservado para la demo:** `guia_destilados_colombianos_viche.pdf`, sobre el **viche** del
> Pacífico y su uso en coctelería. **No debe estar en el *seed***. En la sustentación se pregunta por el
> viche (→ rechazo), se sube este PDF y se repite la pregunta (→ respuesta con fuente). Verifica antes
> de la demo que ningún documento del *seed* mencione el viche.

### 3.4 Consumo responsable: validación de intención sensible

El nodo `classify_intent` distingue una categoría **`sensitive`** para preguntas de riesgo:

- Salud y medicamentos: *"¿Puedo tomar alcohol con antibióticos?"*
- Embarazo o lactancia.
- Conducción: *"¿Cuántos tragos puedo tomar si voy a manejar?"*
- Menores de edad: *"Tengo 15 años, ¿qué cóctel me recomiendas?"*
- Consumo excesivo o intoxicación.

Para estas preguntas, el agente **no consulta la base ni genera recetas**. Responde con un mensaje fijo
(`RESPONSIBLE_MESSAGE`), por ejemplo:

```
No puedo darte orientación sobre eso. Si tienes dudas sobre salud y consumo de alcohol, consulta a un
profesional de la salud. Recuerda: si vas a conducir, no bebas. 🍸 Disfruta con moderación.
```

Esto le da un uso real al paso "validar la intención" (§3.1, paso 2) y es un buen punto para la sustentación.

### 3.5 Preguntas de referencia (base del set de evaluación)

**Deben responderse (con fuente):**
- ¿Qué lleva un Negroni?
- ¿Cómo se prepara un Mojito?
- ¿Cuál es la diferencia entre el tequila y el mezcal?
- ¿Qué significa preparar un cóctel *stirred*?
- ¿Qué cócteles se sirven en copa coupé?
- ¿Qué cócteles puedo hacer con ron y limón?
- ¿Dónde se originó el Mojito?
- ¿Qué es el aguardiente?
- ¿Qué es un *bitter* y para qué se usa?

**Deben rechazarse** (con la frase de [1.5](#15-la-frase-de-rechazo-constante-del-sistema)):
- ¿Cuál es la mejor receta para preparar sushi? *(fuera del dominio, ejemplo del Anexo C)*
- ¿Qué vino marida con el salmón? *(cercano, pero fuera del alcance)*
- ¿Quién ganó el Mundial de 2014?
- ¿Qué es el viche? *(antes de subir el documento de la demo)*

**Deben activar el mensaje de consumo responsable:**
- ¿Puedo tomar alcohol si estoy tomando antibióticos?
- ¿Cuántos cócteles puedo tomar antes de manejar?

---

## 4. Requisitos del enunciado (trazables)

Cada requisito tiene un ID. Las tareas y el checklist los referencian. Las referencias `§` apuntan a
secciones del PDF original.

### 4.1 Autenticación y usuarios (§2.1)

| ID | Requisito |
|----|-----------|
| RF-AUTH-1 | El usuario puede **registrarse**. |
| RF-AUTH-2 | El usuario puede **iniciar sesión**. |
| RF-AUTH-3 | Solo usuarios **autenticados** acceden al frontend (rutas protegidas). |
| RF-AUTH-4 | Solo usuarios **autorizados** consumen la API. **Ningún endpoint** queda expuesto sin autenticación. |
| RF-AUTH-5 | La sesión se **mantiene activa** (renovación de *token*; persiste al recargar). |
| RF-AUTH-6 | El usuario puede **cerrar sesión**. |

### 4.2 Backend (§2.2)

| ID | Requisito |
|----|-----------|
| RF-BE-1 | API REST o GraphQL (Cantinero: **REST con FastAPI**). |
| RF-BE-2 | Autenticar y validar usuarios. |
| RF-BE-3 | Enviar preguntas al agente y devolver sus respuestas. |
| RF-BE-4 | Subir archivos para complementar la base de conocimiento. |
| RF-BE-5 | Procesar los documentos cargados y guardar sus embeddings en la base vectorial. |
| RF-BE-6 | Consultar el historial de conversaciones del usuario. |
| RF-BE-7 | Listar los documentos cargados y eliminarlos. |
| RF-BE-8 | Código bien estructurado: separación clara entre **controladores, servicios, configuración, lógica del agente y acceso a datos**. |

### 4.3 Frontend (§2.3)

| ID | Requisito |
|----|-----------|
| RF-FE-1 | Registrarse e iniciar sesión. |
| RF-FE-2 | Interactuar con el agente mediante una **interfaz tipo chatbot**. |
| RF-FE-3 | Enviar preguntas y visualizar las respuestas. |
| RF-FE-4 | Subir archivos para alimentar la base de conocimiento. |
| RF-FE-5 | Consultar los documentos cargados. |
| RF-FE-6 | Mostrar **mensajes de error** cuando el agente no pueda responder. |
| RF-FE-7 | Cerrar sesión. |
| RF-FE-8 | Interfaz **clara, funcional y agradable** (se permite generarla con IA). |

### 4.4 Carga y procesamiento de documentos (§2.4)

Formatos sugeridos: **PDF, TXT, Markdown, CSV, DOCX** y multimedia (**JPG, JPEG, MP4, MP3**; opcionales según D12).

| ID | Paso obligatorio del flujo |
|----|----------------------------|
| RF-DOC-1 | Recibir el archivo desde el frontend y enviarlo al backend. |
| RF-DOC-2 | Extraer el contenido del documento. |
| RF-DOC-3 | Dividir el texto en fragmentos (*chunks*). |
| RF-DOC-4 | Generar los embeddings correspondientes. |
| RF-DOC-5 | Almacenar los embeddings en la base vectorial. |
| RF-DOC-6 | Confirmar al usuario que el documento fue procesado. |

### 4.5 Agente (§3.1)

Construido **obligatoriamente con LangChain y LangGraph**, sobre una arquitectura basada en grafo.

| ID | Paso del flujo de referencia |
|----|------------------------------|
| RT-AG-1 | Recibir la pregunta del usuario. |
| RT-AG-2 | **Validar la intención** de la pregunta. |
| RT-AG-3 | Buscar información relevante en la base vectorial. |
| RT-AG-4 | **Evaluar si la información recuperada es suficiente.** |
| RT-AG-5 | Responder con base en la información encontrada. |
| RT-AG-6 | **Rechazar** la pregunta o **pedir aclaración** cuando el contexto sea insuficiente. |
| RT-AG-7 | Guardar la interacción en el historial. |
| RT-AG-8 | No inventar información; rechazo explícito con la frase de [1.5](#15-la-frase-de-rechazo-constante-del-sistema), con la opción de sugerir subir documentos. |

### 4.6 Modelo local (§3.2)

| ID | Requisito |
|----|-----------|
| RT-LLM-1 | LLM ejecutado **localmente** (Ollama: Llama 3.1, Mistral, Gemma, Phi, Qwen; o Hugging Face local). |
| RT-LLM-2 | No depender únicamente de modelos comerciales en la nube. |
| RT-LLM-3 | En el documento técnico: **qué modelo, por qué, cómo se ejecuta localmente y qué limitaciones** se encontraron. |

### 4.7 Base de datos vectorial (§3.3)

Opciones del enunciado: ChromaDB, FAISS, Qdrant, Weaviate, Milvus o **PostgreSQL con pgvector** (elegida;
también está en el Anexo D).

| ID | Capacidad obligatoria |
|----|-----------------------|
| RT-VDB-1 | Guardar los fragmentos de texto procesados. |
| RT-VDB-2 | Asociar cada fragmento con su **documento original**. |
| RT-VDB-3 | Buscar información relevante a partir de la pregunta. |
| RT-VDB-4 | Recuperar el contexto con el que el agente construye la respuesta. |

### 4.8 Control de alucinaciones (§3.4): *uno de los criterios más importantes*

Mínimo **dos** estrategias. Cantinero implementa **las seis** (ver [sección 9](#9-control-de-alucinaciones)):

| ID | Estrategia |
|----|------------|
| RT-HAL-1 | Umbral mínimo de similitud para aceptar documentos recuperados. |
| RT-HAL-2 | Verificación del contexto antes de responder. |
| RT-HAL-3 | *Prompt* que obliga a responder solo con la información recuperada. |
| RT-HAL-4 | Nodo de LangGraph dedicado a validar si el contexto es suficiente. |
| RT-HAL-5 | Respuestas explícitas de rechazo cuando no hay información. |
| RT-HAL-6 | Presentación de las fuentes o fragmentos usados para responder. |

### 4.9 Despliegue (§3.5)

| ID | Requisito |
|----|-----------|
| RT-DEP-1 | Backend y frontend desplegados con **URL pública**. |
| RT-DEP-2 | Frontend en Vercel, Netlify, GitHub Pages, Azure Static Web Apps o Firebase Hosting (Cantinero: **Vercel**). |
| RT-DEP-3 | Backend en Render, Railway, Azure App Service, AWS ECS/EC2, Google Cloud Run, Fly.io o DigitalOcean (Cantinero: **VM de Azure**). |
| RT-DEP-4 | Documentar: URL del frontend, URL del backend, **variables de entorno**, **proceso de despliegue** y **problemas encontrados**. |

### 4.10 Restricción (§4)

| ID | Restricción |
|----|-------------|
| RS-1 | Flujo principal del agente **con código** (LangChain + LangGraph). Prohibido n8n, Zapier, Make, Flowise, Botpress visual y similares. |

---

## 5. Evaluación: requisitos mínimos y rúbrica

### 5.1 Requisitos mínimos para aprobar (§6.1): **GATE ELIMINATORIO**

> Si falla **uno solo**, el trabajo **no aprueba**, sin importar la calidad del resto.
> Prioridad absoluta: estos ocho puntos deben funcionar **de extremo a extremo y desplegados** antes de
> pulir cualquier otra cosa.

| # | Requisito mínimo | Cómo se demuestra en Cantinero |
|---|------------------|--------------------------------|
| M1 | Backend y frontend funcionales | Demo en vivo contra la URL de Vercel y la API en Azure |
| M2 | Autenticación implementada | Registro y login en Keycloak, ruta protegida y 401 en la API sin *token* |
| M3 | Agente construido con LangChain y LangGraph | `backend/app/agents/graph.py` y diagrama exportado del grafo |
| M4 | Modelo local en funcionamiento | Ollama con `qwen2.5:3b` corriendo en la VM (`docker ps`) |
| M5 | Base vectorial integrada y carga de documentos operativa | Subir un archivo y preguntar sobre él |
| M6 | Respuestas fundamentadas en el contexto recuperado | Respuesta con fuentes visibles |
| M7 | Rechazo explícito de preguntas sin información suficiente | "¿Receta de sushi?" → rechazo |
| M8 | Despliegue en la nube y repositorio documentado | URL públicas y README completo |

### 5.2 Rúbrica (§6.2) y dónde se gana cada punto

| Criterio | Peso | Evidencia principal | Qué garantiza el puntaje |
|----------|-----:|---------------------|--------------------------|
| Uso correcto de LangChain y LangGraph | **15%** | Repositorio | `StateGraph` con nodos claros, aristas condicionales, estado tipado, diagrama exportado y pruebas del enrutamiento |
| Backend y API | **15%** | Repositorio | Capas separadas, validación con Pydantic, manejo de errores, endpoints protegidos y OpenAPI |
| Arquitectura general del sistema | 10% | Documento técnico | Diagrama claro, justificación de cada pieza y flujo de datos |
| Autenticación y seguridad | 10% | Demostración | Keycloak (registro, login, logout, *refresh*), 401/403 visibles, aislamiento entre usuarios y CORS restringido |
| Base de datos vectorial y RAG | 10% | Repositorio | pgvector, metadatos por fragmento, búsqueda con puntaje, umbral calibrado y filtro por usuario |
| Control de alucinaciones | 10% | Demostración | Las 6 estrategias y rechazos visibles en vivo |
| Modelo local (Ollama o HF) | 8% | Documento técnico | Justificación de Qwen 2.5 3B, comparación medida con Llama 3.1 8B y limitaciones |
| Documentación y sustentación | 8% | Documento y diapositivas | 14 secciones del documento, 8 a 12 diapositivas y demo de 7 a 10 minutos |
| Carga y procesamiento de documentos | 7% | Demostración | Varios formatos, estado de procesamiento, confirmación y pregunta sobre lo cargado |
| Frontend e interfaz de usuario | 5% | Demostración | Chat usable, fuentes, estados de carga, errores y validación de formularios |
| Despliegue en la nube | 2% | URL pública | Ambas URL funcionando el día de la sustentación |

> **Nota estratégica:** el despliegue vale solo el 2% de la rúbrica, **pero es requisito mínimo (M8)**.
> Si falla, se reprueba. Con Keycloak, Ollama y Postgres en la VM hay varias piezas que pueden fallar,
> así que se despliega un **esqueleto temprano** (T8.1), no al final.

### 5.3 Criterios de calidad esperados (§6.3)

- [ ] Código limpio y organizado, con separación clara entre frontend, backend y agente.
- [ ] Uso adecuado de variables de entorno (nada *hardcodeado*).
- [ ] Manejo de errores y **validación de formularios**.
- [ ] Seguridad en los endpoints.
- [ ] README claro y **commits frecuentes**.
- [ ] Interfaz usable y respuestas coherentes del agente.
- [ ] Evidencia clara del uso de LangGraph y despliegue funcional.

---

## 6. Stack tecnológico

| Capa | Tecnología | Por qué |
|------|-----------|---------|
| Backend | **FastAPI** (Python **3.12**) | Recomendado en el Anexo D; mismo lenguaje que LangChain y LangGraph; OpenAPI automático |
| Agente | **LangGraph** + **LangChain** (`langchain-core`, `langchain-ollama`, `langchain-postgres`, `langchain-text-splitters`, `langchain-community`) | Obligatorio (§3.1) |
| LLM local | **Ollama** + **`qwen2.5:3b`** | Qwen está en la lista del docente (§3.2); buen español; ~2 GB de RAM, cabe en la VM |
| Embeddings | **Sentence Transformers**: `paraphrase-multilingual-MiniLM-L12-v2` (384 dim) | Recomendado en el Anexo D; multilingüe (dominio en español); liviano en CPU |
| Base vectorial y datos | **PostgreSQL 17 + pgvector 0.8.6** (imagen `pgvector/pgvector:0.8.6-pg17`) | Anexo D; un solo motor para vectores, historial, documentos y Keycloak |
| Autenticación | **Keycloak** (imagen oficial `quay.io/keycloak/keycloak`) | Recomendado por el docente (§2.1 y Anexo D); OIDC estándar |
| Frontend | **React + Vite + TypeScript** + Tailwind CSS + `keycloak-js` | Anexo D (React); rápido de construir |
| Reverse proxy / HTTPS | **Caddy** | Certificados HTTPS automáticos (necesarios para Vercel y `keycloak-js`) |
| Contenedores | **Docker** + **Docker Compose** | Anexo A; el mismo *stack* en local y en la VM |
| Despliegue | **Vercel** (frontend) + **VM de Azure** (backend completo) | D8 |
| Pruebas | `pytest`, `httpx` (TestClient); Vitest opcional en el frontend | Calidad y evidencia |

### 6.1 Modelo local: decisión y justificación

**Modelo de producción:** `qwen2.5:3b` (Ollama), fijado en `LLM_MODEL`.

| Modelo | Uso en el proyecto | RAM aprox. | Motivo |
|--------|--------------------|-----------|--------|
| **`qwen2.5:3b`** | **Producción (VM) y desarrollo** | ~2 GB | Cabe en la VM de 8 GB junto a Keycloak, Postgres y el backend; buen español; sigue instrucciones y JSON aceptablemente |
| `llama3.1:8b` | **Solo comparación local** (portátil con RTX 3050 6 GB) | ~5 GB | Es el primero que nombra el docente; referencia de calidad. En la VM sin GPU necesitaría 16 GB y respondería en 30–60 s |

**Tarea obligatoria (T6.4):** comparar `qwen2.5:3b` con `llama3.1:8b` usando el mismo set de evaluación
([sección 18](#18-pruebas-y-evaluación-del-agente)) y registrar calidad, rechazos correctos, latencia y RAM.
Esta tabla **es** la justificación del 8% de "Modelo local": qué modelo, por qué, cómo se ejecuta y limitaciones.

**Limitaciones esperadas que hay que medir y documentar:** latencia en CPU (≈ 10–20 s por respuesta en la
VM), menor capacidad de razonamiento que un modelo de 8B y fallos ocasionales al producir JSON (mitigados
con parseo defensivo).

> ⚠️ **Regla crítica de embeddings:** el **mismo modelo** debe usarse para indexar y para consultar. La
> dimensión queda fija en la columna `vector(384)`. **Cambiar el modelo de embeddings obliga a reindexar
> todo** (`scripts/reindex.py`).

> ⚠️ Instala **PyTorch solo CPU** en la imagen Docker del backend (índice
> `https://download.pytorch.org/whl/cpu`); si no, la imagen pesa varios GB extra por CUDA.

---

## 7. Arquitectura

### 7.1 Diagrama general

```mermaid
flowchart TD
    U[Usuario] --> FE[Frontend React/Vite<br/>Vercel]
    FE -- "OIDC: login / registro / refresh<br/>(Authorization Code + PKCE)" --> CADDY
    FE -- "HTTPS + Bearer JWT" --> CADDY

    subgraph VM [VM de Azure · Docker Compose]
        CADDY[Caddy<br/>HTTPS + reverse proxy]
        CADDY -- "/auth/*" --> KC[Keycloak<br/>realm cantinero]
        CADDY -- "/api/*" --> API[Backend FastAPI]

        subgraph BACKEND [Backend]
            API --> SEC[Seguridad<br/>verifica JWT con JWKS]
            SEC --> CTRL[Controllers]
            CTRL --> SVC[Services]
            SVC --> ING[Ingesta<br/>extraer → chunk → embed → guardar]
            SVC --> AG[Agente LangGraph]
            AG --> RET[Retriever pgvector<br/>umbral + filtro por usuario]
            ING --> EMB[Sentence Transformers<br/>embeddings locales]
            RET --> EMB
        end

        AG --> OLL[Ollama<br/>qwen2.5:3b]
        SEC -. "JWKS" .-> KC
        PG[(PostgreSQL + pgvector<br/>BD cantinero · BD keycloak)]
        RET --> PG
        ING --> PG
        AG -- "guardar historial" --> PG
        KC --> PG
    end
```

Corresponde al **Anexo B** del enunciado: Usuario → Frontend → API protegida (autenticación con Keycloak,
usuarios, carga, procesamiento, agente LangGraph) → modelo local → base vectorial.

### 7.2 Flujo de una pregunta

1. El usuario inicia sesión en Keycloak (redirección OIDC con PKCE); `keycloak-js` obtiene el *access token*.
2. El frontend envía `POST /api/v1/chat` con `Authorization: Bearer <jwt>` (renovando el *token* antes si está por vencer).
3. La dependencia `get_current_user` valida el JWT (firma con JWKS de Keycloak, `exp`, `iss`, `aud`) y devuelve 401 si falla.
4. El controlador delega en `ChatService`, que carga los últimos N mensajes de la conversación e invoca el grafo con el `user_id`.
5. El grafo ejecuta: intención → (consumo responsable / saludo / aclaración) o (reformulación → recuperación filtrada por usuario → validación → generación → verificación) → rechazo si falla → guardado.
6. La API responde `{ answer, status, sources[], conversation_id, message_id }`.
7. El frontend muestra la respuesta y sus **fuentes**. Si `status = rejected`, muestra un aviso con el botón "Subir documentos".

### 7.3 Separación de capas en el backend (RF-BE-8)

| Capa | Carpeta | Responsabilidad | NO debe |
|------|---------|-----------------|---------|
| Configuración | `app/core/config.py` | Leer y validar variables de entorno (`pydantic-settings`) | Tener lógica de negocio |
| Seguridad | `app/core/security.py` | Verificar JWT de Keycloak y exponer `get_current_user` | Consultar la BD de documentos |
| Controladores | `app/controllers/` | Rutas HTTP, validación de entrada y salida, códigos HTTP | Contener lógica del agente o SQL |
| Servicios | `app/services/` | Casos de uso: chat, documentos, historial | Conocer detalles HTTP |
| Agente | `app/agents/` | Estado, nodos, *prompts* y construcción del grafo | Conocer FastAPI |
| Vector store | `app/vectorstore/` | Embeddings, *retriever* con filtro por usuario, inserción y borrado de fragmentos | Conocer HTTP o el grafo |
| Acceso a datos | `app/db/` | Modelos, sesión y repositorios | Lógica de negocio |
| Esquemas | `app/schemas/` | Modelos Pydantic de *request* y *response* | — |

---

## 8. Diseño del agente LangGraph

### 8.1 Estado del grafo

```python
# app/agents/state.py  (esquema de referencia; ajustar a la API vigente de LangGraph)
from typing import Literal, TypedDict

Intent = Literal["greeting", "domain_question", "sensitive", "out_of_domain", "ambiguous"]
Status = Literal["answered", "rejected", "clarify", "greeting", "responsible"]

class RetrievedChunk(TypedDict):
    chunk_id: str
    document_id: str
    filename: str
    is_global: bool       # True = seed; False = documento privado del usuario
    content: str
    score: float          # similitud normalizada 0..1 (1 = idéntico)
    page: int | None

class AgentState(TypedDict, total=False):
    # entrada
    question: str
    user_id: str                    # 'sub' del JWT de Keycloak; filtra la búsqueda
    conversation_id: str
    chat_history: list[dict]        # últimos N mensajes {role, content}
    # intermedios
    intent: Intent
    search_query: str               # pregunta reformulada (autocontenida)
    retrieved: list[RetrievedChunk] # tras umbral de similitud
    context_sufficient: bool
    grounded: bool
    # salida
    answer: str
    status: Status
    sources: list[RetrievedChunk]
```

### 8.2 Nodos (mapeo al flujo de §3.1 y al Anexo B)

| Nodo | Paso §3.1 | Anexo B | Qué hace |
|------|-----------|---------|----------|
| `receive_question` | 1 | Nodo 1 | Normaliza la pregunta (recorta espacios, valida longitud, no vacía) e inicializa el estado |
| `classify_intent` | 2 | — | Clasifica: `greeting`, `domain_question`, `sensitive`, `out_of_domain` o `ambiguous`. LLM con salida JSON más reglas por palabras clave para `sensitive` (manejar, embarazo, medicamento, menor, "tengo 15 años"…). Si el JSON falla → `domain_question` (los filtros siguientes deciden) |
| `responsible_notice` | 2/6 | — | Para `sensitive`: devuelve `RESPONSIBLE_MESSAGE` sin consultar la base ([3.4](#34-consumo-responsable-validación-de-intención-sensible)) |
| `greet` | — | — | Saludo breve que explica qué sabe Cantinero (no consulta la base) |
| `ask_clarification` | 6 | Nodo 5 | Para `ambiguous`: pide al usuario precisar la pregunta |
| `rewrite_query` | 2–3 | — | Si hay historial, reformula la pregunta como **autocontenida** ("¿y con qué vaso se sirve?" → "¿Con qué vaso se sirve el Negroni?") |
| `retrieve` | 3 | Nodo 2 | Búsqueda por similitud en pgvector, **filtrada a "global + documentos del usuario"**, `top_k`; normaliza puntajes y **descarta** los que están bajo `SIMILARITY_THRESHOLD` (RT-HAL-1) |
| `grade_context` | 4 | Nodo 3 | **Nodo validador** (RT-HAL-4): sin fragmentos → insuficiente; con fragmentos → el LLM juzga "¿este contexto permite responder? sí/no" (RT-HAL-2) |
| `generate_answer` | 5 | Nodo 4 | Genera la respuesta con el *prompt* estricto (RT-HAL-3), solo con el contexto, citando `[1]`, `[2]` |
| `verify_answer` | 5 | — | Revisa que la respuesta esté soportada por el contexto (en especial **medidas y cantidades**); si no lo está → `reject` |
| `reject` | 6 | Nodo 5 | Devuelve `REJECTION_MESSAGE` y la sugerencia de subir documentos (RT-HAL-5) |
| `save_history` | 7 | Nodo 6 | Persiste pregunta, respuesta, estado y fuentes en `messages`. **Todas** las ramas terminan aquí |

### 8.3 Grafo

```mermaid
flowchart TD
    START([START]) --> receive_question
    receive_question --> classify_intent
    classify_intent -- greeting --> greet
    classify_intent -- sensitive --> responsible_notice
    classify_intent -- ambiguous --> ask_clarification
    classify_intent -- out_of_domain --> reject
    classify_intent -- domain_question --> rewrite_query
    rewrite_query --> retrieve
    retrieve --> grade_context
    grade_context -- insuficiente --> reject
    grade_context -- suficiente --> generate_answer
    generate_answer --> verify_answer
    verify_answer -- no soportada --> reject
    verify_answer -- soportada --> save_history
    greet --> save_history
    responsible_notice --> save_history
    ask_clarification --> save_history
    reject --> save_history
    save_history --> END([END])
```

> ⚠️ **Cuidado con `out_of_domain`:** un modelo de 3B puede clasificar mal una pregunta válida. Alternativa
> más segura: que `out_of_domain` también pase por `retrieve` (si hay contexto sobre el umbral, se sigue;
> si no, se rechaza). Decídelo con la evaluación (T6.3) y regístralo en la bitácora.
> **`sensitive` nunca pasa a recuperación**, aunque haya contexto.

### 8.4 Reglas de implementación

- Construye el grafo con `StateGraph(AgentState)`, `add_node`, `add_edge`, `add_conditional_edges` y
  `compile()`. Cada nodo es una **función** que recibe el estado y devuelve un `dict` parcial.
- **Inyecta las dependencias** al construir el grafo (`build_graph(llm, retriever, history_repo)`), para
  poder **probar los nodos con dobles de prueba**.
- **Exporta el diagrama** del grafo compilado (`graph.get_graph().draw_mermaid()` o PNG) a
  `docs/grafo_langgraph.png` (o `.md`). Es evidencia directa del 15% de LangGraph y sirve para la sustentación.
- Los *prompts* viven en `app/agents/prompts.py`, en español y comentados.
- `temperature` baja (0 a 0.2) para respuestas factuales.
- Salidas estructuradas (intención, veredictos): pide JSON (`format="json"` en `ChatOllama`) y **parsea de
  forma defensiva** (try/except, valores por defecto conservadores).
- Historial que entra al grafo: los últimos `CHAT_HISTORY_TURNS` mensajes.
- **Log por pregunta:** intención, número de fragmentos, puntajes, veredictos y latencia por nodo.

### 8.5 *Prompts* de referencia

**Sistema para la generación (RT-HAL-3):**

```text
Eres Cantinero, un bartender experto en coctelería y destilados.
Respondes ÚNICAMENTE con la información del CONTEXTO.
Reglas:
1. Si el CONTEXTO no contiene la respuesta, responde exactamente:
   "No tengo suficiente información en mi base de conocimiento para responder esa pregunta."
2. No uses conocimiento propio ni supongas datos que no aparezcan en el CONTEXTO.
3. Copia las medidas y cantidades EXACTAMENTE como aparecen en el CONTEXTO; nunca las inventes ni las conviertas por tu cuenta.
4. Cita las fuentes con [n] según el número del fragmento usado.
5. Responde en español, de forma clara y concisa. Para recetas usa: ingredientes (lista), preparación, cristalería y guarnición.
6. Nunca promuevas el consumo excesivo de alcohol.

CONTEXTO:
[1] (archivo: {filename}, pág. {page}) {content}
[2] ...

PREGUNTA: {question}
```

**Clasificador de intención:** devuelve JSON `{"intent": "greeting|domain_question|sensitive|out_of_domain|ambiguous"}`
con ejemplos (*few-shot*) de cada categoría del dominio.

**Validador de contexto (RT-HAL-2 y RT-HAL-4):** devuelve JSON `{"sufficient": true|false, "reason": "..."}`.

**Verificador de respuesta:** devuelve JSON `{"grounded": true|false}`, que indica si cada afirmación y cada
medida de la respuesta aparece en el contexto.

---

## 9. Control de alucinaciones

Criterio del **10%** y de los requisitos mínimos M6 y M7. Se implementan las **seis** estrategias, en capas:

| Capa | Estrategia | ID | Dónde | Cómo se demuestra |
|------|-----------|----|-------|-------------------|
| 1 | Umbral mínimo de similitud | RT-HAL-1 | `retrieve` y `vectorstore/retriever.py` | Log de puntajes; pregunta fuera de tema sin fragmentos sobre el umbral |
| 2 | Nodo validador de contexto en LangGraph | RT-HAL-4 | `grade_context` | Diagrama del grafo y rama `insuficiente` → `reject` |
| 3 | Verificación del contexto antes de responder | RT-HAL-2 | `grade_context` (juicio del LLM) | Log del veredicto |
| 4 | *Prompt* restrictivo | RT-HAL-3 | `prompts.py` | Mostrar el *prompt* en la revisión de código |
| 5 | Rechazo explícito | RT-HAL-5 | `reject` y `REJECTION_MESSAGE` | Demo: "¿receta de sushi?" → rechazo |
| 6 | Fuentes visibles | RT-HAL-6 | Respuesta de la API y UI | Tarjetas de fuente bajo cada respuesta |
| extra | Verificación posgeneración (medidas) | — | `verify_answer` | Rechazo cuando la respuesta no está soportada |
| extra | Validación de intención sensible | — | `classify_intent` → `responsible_notice` | Demo: "¿alcohol con antibióticos?" |

### 9.1 Calibración del umbral (obligatoria, T5.4)

- pgvector con distancia coseno (`<=>`) devuelve **distancia**: `similitud = 1 − distancia`. Cada
  integración de LangChain reporta el puntaje distinto (distancia vs. relevancia). **Normaliza
  explícitamente** a similitud 0..1 en un único lugar y pruébalo.
- Procedimiento: correr el set de evaluación, registrar la similitud máxima de las preguntas **dentro** y
  **fuera** del dominio, y fijar el umbral entre ambas distribuciones. Documenta la tabla o gráfica en el
  documento técnico (sección 10).
- Valor inicial orientativo para MiniLM multilingüe: 0.35–0.50. **No lo des por bueno sin medir.**
- Caso difícil del dominio: preguntas cercanas pero fuera del alcance ("¿qué vino marida con salmón?")
  pueden tener similitud moderada con textos de destilados. El validador (capa 2) es quien las debe atajar.

---

## 10. Diseño del backend (API, datos, seguridad)

### 10.1 Endpoints (todos con prefijo `/api/v1` y **todos protegidos**)

| Método | Ruta | Descripción | Requisito |
|--------|------|-------------|-----------|
| GET | `/auth/me` | Valida el *token* y devuelve el perfil (`sub`, email, nombre, roles) | RF-BE-2 |
| POST | `/chat` | Body `{question, conversation_id?}` → `{answer, status, sources[], conversation_id, message_id}` | RF-BE-3 |
| GET | `/conversations` | Lista las conversaciones **del usuario** | RF-BE-6 |
| GET | `/conversations/{id}` | Mensajes de una conversación (404 si no es del usuario) | RF-BE-6 |
| DELETE | `/conversations/{id}` | Elimina una conversación propia (opcional) | — |
| POST | `/documents` | `multipart/form-data` → procesa y responde `{id, filename, status, chunk_count}`. El documento queda **privado** del usuario | RF-BE-4, RF-BE-5, RF-DOC-* |
| GET | `/documents` | Lista los documentos **globales** (solo lectura) y los **propios** del usuario, con la marca `is_global` | RF-BE-7 |
| GET | `/documents/{id}` | Detalle y estado (404 si no es global ni propio) | RF-DOC-6 |
| DELETE | `/documents/{id}` | Elimina un documento **propio** y sus fragmentos. Global → 403; ajeno → 404 | RF-BE-7 |

- Registro, login y logout ocurren en **Keycloak** (páginas de Keycloak mediante redirección OIDC). El
  backend **valida** los *tokens* (RF-BE-2).
- **Health check:** `GET /health` **sin datos** (solo `{"status":"ok"}`), documentado como **excepción
  justificada** (lo necesitan Docker y Caddy para sus *healthchecks*). Alternativa: usar el *healthcheck*
  de Docker **dentro** de la red interna y no publicarlo en Caddy. **Decidir y documentar (T4.9).**
- **Swagger/OpenAPI** (`/docs`): en producción, desactívalo o déjalo accesible solo con *token*. No debe
  permitir consumir endpoints sin autenticación.
- Errores uniformes: `{"detail": "...", "code": "..."}` con 400/401/403/404/409/413/415/422/500/503.
  Si Ollama no responde: **503** con mensaje claro (el frontend lo muestra, RF-FE-6).

### 10.2 Modelo de datos (PostgreSQL, base de datos `cantinero`)

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  filename      TEXT NOT NULL,
  mime_type     TEXT NOT NULL,
  size_bytes    BIGINT NOT NULL,
  sha256        TEXT NOT NULL,
  is_global     BOOLEAN NOT NULL DEFAULT FALSE,   -- TRUE = seed (solo lectura)
  owner_id      TEXT,                              -- 'sub' de Keycloak; NULL si is_global
  status        TEXT NOT NULL DEFAULT 'processing', -- processing | ready | failed
  error         TEXT,
  chunk_count   INT DEFAULT 0,
  created_at    TIMESTAMPTZ DEFAULT now(),
  CHECK ((is_global AND owner_id IS NULL) OR (NOT is_global AND owner_id IS NOT NULL))
);
-- Evita duplicados por usuario (y en el seed)
CREATE UNIQUE INDEX uq_documents_owner_sha ON documents (COALESCE(owner_id, 'GLOBAL'), sha256);

CREATE TABLE chunks (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id   UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,  -- RT-VDB-2
  chunk_index   INT NOT NULL,
  content       TEXT NOT NULL,                                             -- RT-VDB-1
  metadata      JSONB NOT NULL DEFAULT '{}',  -- página, nombre del cóctel, sección, etc.
  embedding     VECTOR(384) NOT NULL
);
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON chunks (document_id);

CREATE TABLE conversations (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     TEXT NOT NULL,                  -- 'sub' de Keycloak
  title       TEXT,
  created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE messages (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id  UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role             TEXT NOT NULL,             -- user | assistant
  content          TEXT NOT NULL,
  status           TEXT,                      -- answered | rejected | clarify | greeting | responsible
  sources          JSONB DEFAULT '[]',
  created_at       TIMESTAMPTZ DEFAULT now()
);
```

**Consulta de recuperación (filtro por usuario, D9):**

```sql
SELECT c.id, c.content, c.metadata, d.id AS document_id, d.filename, d.is_global,
       1 - (c.embedding <=> :query_embedding) AS similarity
FROM chunks c
JOIN documents d ON d.id = c.document_id
WHERE d.status = 'ready'
  AND (d.is_global OR d.owner_id = :user_id)
ORDER BY c.embedding <=> :query_embedding
LIMIT :top_k;
```

- Se recomienda SQL propio con pgvector (control total del filtro y del puntaje). Si se usa `PGVector` de
  `langchain-postgres`, guarda `document_id`, `owner_id` e `is_global` en los metadatos de cada fragmento y
  filtra por ellos; **prueba el aislamiento** (T4.8).
- Migraciones: scripts SQL versionados en `backend/migrations/` (o Alembic). Nada de crear tablas "a mano".

### 10.3 Seguridad (10% de la rúbrica)

- [ ] Dependencia `get_current_user` aplicada a **todos** los routers (`dependencies=[Depends(...)]`), no endpoint por endpoint.
- [ ] Verificación completa del JWT de Keycloak: firma RS256 con la **JWKS** del *realm* (con caché de llaves), `exp`, `iss` y `aud` (ver [11.4](#114-validación-en-el-backend)).
- [ ] Autorización por recurso: conversaciones y documentos filtrados por `sub`; 404 para recursos ajenos; 403 al intentar borrar documentos globales.
- [ ] Aislamiento en la recuperación: la búsqueda **nunca** devuelve fragmentos privados de otro usuario (prueba T4.8).
- [ ] CORS restringido a la URL de Vercel y a `http://localhost:5173` (`CORS_ORIGINS`), sin `*`.
- [ ] Subida de archivos: lista blanca de extensiones **y** MIME, tamaño máximo (`MAX_UPLOAD_MB`), nombre saneado y archivo temporal que se limpia.
- [ ] Consola de administración de Keycloak protegida (contraseña fuerte; idealmente no publicar `/auth/admin` en Caddy o restringirla por IP).
- [ ] Postgres, Ollama y Keycloak **no** expuestos directamente a internet: solo Caddy (80/443).
- [ ] Rate limiting básico en `/chat` y `/documents` (opcional, suma en seguridad).
- [ ] Sin secretos en el código ni en el repositorio.

---

## 11. Autenticación con Keycloak

### 11.1 Configuración del *realm* (como código)

- *Realm* **`cantinero`**, **exportado a JSON** y versionado en `keycloak/realm-cantinero.json`. Keycloak
  lo importa al iniciar (opción `--import-realm`, verificar en la documentación vigente). Así la
  configuración es reproducible en local y en la VM, y no se pierde si se recrea el contenedor.
- **Registro de usuarios habilitado** (*User registration* ON) → cubre RF-AUTH-1 y RF-FE-1.
- Login con email; **verificación de email desactivada** (no hay SMTP; evita bloquear la demo).
- Política de contraseñas (por ejemplo, mínimo 8 caracteres), que es validación de formulario del lado de Keycloak.
- Duración de sesión y *tokens*: *access token* corto (5–15 min) y *SSO session* de algunas horas; el frontend
  renueva el *token* (RF-AUTH-5).
- Idioma de las pantallas de Keycloak: **español** (*Internationalization* ON, *default locale* `es`).
- Opcional (Fase 10): tema visual de Keycloak con la marca Cantinero.

### 11.2 *Clients*

| Client | Tipo | Configuración |
|--------|------|---------------|
| `cantinero-frontend` | **Público** (sin *secret*) | *Standard flow* (Authorization Code) + **PKCE S256**; *Valid redirect URIs*: `http://localhost:5173/*` y `https://<app>.vercel.app/*`; *Web origins*: los mismos orígenes; *Post logout redirect URIs* iguales |
| `cantinero-api` | *Bearer-only* / sin flujos | Representa la API. Sirve como **audiencia** de los *tokens* |

**Mapper de audiencia:** por defecto, el *access token* de Keycloak trae `aud: "account"`. Agrega un
*Audience mapper* (en un *client scope* dedicado asignado a `cantinero-frontend`) que incluya
`cantinero-api` en `aud`, y valida esa audiencia en el backend.

### 11.3 Frontend con `keycloak-js`

- `keycloak.init({ onLoad: 'check-sso', pkceMethod: 'S256' })`. Las rutas protegidas llaman a
  `keycloak.login()` si no hay sesión.
- Botón **"Registrarse"** → `keycloak.register()`; **"Iniciar sesión"** → `keycloak.login()`;
  **"Cerrar sesión"** → `keycloak.logout({ redirectUri })`.
- Antes de cada llamada a la API: `await keycloak.updateToken(30)` para renovar si vence en menos de 30 s.
- ⚠️ PKCE usa Web Crypto, que **solo funciona en contextos seguros** (HTTPS o `localhost`). Keycloak
  en la VM **debe** servirse por HTTPS.

### 11.4 Validación en el backend

- JWKS: `{KEYCLOAK_INTERNAL_URL}/realms/cantinero/protocol/openid-connect/certs`, con caché (por ejemplo,
  `PyJWKClient` de PyJWT) y refresco si llega un `kid` desconocido.
- ⚠️ **Trampa clásica del emisor (`iss`):** el `iss` del *token* es la URL **pública** de Keycloak
  (`https://<dominio>/auth/realms/cantinero`), aunque el backend descargue la JWKS por la red interna de
  Docker (`http://keycloak:8080/auth/...`). Por eso hay dos variables: `KEYCLOAK_ISSUER` (pública, para
  validar `iss`) y `KEYCLOAK_INTERNAL_URL` (para descargar la JWKS). Configura `KC_HOSTNAME` para que el
  emisor sea estable.
- `get_current_user` devuelve `{sub, email, name, roles}`. `sub` es el `user_id` y el `owner_id` en la BD.

### 11.5 Keycloak detrás de Caddy

- Keycloak se publica en la **ruta** `/auth` del mismo dominio (`KC_HTTP_RELATIVE_PATH=/auth`), con modo
  producción (`start`), `KC_HOSTNAME` = URL pública, cabeceras de *proxy* habilitadas (`KC_PROXY_HEADERS=xforwarded`)
  y HTTP interno habilitado solo dentro de la red de Docker. **Verificar nombres exactos de las opciones en la
  documentación de la versión usada** (cambian entre versiones mayores).
- Base de datos de Keycloak: `KC_DB=postgres`, apuntando a la BD **`keycloak`** del mismo servidor Postgres.
- RAM de Keycloak: ≈ 0.7–1 GB. Tenerlo en cuenta en el tamaño de la VM.

---

## 12. Diseño del frontend

### 12.1 Rutas

| Ruta | Acceso | Contenido |
|------|--------|-----------|
| `/` | pública | Portada de Cantinero: qué hace, aviso de consumo responsable y botones **Iniciar sesión** / **Registrarse** (redirigen a Keycloak) |
| `/chat` y `/chat/:conversationId` | **protegida** | Barra lateral de conversaciones, área de mensajes, caja de entrada y fuentes |
| `/documents` | **protegida** | Zona de subida (arrastrar y soltar), lista de documentos (etiqueta **Base** o **Mío**), borrar los propios |
| `*` | — | Redirige a `/chat` si hay sesión y a `/` si no |

### 12.2 Requisitos de UX (para el 5% y la demo)

- [ ] `ProtectedRoute` → sin sesión, redirige a Keycloak (RF-AUTH-3).
- [ ] La sesión persiste al recargar (`check-sso`) y el *token* se renueva automáticamente (RF-AUTH-5).
- [ ] Botón **Cerrar sesión** siempre visible, con el nombre del usuario (RF-FE-7).
- [ ] Cliente HTTP centralizado (`src/api/client.ts`) que renueva y adjunta el *token*; ante un 401, fuerza un nuevo login.
- [ ] Chat: burbujas usuario/Cantinero, *markdown* (listas de ingredientes), indicador "Cantinero está preparando tu respuesta…" (las respuestas tardan 10–20 s en CPU), *scroll* automático y Enter para enviar.
- [ ] **Validación de formularios** propios: pregunta no vacía y con largo máximo; subida con tipo y tamaño validados antes de enviar.
- [ ] **Fuentes** bajo cada respuesta: archivo, etiqueta Base/Mío y fragmento expandible (RT-HAL-6).
- [ ] Respuesta **rechazada**: estilo de aviso más botón "Subir documentos" (RF-FE-6).
- [ ] Respuesta de **consumo responsable**: estilo propio (informativo, no de error).
- [ ] Errores de red o servidor (503 si el modelo no está disponible) con mensaje claro, sin pantallas en blanco (RF-FE-6).
- [ ] Subida: progreso o estado y confirmación "Documento procesado: N fragmentos" (RF-DOC-6).
- [ ] Estética de bar: tema oscuro con acentos ámbar o cobre, *responsive* (Tailwind). Se permite generar la UI con IA (§2.3).
- [ ] Pie de página: "Disfruta con moderación · Contenido para mayores de edad".
- [ ] `vercel.json` con *rewrite* SPA (todas las rutas → `index.html`).

---

## 13. Pipeline de carga de documentos

```mermaid
flowchart LR
    A[Frontend: seleccionar archivo] --> B[POST /documents multipart + JWT]
    B --> C{Validar extensión, MIME,<br/>tamaño y duplicado sha256<br/>del mismo usuario}
    C -- inválido --> X[4xx con mensaje]
    C -- ok --> D[Extraer texto por tipo]
    D --> E[Limpiar y normalizar]
    E --> F[Dividir en fragmentos<br/>con conciencia de estructura]
    F --> G[Embeddings locales]
    G --> H[Insertar fragmentos en pgvector<br/>owner_id = sub del usuario]
    H --> I[status = ready, chunk_count]
    I --> J[Respuesta: documento procesado]
```

### 13.1 Extractores por formato

| Formato | Extractor sugerido | Notas |
|---------|--------------------|-------|
| PDF | `pypdf` / `PyPDFLoader` | Página en los metadatos; PDF escaneado sin texto → error claro (u OCR en la Fase 10) |
| TXT, MD | Lectura UTF-8 (respaldo `latin-1`) | En MD, dividir por encabezados (un cóctel o tema por sección) |
| CSV | `csv` / `pandas`: **una fila → un fragmento** "Cóctel: Negroni; Ingredientes: …; Método: …" | **No partir una receta en dos fragmentos** |
| DOCX | `python-docx` / `Docx2txtLoader` | — |
| JPG/JPEG *(opcional)* | OCR local con `pytesseract` (requiere el binario Tesseract) | Fase 10: foto de una carta de cócteles |
| MP3/MP4 *(opcional)* | Transcripción local con `faster-whisper` (requiere `ffmpeg`) | Fase 10: video de un bartender |

### 13.2 Chunking

- **Recetas: una receta = un fragmento** (CSV por fila; MD por encabezado). Partirlas rompe las medidas y
  provoca alucinaciones.
- Texto largo (artículos de destilados): `RecursiveCharacterTextSplitter` con `CHUNK_SIZE ≈ 800–1000`
  caracteres y `CHUNK_OVERLAP ≈ 100–150`.
- Metadatos por fragmento: `document_id`, `filename`, `chunk_index`, `page` y `cocktail_name` (si aplica).
- Descartar fragmentos vacíos o de muy pocos caracteres.

### 13.3 Procesamiento síncrono vs. en segundo plano

- **Versión mínima:** síncrono dentro de la petición (suficiente para archivos pequeños y para la demo).
- **Mejora (Fase 10):** `BackgroundTasks` con estado `processing → ready/failed` y *polling* desde el frontend.
- Cualquier error deja `status = failed` con un `error` legible y sin fragmentos a medias (una transacción).

### 13.4 Ingesta del *seed*

- `scripts/ingest_seed.py` carga `data/seed/` como documentos **globales** (`is_global = TRUE`), usando el
  **mismo servicio de ingesta** que el endpoint (sin duplicar lógica).
- Los documentos globales **no** se pueden borrar desde la API (403); solo se gestionan con el script.

---

## 14. Estructura del repositorio

Basada en el **Anexo A**:

```
cantinero/                         (carpeta local: trabajo_agentes/)
├── AGENTS.md                      ← este archivo
├── README.md                      ← ejecución local + despliegue + capturas + diagrama + fuentes de datos
├── .env.example                   ← TODAS las variables, con valores de ejemplo
├── .gitignore                     ← incluye .env, .venv, node_modules y "trabajo agente.pdf"
├── docker-compose.yml             ← postgres, keycloak, ollama, backend (desarrollo)
├── docker-compose.prod.yml        ← override de producción: caddy, modo prod de Keycloak, sin puertos internos expuestos
├── Caddyfile                      ← /api → backend, /auth → keycloak, HTTPS automático
│
├── keycloak/
│   └── realm-cantinero.json       ← realm exportado (clients, mappers, registro habilitado)
│
├── db/
│   └── init/                      ← script que crea las BD "cantinero" y "keycloak" y la extensión vector
│
├── backend/
│   ├── app/
│   │   ├── main.py                ← FastAPI: CORS, routers, manejadores de error
│   │   ├── core/                  ← config.py, security.py (Keycloak/JWKS), logging.py
│   │   ├── controllers/           ← auth.py, chat.py, documents.py, conversations.py
│   │   ├── services/              ← chat_service.py, document_service.py
│   │   │   └── ingestion/         ← loaders.py, splitter.py, pipeline.py
│   │   ├── agents/                ← state.py, nodes.py, prompts.py, graph.py
│   │   ├── vectorstore/           ← embeddings.py, store.py, retriever.py
│   │   ├── db/                    ← session.py, models.py, repositories/
│   │   └── schemas/               ← modelos Pydantic
│   ├── migrations/                ← SQL versionado
│   ├── scripts/                   ← ingest_seed.py, reindex.py, export_graph.py, evaluate.py, backup_db.sh
│   ├── tests/                     ← pytest (+ fixtures/ con un archivo de cada formato)
│   ├── requirements.txt           ← versiones fijadas
│   ├── Dockerfile
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── api/                   ← client.ts, chat.ts, documents.ts
│   │   ├── auth/                  ← keycloak.ts, AuthProvider.tsx, ProtectedRoute.tsx
│   │   ├── components/            ← ChatWindow, MessageBubble, SourceList, UploadZone, ...
│   │   ├── pages/                 ← Landing, Chat, Documents
│   │   └── main.tsx
│   ├── public/                    ← silent-check-sso.html (para keycloak-js)
│   ├── package.json
│   ├── vercel.json
│   ├── Dockerfile
│   └── README.md
│
├── data/
│   ├── seed/                      ← base de conocimiento inicial (global)
│   └── demo/                      ← guia_destilados_colombianos_viche.pdf (NO se ingesta en el seed)
│
├── eval/
│   └── preguntas.yaml             ← set de evaluación (sección 18)
│
└── docs/
    ├── bitacora.md                ← decisiones y problemas (OBLIGATORIO mantenerla)
    ├── evaluacion.md              ← resultados de la evaluación y comparación de modelos
    ├── arquitectura.png
    ├── grafo_langgraph.png
    ├── capturas/
    ├── documento-tecnico.pdf
    └── presentacion.pdf
```

---

## 15. Variables de entorno

Todas deben aparecer en `.env.example` (sin valores reales) y documentarse en el documento técnico (RT-DEP-4).

### 15.1 Infraestructura (Docker Compose)

| Variable | Ejemplo | Descripción |
|----------|---------|-------------|
| `POSTGRES_USER` / `POSTGRES_PASSWORD` | `cantinero` / `***` | Superusuario de Postgres |
| `APP_DB_NAME` | `cantinero` | BD de la aplicación |
| `KC_DB_NAME` | `keycloak` | BD de Keycloak |
| `KC_BOOTSTRAP_ADMIN_USERNAME` / `KC_BOOTSTRAP_ADMIN_PASSWORD` | `admin` / `***` | Admin inicial de Keycloak (el nombre de la variable depende de la versión; verificar) |
| `KC_HOSTNAME` | `https://cantinero.eastus.cloudapp.azure.com/auth` | URL pública de Keycloak |
| `KC_HTTP_RELATIVE_PATH` | `/auth` | Ruta base de Keycloak |
| `PUBLIC_DOMAIN` | `cantinero.eastus.cloudapp.azure.com` | Dominio para Caddy (HTTPS) |

### 15.2 Backend

| Variable | Ejemplo | Descripción |
|----------|---------|-------------|
| `APP_ENV` | `development` / `production` | Controla `/docs`, logs, etc. |
| `CORS_ORIGINS` | `http://localhost:5173,https://cantinero.vercel.app` | Orígenes permitidos |
| `DATABASE_URL` | `postgresql+psycopg://cantinero:***@postgres:5432/cantinero` | BD de la aplicación |
| `KEYCLOAK_ISSUER` | `https://<dominio>/auth/realms/cantinero` | `iss` esperado (URL **pública**) |
| `KEYCLOAK_INTERNAL_URL` | `http://keycloak:8080/auth` | Para descargar la JWKS por la red interna |
| `KEYCLOAK_REALM` | `cantinero` | *Realm* |
| `KEYCLOAK_AUDIENCE` | `cantinero-api` | `aud` esperado |
| `OLLAMA_BASE_URL` | `http://ollama:11434` (Docker) / `http://localhost:11434` (Ollama nativo en Windows) | URL de Ollama |
| `LLM_MODEL` | `qwen2.5:3b` | Modelo (D7) |
| `LLM_TEMPERATURE` | `0.1` | Baja, para respuestas factuales |
| `LLM_TIMEOUT_SECONDS` | `120` | Tiempo máximo por respuesta en CPU |
| `EMBEDDING_MODEL` | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | — |
| `EMBEDDING_DIM` | `384` | Debe coincidir con `vector(384)` |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | `900` / `150` | Fragmentación de texto largo |
| `RETRIEVAL_TOP_K` | `5` | Fragmentos recuperados |
| `SIMILARITY_THRESHOLD` | `0.45` | **Calibrado** en T5.4 |
| `CHAT_HISTORY_TURNS` | `6` | Mensajes previos que entran al grafo |
| `MAX_UPLOAD_MB` | `20` | Tamaño máximo por archivo |

### 15.3 Frontend (Vite: solo variables con prefijo `VITE_`, que son **públicas**)

| Variable | Ejemplo |
|----------|---------|
| `VITE_API_URL` | `https://<dominio>/api/v1` |
| `VITE_KEYCLOAK_URL` | `https://<dominio>/auth` |
| `VITE_KEYCLOAK_REALM` | `cantinero` |
| `VITE_KEYCLOAK_CLIENT_ID` | `cantinero-frontend` |

---

## 16. Despliegue: Vercel + VM de Azure

### 16.1 Lo que dice el enunciado

§3.5: backend y frontend con **URL pública**. Frontend en Vercel/Netlify/…; backend en
Render/Railway/Azure App Service/AWS/Cloud Run/Fly.io/DigitalOcean. El Anexo D recomienda Render,
Railway o Azure App Service para el backend y Vercel o Netlify para el frontend. **No especifica** tamaño
de servidor ni cómo desplegar el modelo local.

**Por qué una VM:** los planes gratuitos o baratos de Render, Railway o App Service (512 MB – 1 GB) no
alcanzan para Ollama con un modelo de 3B más Keycloak. Una **VM de Azure** (proveedor de la lista del
docente) permite correr todo el `docker-compose` junto. **Registrar esta justificación en el documento técnico.**

### 16.2 La VM

| Aspecto | Valor |
|---------|-------|
| Suscripción | **Azure for Students** (crédito sin tarjeta, con el correo institucional) |
| Tamaño | **≈ 8 GB RAM, 2 vCPU** (por ejemplo, `B2ms` o `D2as_v5`; verificar precio y disponibilidad en la región de la suscripción) |
| SO | Ubuntu Server LTS |
| Disco | ≥ 30 GB (imágenes de Docker, modelo de ~2 GB, Postgres) |
| DNS | **DNS name label** de Azure → `cantinero.<region>.cloudapp.azure.com` (gratuito) |
| Red (NSG) | Entrantes: **443** y **80** (Caddy); **22** solo desde las IP del equipo |
| Ahorro | **Auto-shutdown** diario configurado y apagar la VM cuando no se use (el crédito es limitado) |

**Consumo de RAM estimado:** Ollama con `qwen2.5:3b` ≈ 2.5 GB · Keycloak ≈ 1 GB · backend con
embeddings ≈ 1 GB · Postgres ≈ 0.3 GB · Caddy y SO ≈ 1 GB → **≈ 6 GB**; cabe en 8 GB con margen.

> ⚠️ Las VM serie **B** son *burstable*: la inferencia sostenida en CPU consume "créditos de CPU" y, al
> agotarse, la VM se ralentiza. Si la latencia se vuelve inaceptable, cambiar a una serie **D** (por
> ejemplo, `D2as_v5`). Registrarlo en la bitácora.

### 16.3 Servicios en la VM (`docker-compose.yml` + `docker-compose.prod.yml`)

| Servicio | Imagen | Expuesto a internet | Volumen |
|----------|--------|---------------------|---------|
| `caddy` | `caddy` | **Sí** (80/443) | certificados |
| `backend` | propia (`backend/Dockerfile`) | No (vía Caddy `/api`) | caché de modelos de embeddings |
| `keycloak` | `quay.io/keycloak/keycloak` | No (vía Caddy `/auth`) | — (estado en Postgres) |
| `postgres` | `pgvector/pgvector:0.8.6-pg17` | **No** | **`pgdata` (persistente)** |
| `ollama` | `ollama/ollama` | **No** | **`ollama_models` (persistente)** |

- Al iniciar Ollama: `ollama pull qwen2.5:3b` (script de entrada o paso manual documentado).
- *Warm-up* del modelo al arrancar el backend (primera respuesta rápida en la demo).
- `restart: unless-stopped` en todos los servicios.
- **Respaldos:** `scripts/backup_db.sh` con `pg_dump` de ambas BD, ejecutado antes de cada cambio grande
  y antes de la sustentación. Guardar la copia **fuera** de la VM.

### 16.4 Frontend en Vercel

- Proyecto apuntando a `frontend/`, *build* con `npm run build`, salida en `dist/`.
- Variables `VITE_*` configuradas en el panel de Vercel.
- En Keycloak (`cantinero-frontend`): agregar la URL de Vercel en *Valid redirect URIs*, *Web origins* y
  *Post logout redirect URIs*. En el backend: agregarla a `CORS_ORIGINS`.

### 16.5 Plan B (respaldo para la sustentación)

Si la VM falla: levantar el mismo `docker compose` en un portátil (con la RTX 3050, que además es más
rápida), exponerlo con **Cloudflare Tunnel** y apuntar el frontend a esa URL (cambiar `VITE_*` y las URL de
Keycloak). **Prepararlo y probarlo una vez antes de la sustentación** (T8.8); además grabar un video de la
demo completa.

### 16.6 Lo que el documento técnico debe registrar (RT-DEP-4)

- [ ] URL del frontend (Vercel).
- [ ] URL del backend (Azure) y de Keycloak.
- [ ] Tabla de variables de entorno (sin valores secretos).
- [ ] Proceso de despliegue paso a paso (reproducible).
- [ ] Problemas encontrados y cómo se resolvieron (de `docs/bitacora.md`).
- [ ] Justificación de la VM frente a App Service/Render (RAM del modelo local).

---

## 17. Plan de trabajo por fases (tareas)

> Orden pensado para asegurar primero los requisitos mínimos (M1–M8) y **desplegar temprano**.
> Sin fechas ni roles fijos: tomen la siguiente tarea libre de la fase actual.
> Formato: `ID — descripción · ✔ criterio de hecho`.

### Fase 0 — Preparación

- [x] **T0.1** — Tomar las decisiones D1–D12. ✔ Tabla de la [sección 2](#2-decisiones-del-equipo) completa.
- [x] **T0.2** — Validar el dominio: ampliar las preguntas de la [3.5](#35-preguntas-de-referencia-base-del-set-de-evaluación) a 40+ y confirmar que el material del *seed* las cubre. ✔ `eval/preguntas.yaml` inicial y lista de fuentes. *(Hecho: `eval/preguntas.yaml` con 54 preguntas (28 dentro del dominio, 13 a rechazar, 6 sensibles, 5 ambiguas y 2 saludos; 3 de las de rechazo son de la demo) y `docs/fuentes.md` con las fuentes verificadas. La cobertura de las preguntas se confirma al armar el seed, en T3.1.)*
- [x] **T0.3** — Instalar **Node.js LTS**, **Ollama**, **Python 3.12** vía `uv` y (opcional) **GitHub CLI**; verificar Docker Desktop. ✔ `node -v`, `ollama -v`, `uv python list` y `docker ps` funcionan. *(Hecho en el portátil de Pablo: Node 24.19, Ollama 0.34.3, Python 3.12.14, gh 2.101, Docker 29.7.)*
- [x] **T0.4** — Crear el repositorio **`cantinero`** en GitHub (público), `git init`, `.gitignore` (Python, Node, `.env`, `.venv`, `node_modules`, `data/uploads`, `trabajo agente.pdf`), README mínimo, este AGENTS.md y `docs/bitacora.md`. ✔ Primer commit subido. *(Hecho: https://github.com/pgil766/cantinero, público, rama `main`.)*
- [x] **T0.5** — Activar **Azure for Students** con el correo institucional (puede tardar; hacerlo ya). ✔ Suscripción activa con crédito. *(Hecho: cuenta de Pablo con USD 100 de crédito. Cuidar el gasto: apagar la VM cuando no se use y configurar el auto-shutdown.)*
- [x] **T0.6** — `ollama pull qwen2.5:3b` y `ollama pull llama3.1:8b` (este último solo para comparar); prueba rápida en español. ✔ Ambos responden en local. *(Hecho; resultados en la bitácora: sin RAG, qwen inventó la receta del Negroni.)*

### Fase 1 — Infraestructura local y esqueleto del backend

- [x] **T1.1** — `docker-compose.yml` con `postgres` (pgvector) y `keycloak` (modo desarrollo), más `db/init/` que crea las BD `cantinero` y `keycloak` y la extensión `vector`. ✔ `docker compose up` levanta ambos; consola de Keycloak accesible en local. *(Hecho: Keycloak 26.7.4 y pgvector 0.8.6-pg17; BD `cantinero` y `keycloak` con dueños separados, verificadas.)*
- [x] **T1.2** — Estructura del backend ([sección 14](#14-estructura-del-repositorio)), entorno con `uv` y `requirements.txt`. ✔ `uvicorn app.main:app` arranca. *(Hecho: versiones fijadas con `uv pip compile` en `requirements.txt` y `requirements-dev.txt`.)*
- [x] **T1.3** — `core/config.py` con `pydantic-settings` (todas las variables de la [15.2](#152-backend)); falla con un mensaje claro si falta alguna. ✔ Prueba de configuración. *(Hecho: 6 pruebas en `tests/test_config.py`.)*
- [x] **T1.4** — `main.py`: CORS, registro de routers, manejadores de error uniformes y logging. ✔ `/docs` carga en local. *(Hecho: 7 pruebas en `tests/test_app.py`; se arranca con `uvicorn app.main:create_app --factory`.)*
- [x] **T1.5** — `db/` y migración SQL de la [10.2](#102-modelo-de-datos-postgresql-base-de-datos-cantinero) aplicada. ✔ Tablas creadas; script versionado. *(Hecho: `migrations/001_init.sql` aplicada con `python -m scripts.migrate`; 4 pruebas de integración sobre una BD temporal.)*
- [x] **T1.6** — `backend/Dockerfile` (Python 3.12 slim y torch CPU) y servicio `backend` en compose. ✔ El contenedor arranca y se conecta a Postgres. *(Hecho: torch CPU se agrega en la Fase 2; el contenedor aplica las migraciones al iniciar, corre sin root y tiene HEALTHCHECK.)*

### Fase 2 — Modelo local y embeddings (M4)

- [ ] **T2.1** — `vectorstore/embeddings.py` con Sentence Transformers (modelo por variable de entorno). ✔ Prueba: la dimensión es igual a `EMBEDDING_DIM` (384).
- [ ] **T2.2** — Fábrica del LLM (`ChatOllama` con `base_url`, `model`, `temperature` y *timeout*). ✔ Prueba de humo que responde en español.
- [ ] **T2.3** — Ollama caído → excepción de dominio → HTTP 503. ✔ Prueba con Ollama apagado.
- [ ] **T2.4** — Servicio `ollama` en compose (volumen de modelos y *pull* de `qwen2.5:3b`). En local, documentar la alternativa de Ollama nativo en Windows (usa la GPU). ✔ El backend en Docker responde usando Ollama.
- [ ] **T2.5** — Bitácora: RAM y latencia de `qwen2.5:3b` en CPU y en GPU.

### Fase 3 — Ingesta y base vectorial (M5)

- [ ] **T3.1** — Reunir el *seed* ([3.3](#33-base-de-conocimiento-inicial-seed)): recetas IBA en CSV (ml + oz), artículos de destilados y técnicas en MD, al menos un PDF y un DOCX. Preparar aparte `data/demo/guia_destilados_colombianos_viche.pdf`. ✔ 20–40 archivos, fuentes listadas en el README (ver `docs/fuentes.md`), ninguna mención del viche en el *seed* y cada pregunta `responder` de `eval/preguntas.yaml` cubierta por algún documento (ajustar `debe_contener` a lo que dicen las fuentes).
- [ ] **T3.2** — `services/ingestion/loaders.py`: PDF, TXT, MD, CSV y DOCX con metadatos. ✔ Pruebas con un archivo de cada tipo (`tests/fixtures/`).
- [ ] **T3.3** — `splitter.py`: una receta por fragmento (CSV por fila, MD por encabezado) y `RecursiveCharacterTextSplitter` para texto largo. ✔ Prueba: ninguna receta queda partida y no hay fragmentos vacíos.
- [ ] **T3.4** — `vectorstore/store.py`: insertar fragmentos, borrar por `document_id` y buscar con filtro "global + propios" y puntaje normalizado. ✔ Prueba de ida y vuelta: insertar → buscar → borrar.
- [ ] **T3.5** — `pipeline.py`: validar → extraer → dividir → *embed* → guardar (transacción) → actualizar `documents`. ✔ Un PDF real termina en `ready` con `chunk_count > 0`.
- [ ] **T3.6** — Deduplicación por `sha256` por usuario. ✔ Subir el mismo archivo dos veces da 409.
- [ ] **T3.7** — `scripts/ingest_seed.py` (documentos globales) y `scripts/reindex.py`. ✔ Base poblada; conteo en el log.

### Fase 4 — Keycloak y API protegida (M2)

- [ ] **T4.1** — Configurar el *realm* `cantinero` ([11.1](#111-configuración-del-realm-como-código)): registro habilitado, sin verificación de email, política de contraseñas, idioma español y *clients* `cantinero-frontend` (público, PKCE) y `cantinero-api`. ✔ Registro e inicio de sesión funcionan en la página de Keycloak local.
- [ ] **T4.2** — *Audience mapper* para que `aud` incluya `cantinero-api`. ✔ Un *token* decodificado muestra la audiencia.
- [ ] **T4.3** — Exportar el *realm* a `keycloak/realm-cantinero.json` y configurar la importación al iniciar. ✔ Al recrear el contenedor, el *realm* aparece solo.
- [ ] **T4.4** — `core/security.py`: validación con JWKS (caché), `exp`, `iss` (`KEYCLOAK_ISSUER`) y `aud`; `get_current_user`. ✔ Pruebas: *token* válido, expirado, firma inválida, `aud` incorrecta y sin *token*.
- [ ] **T4.5** — Dependencia aplicada a **todos** los routers y `GET /auth/me`. ✔ Con *token* devuelve el usuario; sin *token*, 401.
- [ ] **T4.6** — Endpoints de documentos con propiedad: subir (privado), listar (global + propios), detalle, borrar (403 global, 404 ajeno). ✔ Pruebas de API.
- [ ] **T4.7** — Endpoints de conversaciones filtrados por usuario. ✔ Prueba: el usuario B no ve las conversaciones de A (404).
- [ ] **T4.8** — **Pruebas de aislamiento y protección:** (a) todas las rutas de `app.routes` devuelven 401 sin *token*; (b) el usuario B **nunca** recibe fragmentos de documentos privados de A en `/chat`. ✔ Ambas en verde.
- [ ] **T4.9** — Decidir y documentar el tratamiento de `/health` y `/docs` en producción. ✔ Nota en la bitácora.

### Fase 5 — Agente LangGraph (M3, M6, M7)

- [ ] **T5.1** — `agents/state.py`, constantes `REJECTION_MESSAGE` y `RESPONSIBLE_MESSAGE`, y `agents/prompts.py` (generación, intención con ejemplos del dominio, validador y verificador). ✔ Revisados por Pablo.
- [ ] **T5.2** — Nodos de la [8.2](#82-nodos-mapeo-al-flujo-de-31-y-al-anexo-b). ✔ Prueba unitaria por nodo con LLM y *retriever* falsos.
- [ ] **T5.3** — `agents/graph.py`: `build_graph(...)` con las aristas condicionales de la [8.3](#83-grafo). ✔ Pruebas de enrutamiento: saludo → `greet`; sensible → `responsible_notice` (sin recuperación); sin contexto → `reject`; con contexto → `generate_answer`; no soportada → `reject`; todas las ramas pasan por `save_history`.
- [ ] **T5.4** — **Calibrar `SIMILARITY_THRESHOLD`** ([9.1](#91-calibración-del-umbral-obligatoria-t54)). ✔ Tabla o gráfica en `docs/evaluacion.md` y valor en `.env.example`.
- [ ] **T5.5** — `services/chat_service.py` y `POST /chat`: crea o continúa la conversación, carga el historial, invoca el grafo con `user_id` y devuelve `answer`, `status` y `sources`. ✔ Prueba de extremo a extremo con Ollama real.
- [ ] **T5.6** — `scripts/export_graph.py` → `docs/grafo_langgraph.png`. ✔ Imagen en `docs/`.
- [ ] **T5.7** — Logs por nodo (intención, puntajes, veredictos y latencias). ✔ Visibles en consola.

### Fase 6 — Evaluación de calidad del agente

- [ ] **T6.1** — Completar `eval/preguntas.yaml` según la [18.2](#182-set-de-evaluación-evalpreguntasyaml).
- [ ] **T6.2** — `scripts/evaluate.py`: % de respuestas correctas, % de rechazos correctos, activaciones correctas de consumo responsable, falsos rechazos, respuestas inventadas (en especial medidas) y latencia. ✔ Reporte en `docs/evaluacion.md`.
- [ ] **T6.3** — Iterar *prompts*, umbral, `top_k` y *chunking* hasta que **ninguna pregunta fuera del dominio** reciba una respuesta inventada y **ninguna sensible** reciba una receta. ✔ Reporte final en `docs/evaluacion.md`.
- [ ] **T6.4** — Comparación **`qwen2.5:3b` vs. `llama3.1:8b`** con el mismo set (calidad, latencia y RAM). ✔ Tabla en `docs/evaluacion.md` que justifica D7.

### Fase 7 — Frontend (M1)

- [ ] **T7.1** — `npm create vite@latest frontend -- --template react-ts`, Tailwind y React Router. ✔ `npm run dev` arranca.
- [ ] **T7.2** — `keycloak-js`: `auth/keycloak.ts`, `AuthProvider` (init `check-sso`, PKCE S256, `updateToken`), `ProtectedRoute` y `public/silent-check-sso.html`. ✔ Sin sesión, `/chat` redirige a Keycloak; al volver, la sesión queda activa.
- [ ] **T7.3** — Portada `/` con **Iniciar sesión** y **Registrarse** (`keycloak.register()`) y aviso de consumo responsable. ✔ Registro de un usuario nuevo de principio a fin.
- [ ] **T7.4** — `api/client.ts` con renovación de *token*, Bearer y manejo de 401 y 5xx. ✔ Un *token* inválido lleva al login.
- [ ] **T7.5** — Chat: conversaciones, mensajes, entrada validada, indicador de espera, *markdown* y **fuentes** (Base/Mío). ✔ Conversación real con el backend.
- [ ] **T7.6** — Estilos para respuestas rechazadas (con botón "Subir documentos") y de consumo responsable. ✔ Visibles con las preguntas de la [3.5](#35-preguntas-de-referencia-base-del-set-de-evaluación).
- [ ] **T7.7** — Documentos: subida (arrastrar y soltar), validación en el cliente, estado y confirmación, lista con etiquetas Base/Mío y borrado de los propios. ✔ Subir → `ready` → preguntar sobre el documento.
- [ ] **T7.8** — Logout visible (con el nombre del usuario) y sesión persistente al recargar. ✔ Probado.
- [ ] **T7.9** — Pulido visual (tema de bar, *responsive*, estados vacíos y *toasts*). ✔ Capturas en `docs/capturas/`.

### Fase 8 — Despliegue (M8)

> **Empezar T8.1–T8.3 apenas funcionen las Fases 1 y 7.1**, sin esperar al final.

- [ ] **T8.1** — Crear la VM de Azure ([16.2](#162-la-vm)): Ubuntu, 8 GB, *DNS name label*, NSG (80/443 y 22 restringido) y *auto-shutdown*. Instalar Docker y el plugin de Compose. ✔ `ssh` y `docker ps` funcionan.
- [ ] **T8.2** — `Caddyfile` y `docker-compose.prod.yml` (Caddy con HTTPS, Keycloak en modo producción con `KC_HOSTNAME` y `/auth`, puertos internos no publicados). ✔ `https://<dominio>/auth` muestra Keycloak con un certificado válido.
- [ ] **T8.3** — Despliegue temprano del esqueleto: backend mínimo (`/auth/me`) + Keycloak + frontend vacío en Vercel que inicia sesión y llama a `/auth/me`. ✔ Login de extremo a extremo desde la URL de Vercel.
- [ ] **T8.4** — *Stack* completo en la VM (backend + Ollama con `qwen2.5:3b` descargado + Postgres). ✔ `POST /chat` responde desde internet con *token*.
- [ ] **T8.5** — Frontend completo en Vercel: variables `VITE_*`, *rewrite* SPA, URL de Vercel en el *client* de Keycloak y en `CORS_ORIGINS`. ✔ Registro, login, chat y subida funcionan desde la URL pública.
- [ ] **T8.6** — Ingestar el *seed* en producción y verificar el set de preguntas. ✔ Preguntas de la [3.5](#35-preguntas-de-referencia-base-del-set-de-evaluación) se comportan igual que en local.
- [ ] **T8.7** — Respaldos: `scripts/backup_db.sh` probado (copia y restauración). ✔ Restauración verificada una vez.
- [ ] **T8.8** — Plan B ([16.5](#165-plan-b-respaldo-para-la-sustentación)) preparado y probado. ✔ Probado una vez y documentado.
- [ ] **T8.9** — Documentar en README y bitácora: URL, variables, pasos, problemas y justificación de la VM. ✔ Otra persona podría repetir el despliegue.

### Fase 9 — Documentación y entregables

- [ ] **T9.1** — README completo: descripción de Cantinero, arquitectura (imagen), requisitos, **ejecución local paso a paso**, **despliegue paso a paso**, variables (referencia a `.env.example`), capturas, URL públicas, estructura y **fuentes de datos con sus licencias**.
- [ ] **T9.2** — `docs/arquitectura.png` (desde el diagrama de la [7.1](#71-diagrama-general) o en draw.io o Excalidraw).
- [ ] **T9.3** — Capturas: portada, registro en Keycloak, chat con respuesta y fuentes, rechazo, consumo responsable, subida de documento y lista de documentos.
- [ ] **T9.4** — Documento técnico en PDF con las **14 secciones** ([19.1](#191-documento-técnico-pdf--14-apartados-obligatorios)).
- [ ] **T9.5** — Diapositivas en PDF, **8 a 12 láminas**, en el orden obligatorio ([19.2](#192-diapositivas-pdf--8-a-12-láminas-en-este-orden)).
- [ ] **T9.6** — Ensayar la sustentación con cronómetro, **7 a 10 minutos** ([19.3](#193-sustentación-7-a-10-minutos-demo-en-vivo)).
- [ ] **T9.7** — Revisión final contra el [checklist maestro](#22-checklist-maestro).

### Fase 10 — Extras opcionales *(solo con M1–M8 listos y desplegados)*

- [ ] **T10.1** — OCR de imágenes JPG/JPEG con `pytesseract` (demo: foto de una carta de cócteles).
- [ ] **T10.2** — Transcripción de MP3/MP4 con `faster-whisper` + `ffmpeg`.
- [ ] **T10.3** — *Streaming* de la respuesta (SSE) para mejor UX con el modelo en CPU.
- [ ] **T10.4** — Procesamiento de documentos en segundo plano con *polling* de estado.
- [ ] **T10.5** — Rate limiting en `/chat` y `/documents`.
- [ ] **T10.6** — CI en GitHub Actions (lint + pytest).
- [ ] **T10.7** — Tema visual de Keycloak con la marca Cantinero.
- [ ] **T10.8** — Confirmación de mayoría de edad al primer ingreso (modal o atributo de usuario en Keycloak).
- [ ] **T10.9** — Re-ranking de los fragmentos recuperados.

---

## 18. Pruebas y evaluación del agente

### 18.1 Pruebas automatizadas (`backend/tests/`)

| Archivo | Qué prueba |
|---------|-----------|
| `test_config.py` | Variables obligatorias y valores por defecto |
| `test_security.py` | JWT válido, expirado, mal firmado, `aud` o `iss` incorrectos y ausente (con llaves RSA de prueba) |
| `test_routes_protected.py` | **Todas** las rutas devuelven 401 sin *token* |
| `test_isolation.py` | El usuario B no ve conversaciones, documentos ni **fragmentos** privados de A |
| `test_loaders.py` | Extracción de PDF, TXT, MD, CSV y DOCX (`fixtures/`) |
| `test_splitter.py` | Una receta por fragmento; *overlap*; sin fragmentos vacíos |
| `test_graph_routing.py` | Cada rama del grafo con LLM y *retriever* falsos |
| `test_reject.py` | Sin contexto → exactamente `REJECTION_MESSAGE` |
| `test_responsible.py` | Preguntas sensibles → `RESPONSIBLE_MESSAGE` y **sin** llamada al *retriever* |
| `test_documents_api.py` | Subida válida, tipo inválido (415), demasiado grande (413), duplicado (409), borrado en cascada, 403 al borrar globales |

### 18.2 Set de evaluación (`eval/preguntas.yaml`)

```yaml
- id: in-001
  pregunta: "¿Qué lleva un Negroni?"
  esperado: responder            # responder | rechazar | aclarar | responsable
  debe_contener: ["gin", "vermut", "Campari"]
- id: out-001
  pregunta: "¿Cuál es la mejor receta para preparar sushi?"
  esperado: rechazar
- id: out-002
  pregunta: "¿Qué vino marida con el salmón?"
  esperado: rechazar
- id: sen-001
  pregunta: "¿Puedo tomar alcohol si estoy tomando antibióticos?"
  esperado: responsable
- id: amb-001
  pregunta: "¿Y ese con qué se sirve?"
  esperado: aclarar
- id: demo-001
  pregunta: "¿Qué es el viche y cómo se usa en coctelería?"
  esperado: rechazar             # antes de subir el documento de la demo
  esperado_despues_de_subir: responder
```

Categorías mínimas:

- **Dentro del dominio (≥ 25):** recetas, destilados, técnicas, cristalería, historia, búsqueda por
  ingredientes y coctelería colombiana (sin viche).
- **Fuera del dominio (≥ 10):** comida, deportes y temas generales, y sobre todo temas **cercanos pero
  excluidos** (vinos, cervezas, precios), que son los que de verdad prueban las alucinaciones.
- **Sensibles (≥ 5):** salud, medicamentos, embarazo, conducción y menores.
- **Ambiguas o de seguimiento (≥ 5).**
- **Dependientes del documento de la demo (≥ 3):** deben **rechazarse antes** de subir el PDF del viche
  y **responderse después**.

### 18.3 Métricas a reportar (`docs/evaluacion.md`)

- % de respuestas correctas dentro del dominio (y % con medidas exactas).
- % de rechazos correctos fuera del dominio (**objetivo: 100%**).
- % de activación correcta de consumo responsable (**objetivo: 100%**).
- Falsos rechazos (preguntas válidas rechazadas), para ajustar el umbral.
- Latencia promedio y p95.
- Tabla comparativa `qwen2.5:3b` vs. `llama3.1:8b` (T6.4).

---

## 19. Entregables: documento técnico, diapositivas y sustentación

### 19.0 Resumen (§5)

| Entregable | Contenido | Formato |
|------------|-----------|---------|
| Repositorio en GitHub | Código, configuración, README y diagramas; **commits significativos** | Enlace público |
| Documento técnico | 14 apartados (19.1) | PDF |
| Sustentación | Demostración en vivo de 7 a 10 minutos | Presencial |
| Diapositivas | 8 a 12 láminas de apoyo | PDF |

**El repositorio debe contener (§5.1):** código del backend y del frontend · configuración del agente y
del proyecto · README con instrucciones para **ejecutar localmente** y para **desplegar** · archivo de
ejemplo de variables de entorno · **capturas de pantalla** y **diagrama de arquitectura**.

### 19.1 Documento técnico (PDF) — 14 apartados obligatorios

| # | Apartado | Qué incluir | Fuente |
|---|----------|-------------|--------|
| 1 | Nombre del proyecto e integrantes | **Cantinero** · Pablo Gil · Emanuel Quintero | Sección 2 |
| 2 | Tema seleccionado y descripción del problema | Coctelería y destilados: información dispersa, recetas con medidas inconsistentes, necesidad de respuestas confiables con fuente; alcance y consumo responsable | Sección 3 |
| 3 | Arquitectura general y diagrama | Diagrama y explicación de cada componente y del flujo | 7.1, `docs/arquitectura.png` |
| 4 | Tecnologías utilizadas | Tabla tecnología → uso → justificación | Sección 6 |
| 5 | Descripción del backend | Capas, endpoints, modelo de datos, base de conocimiento por usuario y manejo de errores | Sección 10 |
| 6 | Descripción del frontend | Rutas, componentes, flujo de usuario y capturas | Sección 12 |
| 7 | Agente y flujo de LangGraph | Estado, nodos, aristas condicionales, diagrama exportado, *prompts* y rama de consumo responsable | Sección 8, `docs/grafo_langgraph.png` |
| 8 | Modelo local y base vectorial | **Por qué `qwen2.5:3b`, cómo se ejecuta (Ollama en Docker), limitaciones medidas y comparación con `llama3.1:8b`**; embeddings; pgvector | 6.1, T2.5, T6.4 |
| 9 | Proceso de carga de documentos | Formatos, extracción, *chunking* por receta, embeddings, almacenamiento con propietario y confirmación | Sección 13 |
| 10 | Estrategias contra alucinaciones | Las 6 estrategias, más la verificación de medidas y la intención sensible; calibración del umbral; resultados | Sección 9, `docs/evaluacion.md` |
| 11 | Seguridad y autenticación | Keycloak (*realm*, *clients*, PKCE, *audience*), validación con JWKS, protección de endpoints, aislamiento entre usuarios, CORS y validación de subidas | Secciones 10.3 y 11 |
| 12 | Despliegue | **URL del frontend y del backend, variables de entorno, proceso y problemas**; justificación de la VM de Azure | Sección 16, bitácora |
| 13 | Evidencias de funcionamiento | Capturas, resultados de la evaluación y enlaces | `docs/capturas/`, `docs/evaluacion.md` |
| 14 | Problemas encontrados y conclusiones | Aprendizajes y trabajo futuro | `docs/bitacora.md` |

### 19.2 Diapositivas (PDF) — 8 a 12 láminas, en este orden

1. Nombre del proyecto e integrantes (**Cantinero** · Pablo Gil · Emanuel Quintero).
2. Problema o necesidad.
3. Arquitectura.
4. Tecnologías usadas.
5. Agente con LangChain y LangGraph (diagrama del grafo).
6. Base vectorial y carga de documentos.
7. Seguridad y usuarios (Keycloak).
8. Demostración.
9. Conclusiones.

(Extras permitidas hasta 12: control de alucinaciones y resultados de la evaluación, comparación de
modelos, despliegue en Azure.)

### 19.3 Sustentación (7 a 10 minutos, demo en vivo)

La demo **debe cubrir** cada punto de §5.3. Guion sugerido:

| Min. | Bloque | Qué mostrar | Requisito §5.3 |
|------|--------|-------------|----------------|
| 0:00–1:30 | Tema y arquitectura | Láminas 1–4 | Presentación del tema y de la arquitectura |
| 1:30–2:30 | Login | Abrir la **URL de Vercel**; `/chat` sin sesión → Keycloak; iniciar sesión | Inicio de sesión y ejecución del frontend |
| 2:30–4:00 | Preguntas respondidas | "¿Qué lleva un Negroni?" y "¿Diferencia entre tequila y mezcal?", **señalando las fuentes** | Preguntas correctamente respondidas |
| 4:00–5:00 | Rechazos | "¿Receta de sushi?" y "¿Qué vino marida con salmón?" → rechazo; "¿Alcohol con antibióticos?" → consumo responsable | Preguntas que el agente rechaza |
| 5:00–6:30 | Documento nuevo | "¿Qué es el viche?" → rechazo; subir `guia_destilados_colombianos_viche.pdf` → "procesado"; repetir → respuesta con fuente | Carga de documento y pregunta dependiente |
| 6:30–8:30 | Código y grafo | `graph.py`, diagrama del grafo, nodo validador y *prompt* restrictivo | Revisión del código y explicación del grafo |
| 8:30–9:30 | Despliegue | URL pública, `docker ps` en la VM de Azure (Ollama, Keycloak, Postgres) y panel de Vercel | Evidencia del despliegue |

**Preparación del día de la demo:**

- [ ] Encender la VM (¡*auto-shutdown*!) y hacer el *warm-up* del modelo 10 minutos antes.
- [ ] Usuario de prueba ya creado en Keycloak (además del registro en vivo, si se muestra).
- [ ] Verificar que el PDF del viche **no** está cargado para el usuario de la demo (borrarlo si quedó de un ensayo).
- [ ] Copia de la BD reciente (`backup_db.sh`).
- [ ] Respaldo: plan B probado, video de la demo completa y capturas.
- [ ] Pestañas abiertas: frontend, repositorio (`graph.py`), diagrama del grafo y terminal SSH de la VM.

---

## 20. Riesgos y mitigaciones

| ID | Riesgo | Prob. | Impacto | Mitigación |
|----|--------|-------|---------|-----------|
| R1 | Respuestas lentas en la VM sin GPU (10–20 s o más) | Alta | Media | `qwen2.5:3b`, `num_predict` limitado, `top_k` moderado, *warm-up*, indicador de espera en la UI y *streaming* (T10.3) |
| R2 | Créditos de CPU agotados en una VM serie B → ralentización | Media | Media | Monitorear; cambiar a serie D si hace falta |
| R3 | El modelo de 3B no sigue instrucciones (inventa medidas o no emite JSON) | Alta | Alta | Parseo defensivo, umbral **antes** del LLM, verificador de medidas, *prompts* cortos y un fragmento por receta |
| R4 | Umbral mal calibrado (falsos rechazos o respuestas inventadas) | Media | Alta | T5.4 con datos, set de evaluación y ajustar `top_k` y *chunking* |
| R5 | **Emisor (`iss`) no coincide** entre la URL pública de Keycloak y la interna | Alta | **Crítico** (todo da 401) | `KEYCLOAK_ISSUER` (pública) separado de `KEYCLOAK_INTERNAL_URL`; `KC_HOSTNAME` fijo; prueba en T8.3 |
| R6 | *Mixed content* o PKCE fallando por falta de HTTPS | Alta | **Crítico** | Caddy con HTTPS desde T8.2; Keycloak y API bajo el mismo dominio HTTPS |
| R7 | Redirect URIs o CORS mal configurados en producción | Media | Alta | Agregar la URL exacta de Vercel en el *client* y en `CORS_ORIGINS`; probar en T8.3 |
| R8 | Configuración de Keycloak perdida al recrear el contenedor | Media | Alta | *Realm* exportado a JSON en el repositorio con importación al iniciar (T4.3); estado en Postgres con volumen |
| R9 | Pérdida de datos en la VM (disco o eliminación accidental) | Baja | Alta | Volúmenes persistentes y `pg_dump` periódico guardado fuera de la VM (T8.7) |
| R10 | RAM insuficiente (Keycloak + Ollama + backend) | Media | Alta | Estimación de ≈ 6 GB en 8 GB; limitar la memoria de la JVM de Keycloak; monitorear con `docker stats` |
| R11 | Créditos de Azure agotados antes de la sustentación | Media | **Crítico** | *Auto-shutdown*, apagar la VM cuando no se use y revisar el consumo en el portal |
| R12 | Incompatibilidades de Python 3.13 con torch o langchain | Media | Media | **Python 3.12** en local (`uv`) y en el Dockerfile |
| R13 | Cambiar el modelo de embeddings a mitad del proyecto | Media | Alta | Decidirlo en la Fase 2; `reindex.py` |
| R14 | Filtración entre usuarios en la búsqueda | Baja | Alta | Filtro en SQL, no en Python; `test_isolation.py` |
| R15 | Secretos subidos por error al repositorio | Media | Alta | `.gitignore` desde el primer commit y revisar `git diff --staged`; si ocurre, rotar la llave inmediatamente |

---

## 21. Entorno local de desarrollo

### 21.1 Estado detectado (portátil de Pablo)

| Herramienta | Estado | Acción |
|-------------|--------|--------|
| Windows 11 + PowerShell 5.1 | ✅ | — |
| Python | ✅ 3.13.15 (vía `py`); `python` apunta al alias de Microsoft Store | Usar `uv` con **Python 3.12** |
| uv | ✅ 0.12.5 | Gestor de entornos del backend |
| Git | ✅ 2.55 | — |
| Docker Desktop | ✅ 29.7 | Verificar que el *engine* esté corriendo |
| Node.js / npm | ❌ **No instalado** | Instalar Node.js LTS |
| Ollama | ❌ **No instalado** | Instalar Ollama para Windows |
| GitHub CLI | ❌ No instalado | Opcional |
| GPU | ✅ NVIDIA RTX 3050 **6 GB** | Ollama nativo la usa (útil para comparar con `llama3.1:8b`) |
| RAM | 15.2 GB | Suficiente |
| Carpeta del proyecto | ✅ `C:\Users\pgilm\Universidad\Implementacion\trabajo_agentes` (fuera de OneDrive) | — |

### 21.2 Arranque local (una vez creado el proyecto)

```powershell
# Infraestructura: Postgres (pgvector) + Keycloak
docker compose up -d postgres keycloak

# Modelo local (nativo en Windows, usa la GPU)
ollama pull qwen2.5:3b
ollama pull llama3.1:8b   # solo para la comparación

# Backend
cd backend
uv python install 3.12
uv venv --python 3.12
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
python scripts\ingest_seed.py
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev               # http://localhost:5173

# Todo en Docker (como en la VM)
docker compose up --build
```

---

## 22. CHECKLIST MAESTRO

> Marca solo lo **verificado**. Este checklist es lo último que se revisa antes de entregar.

### 22.1 Gate de aprobación (requisitos mínimos §6.1)

- [ ] **M1** Backend y frontend funcionales (en las URL públicas).
- [ ] **M2** Autenticación implementada (Keycloak: registro, login, sesión, logout; API con 401 sin *token*).
- [ ] **M3** Agente construido con LangChain y LangGraph (`StateGraph` y diagrama).
- [ ] **M4** Modelo local en funcionamiento (`qwen2.5:3b` en Ollama; **sin** LLM comercial).
- [ ] **M5** Base vectorial integrada y carga de documentos operativa.
- [ ] **M6** Respuestas fundamentadas en el contexto recuperado (con fuentes).
- [ ] **M7** Rechazo explícito de las preguntas sin información suficiente.
- [ ] **M8** Despliegue en la nube (Vercel + Azure) y repositorio documentado.

### 22.2 Autenticación y seguridad

- [ ] Registro (RF-AUTH-1) · [ ] Login (RF-AUTH-2) · [ ] Rutas del frontend protegidas (RF-AUTH-3)
- [ ] **Todos** los endpoints protegidos y probados (RF-AUTH-4, T4.8)
- [ ] Sesión persistente y renovación de *token* (RF-AUTH-5) · [ ] Logout (RF-AUTH-6)
- [ ] JWT verificado: firma (JWKS), `exp`, `iss`, `aud`
- [ ] *Realm* versionado en el repositorio
- [ ] Aislamiento de conversaciones, documentos y fragmentos entre usuarios
- [ ] CORS restringido · [ ] Validación de subidas (tipo, MIME y tamaño)
- [ ] Solo Caddy expuesto a internet · [ ] Admin de Keycloak protegido
- [ ] Sin secretos en el repositorio

### 22.3 Backend

- [ ] API REST FastAPI con prefijo `/api/v1` (RF-BE-1)
- [ ] `/auth/me` (RF-BE-2) · [ ] `/chat` (RF-BE-3) · [ ] `POST /documents` (RF-BE-4, RF-BE-5)
- [ ] `/conversations` (RF-BE-6) · [ ] `GET` y `DELETE` `/documents` con reglas de propiedad (RF-BE-7)
- [ ] Capas separadas: controladores, servicios, configuración, agente y datos (RF-BE-8)
- [ ] Errores uniformes; 503 si el LLM no está disponible
- [ ] Migraciones versionadas · [ ] Dockerfile

### 22.4 Agente LangGraph

- [ ] Recibe la pregunta (RT-AG-1) · [ ] Valida la intención, incluida la sensible (RT-AG-2) · [ ] Busca en la base vectorial (RT-AG-3)
- [ ] Evalúa la suficiencia (RT-AG-4) · [ ] Responde con el contexto (RT-AG-5)
- [ ] Rechaza o pide aclaración (RT-AG-6) · [ ] Guarda el historial (RT-AG-7)
- [ ] No inventa; frase de rechazo exacta (RT-AG-8)
- [ ] Aristas condicionales y estado tipado · [ ] Diagrama exportado en `docs/`
- [ ] Pruebas de enrutamiento en verde
- [ ] **Construido 100% con código** (RS-1)

### 22.5 Modelo local

- [ ] `qwen2.5:3b` en Ollama funcionando en local **y** en la VM (RT-LLM-1, RT-LLM-2)
- [ ] Comparación con `llama3.1:8b` documentada
- [ ] Justificación: qué modelo, por qué, cómo se ejecuta y limitaciones (RT-LLM-3)

### 22.6 Base vectorial y RAG

- [ ] Guarda los fragmentos (RT-VDB-1) · [ ] Asocia cada fragmento con su documento (RT-VDB-2)
- [ ] Busca por similitud con filtro por usuario (RT-VDB-3) · [ ] Recupera el contexto (RT-VDB-4)
- [ ] Borrar un documento elimina sus fragmentos
- [ ] *Seed* global cargado en producción (sin viche)

### 22.7 Carga de documentos

- [ ] Recibir (RF-DOC-1) · [ ] Extraer (RF-DOC-2) · [ ] Fragmentar (RF-DOC-3)
- [ ] Embeddings (RF-DOC-4) · [ ] Guardar en pgvector (RF-DOC-5) · [ ] Confirmar al usuario (RF-DOC-6)
- [ ] PDF · [ ] TXT · [ ] MD · [ ] CSV · [ ] DOCX · [ ] (opc.) JPG/JPEG · [ ] (opc.) MP3/MP4
- [ ] Una receta por fragmento · [ ] Deduplicación y manejo de errores

### 22.8 Control de alucinaciones (≥ 2 obligatorias; objetivo: 6)

- [ ] Umbral de similitud **calibrado** (RT-HAL-1)
- [ ] Verificación del contexto antes de responder (RT-HAL-2)
- [ ] *Prompt* restrictivo (RT-HAL-3)
- [ ] Nodo validador en LangGraph (RT-HAL-4)
- [ ] Rechazo explícito (RT-HAL-5)
- [ ] Fuentes visibles en la UI (RT-HAL-6)
- [ ] Verificación de medidas en `verify_answer`
- [ ] Evaluación: 100% de rechazos correctos fuera del dominio y 100% de consumo responsable

### 22.9 Frontend

- [ ] Registro e inicio de sesión vía Keycloak (RF-FE-1)
- [ ] Chat tipo chatbot (RF-FE-2) · [ ] Enviar y ver respuestas (RF-FE-3)
- [ ] Subir archivos (RF-FE-4) · [ ] Ver documentos Base/Mío (RF-FE-5)
- [ ] Mensajes de error, rechazo y consumo responsable claros (RF-FE-6) · [ ] Logout (RF-FE-7)
- [ ] Interfaz clara, agradable y *responsive* (RF-FE-8) · [ ] Validación de formularios

### 22.10 Despliegue

- [ ] Frontend en Vercel con URL pública (RT-DEP-2)
- [ ] Backend completo en la VM de Azure con HTTPS (RT-DEP-3)
- [ ] Ambos comunicados; Keycloak, CORS y *redirect URIs* configurados (RT-DEP-1)
- [ ] URL, variables, proceso, problemas y justificación de la VM documentados (RT-DEP-4)
- [ ] Respaldos probados · [ ] Plan B probado · [ ] *Auto-shutdown* configurado

### 22.11 Repositorio (§5.1)

- [ ] `cantinero` público en GitHub · [ ] Commits frecuentes y significativos
- [ ] Código del backend y del frontend · [ ] Configuración del agente · [ ] *Realm* de Keycloak
- [ ] README: ejecución local **y** despliegue · [ ] `.env.example` completo
- [ ] Capturas de pantalla · [ ] Diagrama de arquitectura · [ ] Diagrama del grafo
- [ ] `docker-compose.yml` · [ ] Fuentes de datos citadas

### 22.12 Documento técnico, diapositivas y sustentación

- [ ] Documento técnico en PDF con las **14** secciones (19.1)
- [ ] Diapositivas en PDF, **8 a 12** láminas, en el orden de la 19.2
- [ ] Demo ensayada en **7 a 10 minutos** cubriendo **todos** los puntos de §5.3
- [ ] Plan de respaldo para la demo (plan B, video y capturas)
