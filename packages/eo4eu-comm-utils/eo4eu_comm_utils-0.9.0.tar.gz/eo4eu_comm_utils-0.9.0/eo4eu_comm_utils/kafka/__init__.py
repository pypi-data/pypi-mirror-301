import logging

default_logger = logging.getLogger(__name__)


class MockMessage:
    def __init__(self, value: str = "", topic: str = "unknown"):
        self._value = value
        self._topic = topic

    def value(self) -> bytes:
        return self._value.encode("utf-8")

    def topic(self) -> str:
        return self._topic

    def error(self) -> bool:
        return False


from .consumer import KafkaConsumer
from .producer import KafkaProducer

