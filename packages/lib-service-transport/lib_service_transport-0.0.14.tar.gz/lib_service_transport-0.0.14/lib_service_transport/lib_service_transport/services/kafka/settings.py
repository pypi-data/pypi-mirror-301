from socket import gethostname

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class KafkaSettings(BaseSettings):
    BOOTSTRAP_SERVERS: str = Field(default='localhost:9092')
    CLIENT_ID: str | int = Field(default_factory=gethostname)
    GROUP_ID: str = Field(default='foo')
    AUTO_OFFSET_RESET: str = Field(default='smallest')
    ENABLE_AUTO_COMMIT: bool = Field(default=False)

    # topics
    TOPIC_ORDER: str  # TODO: удалить!
    TOPIC_SALES_ORDER: str
    TOPIC_ORGANIZATION: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        env_prefix='KAFKA_',
    )
