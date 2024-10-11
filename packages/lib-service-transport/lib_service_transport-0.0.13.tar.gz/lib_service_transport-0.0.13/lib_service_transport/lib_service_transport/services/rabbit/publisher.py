from typing import Any

from orjson import dumps
from pika import BasicProperties
from pika.delivery_mode import DeliveryMode
from pika.exceptions import ChannelClosed
from pika.exceptions import NackError
from pika.exceptions import UnroutableError
from pydantic import BaseModel

from . import BasePublisherRabbit


class PublisherRabbit(BasePublisherRabbit):

    def publish_message(
            self,
            outgoing_message: BaseModel,
            exchange_name: str,
            routing_key: str,
            order_queue: str,
    ) -> Any:
        """Отправляет сообщения в RabbitMQ."""

        try:
            self.check_exists_queue(queue_name=order_queue)
        except ChannelClosed:
            pass

        properties = BasicProperties(
            delivery_mode=DeliveryMode.Persistent,
            content_type='application/json',
        )

        try:
            self._channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                properties=properties,
                body=dumps(outgoing_message.model_dump()),
            )
        except UnroutableError:
            raise
        except NackError:
            raise
