# EduPulse AI — RAG-Based University Knowledge Assistant

EduPulse AI is a production-oriented university knowledge assistant that retrieves trusted academic content and generates grounded answers with source references.

## What this project demonstrates

- **RAG pipeline:** document ingestion → chunking → TF-IDF retrieval → grounded answer generation
- **LLM integration:** optional OpenAI generation using retrieved context only
- **Authentication:** JWT access tokens + Argon2 password hashing
- **Persistence:** PostgreSQL in production, SQLite for local development
- **Protected ingestion:** only authenticated users can add knowledge documents
- **Source attribution:** answers expose retrieved source metadata
- **Production deployment:** Docker + Render Blueprint + managed PostgreSQL + HTTPS
- **API:** FastAPI + OpenAPI documentation
- **CI:** automated pytest workflow
- **Responsive UI:** authentication, Q&A, document ingestion and health status

## Architecture

```text
                    Browser
                       |
                    HTTPS
                       |
              FastAPI application
               /       |        \
              /        |         \
          JWT Auth   RAG Engine   Health
             |           |
        PostgreSQL   TF-IDF Retriever
                        |
                  Top-K Context
                        |
                 OpenAI (optional)
                        |
                 Answer + Sources
```

## Run locally

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/` or `/docs` for Swagger UI.

For local development, leaving `DATABASE_URL` unset uses SQLite. Set `OPENAI_API_KEY` for LLM generation.

## API

| Endpoint | Purpose | Auth |
|---|---|---|
| `POST /api/v1/auth/register` | Create account | No |
| `POST /api/v1/auth/login` | Get JWT token | No |
| `GET /api/v1/auth/me` | Current user | JWT |
| `POST /api/v1/documents` | Persist + index document | JWT |
| `POST /api/v1/ask` | Retrieve and answer | No |
| `GET /health` | Application/database health | No |

## Deploy to Render

The repository includes `render.yaml` for a Blueprint deployment.

1. Connect the GitHub repository to Render.
2. Create a new Blueprint from the repository.
3. Render creates the web service and PostgreSQL database from `render.yaml`.
4. Add `OPENAI_API_KEY` as a deployment secret if LLM generation is desired.
5. After deployment, open the generated HTTPS `onrender.com` URL.

The configuration enables automatic deploys and uses `/health` as the health check. The free database is suitable for a portfolio demo; use a persistent paid database plan for long-term production data.

## Security

Never commit `.env` or API keys. Use deployment secrets for production credentials. Rotate `SECRET_KEY` if it is exposed.

## Testing

```bash
pytest -q
```

Tests cover health checks, authentication, login and protected document ingestion.

## Interview talking points

- **Why PostgreSQL?** Durable relational storage, constraints and transactions for users/documents.
- **Why JWT?** Stateless API authentication that can scale across application instances.
- **Why RAG?** Retrieved institutional context reduces unsupported generation and provides inspectable sources.
- **Why TF-IDF first?** Lightweight, explainable retrieval baseline before comparing embeddings/hybrid retrieval.
- **What happens on restart?** Documents are loaded from PostgreSQL and the retrieval index is rebuilt at startup.
- **How is production configured?** Docker-compatible FastAPI process, environment-based secrets, managed PostgreSQL, health checks and CI.
