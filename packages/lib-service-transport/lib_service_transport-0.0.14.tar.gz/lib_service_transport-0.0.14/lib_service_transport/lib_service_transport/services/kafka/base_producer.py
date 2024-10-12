from confluent_kafka import Producer

from .event_types_enum import EventTypeEnum


class ProducerKafka:
    def __init__(self, producer: Producer):
        self._producer = producer

    def produce_message(
            self,
            topic: str,
            message: str | bytes,
            event_type: EventTypeEnum,
    ) -> None:

        try:
            self._producer.produce(
                topic=topic,
                value=message,
                key=event_type,
                callback=self.delivery_report,
            )
            self._producer.poll(0)
        except Exception:
            pass

    def flush(self) -> None:
        self._producer.flush()

    @classmethod
    def delivery_report(cls, err, msg) -> None:
        if err is not None:
            pass
        else:
            pass
