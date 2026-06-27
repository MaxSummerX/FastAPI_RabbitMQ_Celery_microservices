from celery import Celery
from celery.schedules import crontab

from app.config import settings


app = Celery(
    "task_service",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL,
    timezone=settings.TIMEZONE,
    include=["app.infrastructure.celery.tasks"],
    result_expires=3600,
)

app.conf.beat_schedule = {
    "daily_email_sender": {
        "task": "app.infrastructure.celery.tasks.daily_email_sender",
        "schedule": crontab(hour=9, minute=0),  # minute="*/1" для тестирования
    },
}
