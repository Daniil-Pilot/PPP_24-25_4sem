from fastapi import APIRouter, Depends
from app.schemas.user import FuzzySearchRequest
from app.celery.tasks import run_fuzzy_search
import uuid
from fastapi import APIRouter

api_router = APIRouter()

@api_router.post("/search")
async def start_search(request: FuzzySearchRequest):
    task_id = str(uuid.uuid4())
    run_fuzzy_search.delay(request.word, request.algorithm, task_id)
    return {"task_id": task_id, "status": "submitted"}
