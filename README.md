# electricity-rag

Sistema RAG (Retrieval-Augmented Generation) con FastAPI para consultar
documentación real del mercado eléctrico español en lenguaje natural.
Proyecto 3 de un portfolio backend Python de 5 proyectos progresivos
(ver [proyecto 2](https://github.com/castgomezborja-git/electricity-pipeline)
para la fuente de datos históricos del precio de la luz).

## Objetivo

Backend con integración real de IA (no un wrapper de chat): ingesta de
documentos → chunking → embeddings → almacenamiento vectorial → recuperación
semántica → generación aumentada con citas, todo con orquestación propia
(sin frameworks tipo LangChain) para poder defender cada paso del pipeline.

## Stack

- **Lenguaje/entorno:** Python 3.12, `uv` como gestor de dependencias
- **API:** FastAPI (pendiente)
- **Base de datos:** PostgreSQL 16 + extensión `pgvector` (vector store), vía Docker Compose
- **ORM:** SQLAlchemy 2.0
- **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`, 384 dimensiones) — local, sin coste
- **LLM generador:** `llama3.1:8b` vía Ollama — local, sin coste
- **Autenticación:** JWT real con usuarios (pendiente)
- **Orquestación RAG:** código propio, sin LangChain

## Corpus

Documentación oficial y pública sobre el mercado eléctrico español:
- Guía informativa para los consumidores de electricidad (CNMC)
- [pendiente: 2-3 documentos adicionales]

## Estado actual

- [x] Scaffolding del proyecto (`uv init --package`)
- [x] Configuración vía `pydantic-settings` (`.env`)
- [x] Modelo de datos: `Document` y `Chunk` (con columna vectorial `embedding`)
- [x] PostgreSQL + `pgvector` vía Docker Compose, tablas creadas y verificadas
- [x] Ingesta: extracción de texto (PDF, con detección de cabecera/pie de página repetidos), chunking por tokens
- [ ] Retrieval: búsqueda semántica top-k
- [ ] Generación: prompt aumentado + Ollama, respuesta con citas
- [ ] API FastAPI
- [ ] Autenticación JWT
- [ ] Tests (unitarios + `testcontainers` para la capa de base de datos)
- [ ] Dockerización completa de la app (además de Postgres)
- [ ] Despliegue

## Cómo levantar el entorno de desarrollo

```powershell
uv sync
docker compose up -d
uv run python scripts/create_tables.py
```

Requiere un `.env` local (no versionado) con `DATABASE_URL`, `POSTGRES_USER`,
`POSTGRES_PASSWORD` y `POSTGRES_DB`.