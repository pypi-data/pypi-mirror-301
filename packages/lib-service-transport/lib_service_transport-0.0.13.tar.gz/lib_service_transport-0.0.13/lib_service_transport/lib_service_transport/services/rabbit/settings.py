from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class RabbitMQSettings(BaseSettings):
    host: str = Field(default='0.0.0.0')
    port: int = Field(default=5672)
    default_user: str = Field(default='guest')
    default_pass: str = Field(default='guest')
    heartbeat: int = Field(default=60)

    exchange: str = Field(default='')
    prefetch_count: int = Field(default=1)

    # routing_keys
    routing_key: str = Field(default='')  # TODO: удалить !
    sales_order_routing_key: str = Field(default='')

    # queues
    order_queue: str  # TODO: удалить !
    sales_order_queue: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='RABBITMQ_',
    )
