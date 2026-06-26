from app.config import settings
from app.infrastructure.message_brokers.rabbit.publisher import RabbitEventPublisher


def create_publisher() -> RabbitEventPublisher:
    """Создать экземпляр RabbitMQ-паблишера для публикации доменных событий"""
    return RabbitEventPublisher(url=settings.RABBIT_URL, exchange_name=settings.RABBIT_EXCHANGE)
