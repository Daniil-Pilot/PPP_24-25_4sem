from app.celery.worker import celery_app
from app.services.fuzzy_search import fuzzy_search
from app.websocket.manager import notify_client
import time

@celery_app.task(bind=True)
def run_fuzzy_search(self, word: str, algorithm: str, task_id: str):
    notify_client(task_id, {
        "status": "STARTED",
        "task_id": task_id,
        "word": word,
        "algorithm": algorithm
    })

    for i in range(1, 5):
        time.sleep(1)
        notify_client(task_id, {
            "status": "PROGRESS",
            "task_id": task_id,
            "progress": i * 25,
            "current_word": f"word {i}"
        })

    results = fuzzy_search(word, algorithm)

    notify_client(task_id, {
        "status": "COMPLETED",
        "task_id": task_id,
        "execution_time": 4.0,
        "results": results
    })

    return {
        "status": "COMPLETED",
        "task_id": task_id,
        "results": results
    }
