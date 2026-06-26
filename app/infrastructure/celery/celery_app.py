from celery import Celery

from app.config import settings


app = Celery(
    "task_service",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL,
    timezone=settings.TIMEZONE,
    include=["app.infrastructure.celery.tasks"],
    result_expires=3600,
)
