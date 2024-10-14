import logging
import json
from datetime import datetime

import pandas as pd
from confluent_kafka import Consumer, Producer, KafkaError

from quartic_sdk.pipelines.settings import settings

logger = logging.getLogger(__name__)


class KafkaBatchConsumer:
    """
    Consumes batches from kafka, returns the batch as a DataFrame, and implements manual offset commits
    """

    def __init__(
        self,
        conf: dict,
        topics: list[str],
        batch_size: int = 2000,
        batch_timeout: int = 5,
        poll_timeout: int = 3,
    ):
        self.conf = conf
        self.consumer = Consumer(conf)
        self.consumer.subscribe(topics)
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.poll_timeout = poll_timeout

    def get(self):
        """
        Retrieve an event batch DataFrame
        """
        messages = []
        # Block until we receive a message batch
        while not messages:
            messages = self._consume_batch()
        return self._to_df(messages)

    def commit(self):
        """
        Commit consumer offset
        """
        if self.conf.get("enable.auto.commit", True):
            logger.warning("Auto commit enabled. Ignoring commit attempt")
            return
        self.consumer.commit(asynchronous=False)

    def _consume_batch(self):
        messages = []

        batch_start = datetime.now()
        for _ in range(self.batch_size):
            message = self.consumer.poll(timeout=self.poll_timeout)
            logger.info(f"Got message {message} {len(messages)=}")

            if message is None and not messages:
                batch_start = datetime.now()

            if message is not None:
                if message.error():
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logger.exception(
                            f"Error during kafka message consumption: {message.error()}"
                        )
                        break
                else:
                    messages.append(message)

            time_elapsed = (datetime.now() - batch_start).total_seconds()
            if time_elapsed >= self.batch_timeout:
                logger.info(f"Returning current batch due to batch timeout")
                return messages

        return messages

    def _to_df(self, messages: list):
        messages = [
            {
                **json.loads(m.value().decode("utf-8")),
                "topic": m.topic(),
            }
            for m in messages
        ]
        return pd.DataFrame(messages)


class KafkaProducerFactory:
    producer = None

    @classmethod
    def get_producer(cls):
        if cls.producer is None:
            cls.producer = Producer(
                {
                    **settings.get_kafka_config(),
                    "linger.ms": 50,
                    "queue.buffering.max.ms": 50,
                    "batch.size": 2000,
                }
            )
        return cls.producer
