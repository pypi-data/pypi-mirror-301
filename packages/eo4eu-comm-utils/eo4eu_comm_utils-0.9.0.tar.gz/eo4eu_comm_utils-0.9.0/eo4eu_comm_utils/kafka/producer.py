from logging import Logger
from typing import Callable
from confluent_kafka import Producer

from . import default_logger, MockMessage


class MockProducer:
    def __init__(self, config: dict):
        pass

    def produce(
        self,
        topic: str = "unknown",
        key: str = "",
        value: MockMessage|None = None,
        callback: Callable[[str,MockMessage],None]|None = None
    ):
        if callback is None:
            callback = lambda err, msg: None
        if value is None:
            value = MockMessage()

        callback(None, MockMessage(value, topic))

    def flush(self):
        pass


class KafkaProducer:
    def __init__(
        self,
        topic: str,
        config: dict,
        logger: Logger|None = None,
        mock: bool = False
    ):
        if logger is None:
            logger = default_logger

        self.topic = topic
        self.logger = logger
        if mock:
            self.producer = MockProducer(config)
        else:
            self.producer = Producer(config)

    def set_topic(self, topic: str):
        self.topic = topic

    def send_message(self, key: str, msg: str, topic: str|None = None):
        if topic is None:
            topic = self.topic

        def _acked(err, msg):
            if err is not None:
                self.logger.error(
                    f"Failed to deliver message: {str(msg.value())}: {str(err)}"
                )
            else:
                self.logger.info(
                    f"Message produced: {str(msg.value())} on topic {topic}"
                )

        self.producer.produce(topic, key=key, value=msg, callback=_acked)
        self.producer.flush()
