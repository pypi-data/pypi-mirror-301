from abc import abstractmethod

from ..kafka.base_producer import ProducerKafka
from .base_consumer import BaseConsumerRabbit


class MessageTransferRabbitToKafkaService(BaseConsumerRabbit):
    def __init__(
            self,
            settings: 'RabbitMQSettings',
            producer_kafka: ProducerKafka,
    ) -> None:
        super().__init__(settings=settings)
        self._producer_kafka = producer_kafka

    @abstractmethod
    def callback(
            self,
            ch: 'BlockingChannel',  # noqa
            method: 'Basic.Deliver',  # noqa
            properties: 'BasicProperties',
            body: bytes,
    ) -> None:
        pass
