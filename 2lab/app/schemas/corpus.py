from pydantic import BaseModel
from typing import List

class CorpusBase(BaseModel):
    name: str
    text: str

class CorpusCreate(CorpusBase):
    pass

class Corpus(CorpusBase):
    id: int
    
    class Config:
        orm_mode = True

class CorpusList(BaseModel):
    corpuses: List[dict]

class SearchRequest(BaseModel):
    word: str
    algorithm: str
    corpus_id: int

class SearchResult(BaseModel):
    word: str
    distance: int

class SearchResponse(BaseModel):
    execution_time: float
    results: List[SearchResult]
