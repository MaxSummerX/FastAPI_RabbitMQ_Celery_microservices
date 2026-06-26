from fastapi import APIRouter, status

from app.infrastructure.celery.tasks import send_emails
from app.presentation.schemas.mailing import MailRequest, MailResponse


router = APIRouter(prefix="/mailing", tags=["Mailing"])


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def newsletter(payload: MailRequest) -> MailResponse:
    """Запускает фоновую рассылку всем пользователям."""
    task = send_emails.delay(payload.subject, payload.body)  # type: ignore[attr-defined]
    return MailResponse(task_id=task.id, status=task.status)
