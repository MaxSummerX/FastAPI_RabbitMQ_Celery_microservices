from collections.abc import Generator
from contextlib import contextmanager

from app.application.services.mailing_service import MailingService
from app.infrastructure.database.connection import sync_session_factory
from app.infrastructure.email.email import LoggingEmailSender
from app.infrastructure.persistence.sqlalchemy.user_repository import UserSQLAlchemyRepositorySync


@contextmanager
def mailing_service_factory() -> Generator[MailingService]:
    """
    Фабрика для создания сервиса рассылки email.
    """
    with sync_session_factory() as session:
        repo = UserSQLAlchemyRepositorySync(session)
        email_sender = LoggingEmailSender()
        service = MailingService(repo, email_sender)
        yield service
