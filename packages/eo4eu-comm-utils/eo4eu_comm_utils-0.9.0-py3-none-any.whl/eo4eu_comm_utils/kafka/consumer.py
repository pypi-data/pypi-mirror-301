import time
from logging import Logger
from typing import Callable
from confluent_kafka import Consumer

from . import default_logger, MockMessage


class MockConsumer:
    def __init__(self, config: dict|None):
        if config is None:
            config = {}

        self.message = config.get("message", "")
        self.topic = "unknown"

    def subscribe(self, topics: list[str]):
        self.topic = topics[0]

    def poll(self, timeout: int = 1.0) -> MockMessage:
        return MockMessage(self.message, self.topic)

    def close(self):
        pass


class KafkaConsumer:
    def __init__(
        self,
        topics: list[str]|str,
        config: dict,
        handler: Callable[[str],None]|None = None,
        logger: Logger|None = None,
        timeout: float = 1.0,
        mock: bool = False,
        mock_config: dict|None = None
    ):
        if not isinstance(topics, list):
            topics = [topics]
        if logger is None:
            logger = default_logger

        if mock:
            self.consumer = MockConsumer(mock_config)
        else:
            self.consumer = Consumer(config)
        self.mock = mock
        self.topics = topics
        self.handler = handler
        self.logger = logger
        self.timeout = timeout

    def consume(self, handler: Callable[[str],None]|None = None):
        if handler is None:
            handler = self.handler

        try:
            self.consumer.subscribe(self.topics)
            while True:
                msg = self.consumer.poll(timeout = self.timeout)
                if msg is None or msg.error():
                    continue

                decoded_msg = msg.value().decode("utf-8")
                self.logger.info(
                    f"New message received: {decoded_msg} from topic {msg.topic()}"
                )
                handler(decoded_msg)
                if self.mock:
                    break
        finally:
            self.consumer.close()
