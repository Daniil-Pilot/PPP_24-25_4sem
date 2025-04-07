from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Corpus(Base):
    __tablename__ = "corpus"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    text = Column(String)
