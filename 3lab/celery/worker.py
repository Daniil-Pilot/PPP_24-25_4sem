from celery import Celery
from app.core.config import settings

celery_app = Celery(
    'worker',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.task_routes = {
    'app.celery.tasks.*': {'queue': 'default'}
}
