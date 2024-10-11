from typing import Callable

from pika import BasicProperties
from pika.exceptions import UnroutableError

from .base_consumer import BaseConsumerRabbit


# TODO: Его можно удалять потому что метод on_request лучше реализовывать каждый раз.
class ConsumerRPCRabbit(BaseConsumerRabbit):
    """Базовый класс Consumer для RPC"""

    callback: Callable = NotImplemented

    def on_request(
            self,
            ch: 'BlockingChannel',  # noqa
            method: 'Basic.Deliver',  # noqa
            properties: 'BasicProperties',
            body: bytes,
    ) -> None:
        """Принимает данные из входящих запросов и отвечает на запросы."""

        incoming_message = self.get_incoming_message(
            value=body,
            incoming_message_schema=self.incoming_message_schema,
        )

        response = self.callback(incoming_message=incoming_message)

        try:
            self._channel.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                properties=BasicProperties(correlation_id=properties.correlation_id),
                body=response
            )
        except UnroutableError:
            raise

        self.acknowledge_message(delivery_tag=method.delivery_tag)
