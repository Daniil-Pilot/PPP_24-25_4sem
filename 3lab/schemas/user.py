from pydantic import BaseModel

class FuzzySearchRequest(BaseModel):
    word: str
    algorithm: str