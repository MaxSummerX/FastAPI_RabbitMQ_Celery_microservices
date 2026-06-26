from app.application.services.factories import mailing_service_factory
from app.infrastructure.celery.celery_app import app


@app.task
def send_emails(subject: str, body: str) -> None:
    """
    Задача Celery для рассылки email всем пользователям.

    Args:
        subject: Тема письма
        body: Текст письма
    """

    with mailing_service_factory() as mail_service:
        mail_service.bulk_send_emails(subject, body)
