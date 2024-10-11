from abc import ABC, abstractmethod

from pika import BlockingConnection
from pika import ConnectionParameters
from pika import PlainCredentials


class BaseQueueAgent(ABC):
    """Базовый класс"""

    def __init__(self, settings: 'RabbitMQSettings'):
        """
            Инициализация класса
        :param settings: настройки сервера RabbitMQ
        """
        credentials = PlainCredentials(
            username=settings.rabbit.default_user,
            password=settings.rabbit.default_pass,
        )
        self._connection_params = ConnectionParameters(
            host=settings.rabbit.host,
            port=settings.rabbit.port,
            credentials=credentials,
            heartbeat=settings.rabbit.heartbeat,
        )

        self._connection = None
        self._channel = None

    def connect(self) -> None:
        """Соединение с сервером RabbitMQ."""
        self._connection = BlockingConnection(parameters=self._connection_params)
        self._channel = self._connection.channel()

    def close_connection(self) -> None:
        """Закрытие соединения с RabbitMQ."""
        if self._connection is not None:
            self._connection.close()

    @abstractmethod
    def setup(self, **kwargs: str | int) -> None:
        """Настройка обменника (exchange), очереди (queue)."""
        pass

    @abstractmethod
    def run(self, **kwargs: str | int) -> None:
        """Запуск."""
        pass
