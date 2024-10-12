import uuid

from orjson import loads
from pika import BasicProperties
from pika.delivery_mode import DeliveryMode
from pika.exceptions import ChannelClosed
from pika.exceptions import NackError
from pika.exceptions import UnroutableError
from pydantic import BaseModel

from . import BasePublisherRabbit
from . import RabbitMQSettings


class PublisherRPCRabbit(BasePublisherRabbit):
    def __init__(self, settings: 'RabbitMQSettings'):
        """
            Инициализация класса
        :param settings: настройки сервера RabbitMQ
        """
        super().__init__(settings=settings)

        self._queue = None
        self._callback_queue = None

        self._correlation_id = None
        self._response = None

    def on_response(
            self,
            ch: 'BlockingChannel',  # noqa
            method: 'Basic.Deliver',  # noqa
            properties: 'BasicProperties',
            body: bytes,
    ) -> None:
        """Получение ответа от сервера RabbitMQ"""
        if self._correlation_id == properties.correlation_id:
            self._response = body

    def setup(
            self,
            exchange_name: str,
            queue_name: str = '',
    ) -> None:
        """
        Настройка обменника (exchange), очереди (queue).
        """
        super().setup(exchange_name=exchange_name, queue_name=queue_name)

        self._queue = self._channel.queue_declare(
            queue=queue_name,
            exclusive=True,
            durable=True,
        )

        self._callback_queue = self._queue.method.queue

        self._channel.basic_consume(
            queue=self._callback_queue,
            on_message_callback=self.on_response,
        )

    def publish_message(
            self,
            outgoing_message: BaseModel,
            exchange_name: str,
            routing_key: str,
            order_queue: str,
    ) -> dict:
        """Отправляет сообщения в RabbitMQ."""
        try:
            self.check_exists_queue(queue_name=order_queue)
        except ChannelClosed:
            raise

        self._correlation_id = str(uuid.uuid4())

        properties = BasicProperties(
            reply_to=self._callback_queue,
            correlation_id=self._correlation_id,
            delivery_mode=DeliveryMode.Persistent,
            content_type='application/json',
        )

        try:
            self._channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                properties=properties,
                body=outgoing_message.model_dump_json(),
            )
        except UnroutableError:
            raise
        except NackError:
            raise

        self.waiting_response_to_rpc()

        return loads(self._response)

    def waiting_response_to_rpc(self) -> None:
        """Ожидает ответное сообщение от потребителя (consumer) RPC"""
        while self._response is None:
            self._connection.process_data_events()
