from abc import abstractmethod

from pika import BasicProperties
from pydantic import BaseModel

from .base_queue_agent import BaseQueueAgent


class BaseConsumerRabbit(BaseQueueAgent):
    """Базовый класс Consumer"""
    EXCHANGE: str = NotImplemented
    ROUTING_KEY: str = NotImplemented
    QUEUE: str = NotImplemented
    PREFETCH_COUNT: int = NotImplemented

    incoming_message_schema: BaseModel = NotImplemented

    def setup(self) -> None:
        """
        Настройка обменника (exchange), очереди (queue), связи (bind).
        """
        self._channel.exchange_declare(
            exchange=self.EXCHANGE,
            durable=True,
        )

        self._channel.queue_declare(queue=self.QUEUE, durable=True)
        self._channel.queue_bind(
            exchange=self.EXCHANGE,
            queue=self.QUEUE,
            routing_key=self.ROUTING_KEY,
        )

        self._channel.basic_qos(prefetch_count=self.PREFETCH_COUNT)
        self._channel.basic_consume(
            queue=self.QUEUE,
            on_message_callback=self.on_request,
        )

    def acknowledge_message(self, delivery_tag) -> None:
        """
            Подтверждение получения сообщения от сервера RabbitMQ путем отправки
            ему соответствующего сообщения в ответ.
        """
        self._channel.basic_ack(delivery_tag=delivery_tag)

    def start_consuming(self) -> None:
        """Запуск."""
        self._channel.start_consuming()

    def run(self) -> None:
        """Подключение к серверу RabbitMQ и настройка обменника, очереди, связи."""
        self.connect()
        self.setup()

    @classmethod
    def get_incoming_message(
            cls,
            value: bytes,
            incoming_message_schema: BaseModel,
    ) -> BaseModel:
        try:
            return incoming_message_schema.model_validate_json(value)
        except Exception:
            pass

    @abstractmethod
    def on_request(
            self,
            ch: 'BlockingChannel',  # noqa
            method: 'Basic.Deliver',  # noqa
            properties: 'BasicProperties',
            body: bytes,
    ) -> None:
        """Принимает данные из входящих запросов и отвечает на запросы."""
        pass
