# RAG-Based University Knowledge Assistant

A grounded university Q&A system that ingests trusted academic documents, retrieves relevant passages, and optionally uses an LLM to generate concise answers with source references.

## Production-style features
- `.txt` / `.md` document ingestion
- Overlapping chunking
- TF-IDF + cosine retrieval baseline
- Top-K source selection
- Grounded optional OpenAI generation
- Source metadata returned with every answer
- Interactive browser dashboard
- FastAPI + OpenAPI
- GitHub Actions CI
- No API key required for retrieval-only mode

## Architecture
```text
University Docs
      |
 Ingestion -> Chunking -> TF-IDF Index
                              |
Student Question -> Retriever -> Top-K Context
                                      |
                         +------------+------------+
                         |                         |
                  Extractive mode            Optional LLM
                         |                         |
                         +---------- Answer + Sources
```

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000/` for the dashboard or `/docs` for the API.

## API
- `POST /api/v1/documents` — index a document
- `POST /api/v1/ask` — retrieve and answer a question
- `GET /health` — knowledge-base health

Example:
```json
{"question":"When does the semester begin?","top_k":3}
```

## LLM mode
Copy `.env.example`, set `OPENAI_API_KEY`, and optionally set `OPENAI_MODEL`. The LLM receives only retrieved document context, reducing unsupported answers compared with unconstrained generation.

## Security
Never commit API keys. Keep `.env` local and use environment variables or a deployment secret manager.

## Next production upgrades
Persistent vector database, PostgreSQL document metadata, authentication/RBAC, document upload validation, conversation history, retrieval evaluation (precision/recall), hybrid BM25 + embeddings, and deployment monitoring.