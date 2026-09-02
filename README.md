# RAG-Based University Knowledge Assistant

A retrieval-augmented generation (RAG) backend for answering university questions from trusted documents instead of relying only on model memory.

## Features
- Document ingestion from `.txt` and `.md`
- Chunking with overlap
- TF-IDF retrieval with cosine similarity for a dependency-light baseline
- Source-aware answers with citations
- FastAPI endpoints for ingestion and question answering
- Conversation-independent retrieval, making responses reproducible
- Clear boundary between retrieval and generation

## Architecture
```text
University Docs -> Ingestion -> Chunking -> TF-IDF Index
                                             |
User Question -> Retriever -> Top-K Context -> Answer Generator
                                             |
                                         Sources
```

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API
`POST /api/v1/documents`
```json
{"title":"Academic Calendar","content":"The semester begins on..."}
```

`POST /api/v1/ask`
```json
{"question":"When does the semester begin?","top_k":3}
```

The reference implementation uses extractive answers from retrieved context so it can run without an external LLM key. A production deployment can replace `AnswerGenerator` with an LLM while preserving the retrieval contract.

## Why this project matters
This demonstrates practical RAG fundamentals: ingestion, chunking, indexing, semantic retrieval, grounding, citations, and evaluation boundaries.