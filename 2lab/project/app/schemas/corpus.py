from pydantic import BaseModel

class CorpusBase(BaseModel):
    name: str
    text: str

class CorpusCreate(CorpusBase):
    pass

class Corpus(CorpusBase):
    id: int

    class Config:
        orm_mode = True
