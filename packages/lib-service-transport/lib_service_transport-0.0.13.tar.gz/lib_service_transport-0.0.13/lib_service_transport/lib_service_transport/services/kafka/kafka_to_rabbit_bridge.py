from abc import abstractmethod

from confluent_kafka import Consumer

from . import OrderCreationMessage
from .base_consumer import BaseConsumerKafka
from ..rabbit import BasePublisherRabbit
from ..rabbit import RabbitMQSettings


class MessageTransferKafkaToRabbitService(BaseConsumerKafka):
    def __init__(
            self,
            settings: RabbitMQSettings,
            consumer: Consumer,
            publisher_rabbit: BasePublisherRabbit,
    ) -> None:
        super().__init__(consumer=consumer)
        self._publisher_rabbit = publisher_rabbit
        self._settings = settings

    @abstractmethod
    def callback(self, outgoing_message: OrderCreationMessage) -> None:
        pass
