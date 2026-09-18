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
- **API:** FastAPI
- **Base de datos:** PostgreSQL 16 + extensión `pgvector` (vector store), vía Docker Compose
- **ORM:** SQLAlchemy 2.0
- **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`, 384 dimensiones) — local, sin coste
- **LLM generador:** `llama3.1:8b` vía Ollama — local, sin coste
- **Autenticación:** JWT real con usuarios (bcrypt para hasheo de contraseñas)
- **Orquestación RAG:** código propio, sin LangChain

## Corpus

Documentación oficial y pública sobre el mercado eléctrico español:
- Guía informativa para los consumidores de electricidad (CNMC, 2022)
- Funcionamiento del Mercado Diario (OMIE)
- [pendiente: bono social eléctrico — vía URL, requiere loader HTML aún no construido]

## Estado actual

- [x] Scaffolding del proyecto (`uv init --package`)
- [x] Configuración vía `pydantic-settings` (`.env`)
- [x] Modelo de datos: `Document`, `Chunk` (columna vectorial `embedding`) y `User`
- [x] PostgreSQL + `pgvector` vía Docker Compose, tablas creadas y verificadas
- [x] Ingesta: extracción de texto (PDF, con detección de cabecera/pie de página repetidos), chunking por tokens, embeddings (sentence-transformers), persistencia idempotente en PostgreSQL/pgvector
- [x] Retrieval: búsqueda semántica top-k (distancia coseno con pgvector)
- [x] Generación: prompt aumentado con citas + Ollama (llama3.1:8b), verificado con demo real de reducción de alucinación
- [x] API FastAPI (`POST /ask`)
- [x] Autenticación JWT (`POST /login`, bcrypt, token con expiración de 30min, endpoint `/ask` protegido)
- [x] Tests unitarios (chunking, extracción/limpieza de PDF, hashing — 12 tests)
- [ ] Tests de integración con `testcontainers` para la capa de persistencia/retrieval
- [ ] Dockerización completa de la app (además de Postgres)
- [ ] Despliegue

## Cómo levantar el entorno de desarrollo

```powershell
uv sync
docker compose up -d
docker compose exec postgres psql -U electricity_rag -d electricity_rag -c "CREATE EXTENSION IF NOT EXISTS vector;"
uv run python scripts/create_tables.py
uv run python scripts/ingest.py
uv run python scripts/create_user.py <username> <password>
uv run uvicorn electricity_rag.main:app --reload
```

Requiere un `.env` local (no versionado) con `DATABASE_URL`, `POSTGRES_USER`,
`POSTGRES_PASSWORD`, `POSTGRES_DB` y `JWT_SECRET_KEY` (genera este último con
`python -c "import secrets; print(secrets.token_hex(32))"`, nunca lo escribas a mano).

Con el servidor levantado, la documentación interactiva está disponible en
`http://127.0.0.1:8000/docs`.

## Notas de instalación

Si `ollama pull` falla con un error de certificado TLS contra el backend de
Cloudflare R2 (bug conocido de Ollama, no depende de antivirus/VPN/router),
la alternativa es descargar el GGUF manualmente desde HuggingFace y crear el
modelo local con `ollama create llama3.1:8b -f Modelfile` (con una línea
`FROM <ruta_al_gguf>` en el Modelfile).

## Notas de mejoras futuras

- Endpoint `POST /register` — decidido NO implementarlo en el alcance actual:
  dejarlo abierto sin restricciones permitiría a cualquiera crear cuentas y
  consumir el LLM/GPU local; hacerlo bien requeriría añadir un rol admin que
  autorizara la creación de usuarios, una dimensión de autorización completa
  sin otro caso de uso en el proyecto (mismo motivo YAGNI por el que `User`
  no tiene campo `role`). El único usuario se sigue creando vía
  `scripts/create_user.py`.
- Formato de citas `[Fuente: ...]` no siempre presente en la respuesta del LLM (no determinismo del modelo) — se podría reforzar con `temperature` más baja o prompt más insistente