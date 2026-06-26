from dataclasses import asdict
from uuid import UUID

import aio_pika
import orjson
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractRobustConnection

from app.domain.events.base import BaseEvent
from app.infrastructure.message_brokers.protocols.publisher import IEventPublisher


class RabbitEventPublisher(IEventPublisher):
    def __init__(self, url: str, exchange_name: str) -> None:
        self.url = url
        self.exchange_name = exchange_name
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None
        self._exchange: AbstractExchange | None = None

    async def start(self) -> None:
        """Устанавливает соединение с брокером"""
        self._connection = await aio_pika.connect_robust(self.url)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            self.exchange_name, aio_pika.ExchangeType.DIRECT, durable=True
        )

    async def stop(self) -> None:
        """Закрывает соединение с брокером."""
        if self._connection is not None:
            await self._connection.close()
        self._connection = None
        self._channel = None
        self._exchange = None

    async def publish(self, event: BaseEvent) -> None:
        """Публикует событие в брокер."""
        if self._exchange is None:
            raise RuntimeError("Publisher not started")
        data: bytes = orjson.dumps(self._to_dict(event))
        message = aio_pika.Message(
            body=data,
            message_id=str(event.event_id),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await self._exchange.publish(message, routing_key=event.event_title)

    def _to_dict(self, event: BaseEvent) -> dict:
        """Преобразует событие в словарь для публикации в RabbitMQ."""
        data = asdict(event)
        data["event_title"] = event.event_title
        for key, value in data.items():
            if isinstance(value, UUID):
                data[key] = str(value)
        return data
