from fastapi import FastAPI
from app.api import corpus, search

app = FastAPI()

app.include_router(corpus.router, prefix="/corpus", tags=["corpus"])
app.include_router(search.router, prefix="/search", tags=["search"])
