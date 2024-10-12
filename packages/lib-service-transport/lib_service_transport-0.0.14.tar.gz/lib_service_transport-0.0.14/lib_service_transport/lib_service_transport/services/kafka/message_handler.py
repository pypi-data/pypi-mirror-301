from abc import abstractmethod

from pydantic import BaseModel


class MessageHandlerKafka:
    """Базовый класс для обработки сообщений"""

    incoming_message_schema: BaseModel = NotImplemented

    @abstractmethod
    def on_request(self, incoming_message: BaseModel) -> None:
        pass
