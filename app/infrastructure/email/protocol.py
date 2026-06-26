from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Email:
    to: str
    subject: str
    body: str


class IEmailSender(ABC):
    @abstractmethod
    def send_email(self, email: Email) -> None:
        """Отправляет email."""
        pass
