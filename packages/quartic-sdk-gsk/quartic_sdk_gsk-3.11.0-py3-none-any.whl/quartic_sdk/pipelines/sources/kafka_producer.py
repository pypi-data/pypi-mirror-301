import os
import json
import logging
from datetime import datetime, timedelta

from quartic_sdk.utilities.kafka import KafkaProducerFactory

from confluent_kafka.cimpl import Producer

class KafkaConnector(object):
    """
    Class to upload data to Kafka
    """

    def __init__(self):
        self.kafka_producer = KafkaProducerFactory.get_producer()
        self.last_flushed = datetime.now()
        self.flush_interval = timedelta(seconds=5)

    def upload_data(self, datapoint, topic, key) -> None:
        """
        Transform message and write to Kafka
        """

        def delivery_callback(err, msg):
            if err:
                print(err)
            else:
                self.kafka_online = True

        self.kafka_producer.produce(topic, value=json.dumps(datapoint),
                                    key=str(key), on_delivery=delivery_callback)

        if datetime.now() - self.last_flushed >= self.flush_interval:
            try:
                self.kafka_producer.flush()
                self.last_flushed = datetime.now()
            except Exception:
                logging.exception("Error while flushing producer buffer")
