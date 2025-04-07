from fastapi import APIRouter, Depends
from app.services.fuzzy_search import levenshtein_distance, damerau_levenshtein_distance
from app.cruds import corpus
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
import time

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/search_algorithm")
async def search_algorithm(word: str, algorithm: str, corpus_id: int, db: Session = Depends(get_db)):
    db_corpus = corpus.get_corpus(db=db, corpus_id=corpus_id)
    if not db_corpus:
        return {"message": "Corpus not found"}
    
    corpus_text = db_corpus.text
    search_function = None
    if algorithm == "levenshtein":
        search_function = levenshtein_distance
    elif algorithm == "damerau_levenshtein":
        search_function = damerau_levenshtein_distance
    else:
        return {"message": "Invalid algorithm"}

    words = corpus_text.split()
    results = []
    start_time = time.time()

    for word_in_corpus in words:
        distance = search_function(word, word_in_corpus)
        results.append({"word": word_in_corpus, "distance": distance})

    end_time = time.time()
    execution_time = end_time - start_time

    return {"execution_time": execution_time, "results": results}
