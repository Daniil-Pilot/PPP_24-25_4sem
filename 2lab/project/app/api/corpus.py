from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.cruds import corpus
from app.schemas.corpus import CorpusCreate, Corpus
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload_corpus", response_model=Corpus)
def upload_corpus(corpus_create: CorpusCreate, db: Session = Depends(get_db)):
    return corpus.create_corpus(db=db, name=corpus_create.name, text=corpus_create.text)

@router.get("/corpuses", response_model=list[Corpus])
def get_corpuses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return corpus.get_all_corpuses(db=db, skip=skip, limit=limit)
