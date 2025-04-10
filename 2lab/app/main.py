from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import users, search

app = FastAPI(title="Fuzzy Search API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Включение API роутеров
app.include_router(users.router, tags=["users"])
app.include_router(search.router, tags=["search"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Fuzzy Search API"}
