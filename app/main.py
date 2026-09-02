from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.models import AskRequest, DocumentRequest
from app.rag import generator, kb

app = FastAPI(title="RAG University Knowledge Assistant", version="2.0.0")


@app.get("/", include_in_schema=False)
def home():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "ok", "documents_indexed": len(kb.chunks)}


@app.post("/api/v1/documents")
def add_document(request: DocumentRequest):
    kb.add_document(request.title, request.content)
    return {"status": "indexed", "chunks": len(kb.chunks)}


@app.post("/api/v1/ask")
def ask(request: AskRequest):
    if not kb.chunks:
        raise HTTPException(status_code=409, detail="Knowledge base is empty. Add a document first.")
    results = kb.retrieve(request.question, request.top_k)
    return generator.generate(request.question, results)
