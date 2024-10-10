import os
import json
import logging
from datetime import datetime, timedelta

from confluent_kafka.cimpl import Producer

class KafkaConnector(object):
    """
    Class to upload data to Kafka
    """

    def __init__(self):
        self.kafka_config = self.get_kafka_config()
        self.kafka_producer = Producer(self.kafka_config)
        self.last_flushed = datetime.now()
        self.flush_interval = timedelta(seconds=5)

    
    def get_kafka_config(self):
        return {
                    'bootstrap.servers': os.environ.get('KAFKA_BROKER_URL', 'broker:9092'),
                    'sasl.mechanism': os.environ.get('KAFKA_SASL_MECHANISM'),
                    'security.protocol': os.environ.get('KAFKA_SECURITY_PROTOCOL'),
                    'sasl.username': os.environ.get("KAFKA_SASL_USERNAME"),
                    'sasl.password': os.environ.get("KAFKA_SASL_PASSWORD"),
                    'ssl.endpoint.identification.algorithm': ' ',
                    'message.timeout.ms': 30000,
                    'queue.buffering.max.ms': 50,
                    "topic.metadata.refresh.interval.ms": 180000,
                    'enable.ssl.certificate.verification': False,
                    'linger.ms': 50, 
                    'batch.size': 150000
                }

    async def upload_data(self, datapoint, topic, connector_id) -> None:
        """
        Transform message and write to Kafka
        """

        def delivery_callback(err, msg):
            if err:
                print(err)
            else:
                self.kafka_online = True

        self.kafka_producer.produce(topic, value=json.dumps(datapoint),
                                    key=str(connector_id), on_delivery=delivery_callback)

        if datetime.now() - self.last_flushed >= self.flush_interval:
            try:
                self.kafka_producer.flush()
                self.last_flushed = datetime.now()
            except Exception:
                logging.exception("Error while flushing producer buffer")
