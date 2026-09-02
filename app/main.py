from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user, hash_password, verify_password
from app.db import Document, User, get_db, init_db
from app.models import AskRequest, AuthRequest, DocumentRequest
from app.rag import generator, kb


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    with next(get_db()) as db:
        documents = db.scalars(select(Document).order_by(Document.id)).all()
        for document in documents:
            kb.add_document(document.title, document.content)
    if not kb.chunks:
        sample = Path("data/sample_handbook.md")
        if sample.exists():
            content = sample.read_text(encoding="utf-8")
            with next(get_db()) as db:
                document = Document(title="University Academic Handbook", content=content)
                db.add(document)
                db.commit()
            kb.add_document("University Academic Handbook", content)
    yield


app = FastAPI(title="EduPulse AI — University Knowledge Assistant", version="3.0.0", lifespan=lifespan)


@app.get("/", include_in_schema=False)
def home():
    return FileResponse("static/index.html")


@app.get("/health")
def health(db: Session = Depends(get_db)):
    return {"status": "ok", "database": "connected", "documents_indexed": len(kb.chunks), "documents_stored": db.query(Document).count()}


@app.post("/api/v1/auth/register")
def register(request: AuthRequest, db: Session = Depends(get_db)):
    email = request.email.strip().lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = User(email=email, password_hash=hash_password(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"access_token": create_access_token(user.id), "token_type": "bearer", "user": {"id": user.id, "email": user.email}}


@app.post("/api/v1/auth/login")
def login(request: AuthRequest, db: Session = Depends(get_db)):
    email = request.email.strip().lower()
    user = db.scalar(select(User).where(User.email == email))
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return {"access_token": create_access_token(user.id), "token_type": "bearer", "user": {"id": user.id, "email": user.email}}


@app.get("/api/v1/auth/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email}


@app.post("/api/v1/documents")
def add_document(request: DocumentRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    document = Document(title=request.title.strip(), content=request.content)
    db.add(document)
    db.commit()
    kb.add_document(document.title, document.content)
    return {"status": "indexed", "document_id": document.id, "chunks": len(kb.chunks), "created_by": user.email}


@app.post("/api/v1/ask")
def ask(request: AskRequest):
    if not kb.chunks:
        raise HTTPException(status_code=409, detail="Knowledge base is empty. Add a document first.")
    results = kb.retrieve(request.question, request.top_k)
    return generator.generate(request.question, results)
