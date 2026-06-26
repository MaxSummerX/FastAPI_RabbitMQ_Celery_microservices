import logging

from app.infrastructure.email.protocol import Email, IEmailSender


logger = logging.getLogger(__name__)


class LoggingEmailSender(IEmailSender):
    """Симуляция отправки email через логирование."""

    def send_email(self, email: Email) -> None:
        logger.info(
            "Email отправлен: to=%s, subject=%s, body=%s",
            email.to,
            email.subject,
            f"{email.body[:15]}...",
        )
