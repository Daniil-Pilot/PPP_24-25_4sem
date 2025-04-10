from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.cruds.corpus import create_corpus, get_corpus, get_all_corpuses
from app.db.session import get_db
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.corpus import CorpusCreate, Corpus, CorpusList, SearchRequest, SearchResponse
from app.services.fuzzy_search import search_text

router = APIRouter()

@router.post("/upload_corpus", response_model=dict)
def upload_corpus(
    corpus: CorpusCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_corpus = create_corpus(db=db, corpus=corpus, user_id=current_user.id)
    return {
        "corpus_id": db_corpus.id,
        "message": "Corpus uploaded successfully"
    }

@router.get("/corpuses", response_model=CorpusList)
def get_corpuses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    corpuses = get_all_corpuses(db)
    return {
        "corpuses": [{"id": corpus.id, "name": corpus.name} for corpus in corpuses]
    }

@router.post("/search_algorithm", response_model=SearchResponse)
def search_algorithm(
    search_request: SearchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    corpus = get_corpus(db, corpus_id=search_request.corpus_id)
    if not corpus:
        raise HTTPException(status_code=404, detail="Corpus not found")
    
    if search_request.algorithm not in ["levenshtein", "damerau_levenshtein"]:
        raise HTTPException(status_code=400, detail=f"Algorithm {search_request.algorithm} not supported")
    

    execution_time, results = search_text(
        corpus.text, 
        search_request.word, 
        search_request.algorithm
    )
    
    return {
        "execution_time": execution_time,
        "results": results
    }
