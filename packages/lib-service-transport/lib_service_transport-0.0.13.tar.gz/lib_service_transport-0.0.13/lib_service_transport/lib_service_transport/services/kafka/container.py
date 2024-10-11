from confluent_kafka.cimpl import Message

from .message_handler import MessageHandlerKafka
from .base_consumer import BaseConsumerKafka


class ContainerConsumersKafka(BaseConsumerKafka):
    consumers: dict[str, MessageHandlerKafka] = {}

    def add_consumer(
            self,
            event_type: str,
            consumer: MessageHandlerKafka,
    ) -> None:
        self.consumers[event_type] = consumer

    def get_handler(self, event_type: str) -> MessageHandlerKafka:
        try:
            return self.consumers[event_type]
        except KeyError:
            pass

    def on_request(self, message: Message) -> None:
        event_type = message.key()
        handler = self.get_handler(event_type.decode())
        incoming_message = self.get_incoming_message(
            value=message.value(),
            incoming_message_schema=handler.incoming_message_schema,
        )
        handler.on_request(incoming_message=incoming_message)
