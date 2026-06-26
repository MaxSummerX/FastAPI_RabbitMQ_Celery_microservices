import logging

from app.domain.repositories.users import IUserRepositorySync
from app.infrastructure.email.protocol import Email, IEmailSender


logger = logging.getLogger(__name__)


class MailingService:
    """Сервис рассылки email пользователям."""

    def __init__(self, user_repo: IUserRepositorySync, email_sender: IEmailSender) -> None:
        self.user_repo = user_repo
        self.email_sender = email_sender

    def send_email(self, email: Email) -> None:
        """
        Отправляет email одному пользователю.

        Args:
            email: Объект письма (to, subject, body)
        """
        self.email_sender.send_email(email)

    def bulk_send_emails(self, subject: str, body: str) -> None:
        """
        Рассылает email всем пользователям из базы.

        Args:
            subject: Тема письма
            body: Текст письма
        """
        for user in self.user_repo.get_all():
            try:
                self.send_email(Email(subject=subject, body=body, to=user.email))
            except Exception as exc:
                logger.error("Ошибка при отправке %s: %s", user.email, exc)
