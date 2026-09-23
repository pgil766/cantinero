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

## 2026-09-23 · Nota · Python 3.12 para el proyecto

- El equipo tiene Python 3.13 instalado, pero se usa **Python 3.12** (vía `uv`) en local y en Docker para evitar
  incompatibilidades de PyTorch y LangChain con la versión más reciente.
