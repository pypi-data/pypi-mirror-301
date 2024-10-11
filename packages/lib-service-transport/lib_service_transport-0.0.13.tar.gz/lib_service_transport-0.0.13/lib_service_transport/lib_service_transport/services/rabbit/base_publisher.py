from abc import abstractmethod
from typing import Any

from pika.exceptions import ChannelClosed
from pydantic import BaseModel

from .base_queue_agent import BaseQueueAgent


class BasePublisherRabbit(BaseQueueAgent):

    def setup(self, exchange_name: str, queue_name: str = '') -> None:
        """
        Настройка обменника (exchange), очереди (queue).
        """
        self._channel.exchange_declare(
            exchange=exchange_name,
            durable=True,
        )

        self._channel.queue_declare(
            queue=queue_name,
            exclusive=True,
            durable=True,
        )

    def run(self, exchange_name: str, queue_name: str = '') -> None:
        """Подключение к серверу RabbitMQ и настройка обменника и очереди."""
        self.connect()
        self.setup(exchange_name=exchange_name, queue_name=queue_name)

    def check_exists_queue(self, queue_name) -> None:
        """Проверка наличия очереди (queue)."""
        try:
            self._channel.queue_declare(queue=queue_name, passive=True)
        except ChannelClosed:
            raise

    @abstractmethod
    def publish_message(self, **kwargs: str | int | BaseModel) -> Any:
        """Отправляет сообщения в RabbitMQ."""
        pass
