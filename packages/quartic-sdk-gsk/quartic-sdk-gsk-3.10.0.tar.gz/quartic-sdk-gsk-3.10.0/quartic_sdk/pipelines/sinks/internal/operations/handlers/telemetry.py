import logging
import json
from typing import Tuple, Type

from confluent_kafka import Producer

from quartic_sdk.pipelines.sinks.internal.operations.handlers.base import (
    OperationHandler,
)
from quartic_sdk.pipelines.sinks.internal.operations.operations import TagTelemetry
from quartic_sdk.utilities.kafka import KafkaProducerFactory


logger = logging.getLogger(__name__)
TELEMETRY_TOPIC = "flat_telemetry"


class TagTelemetryHandler(OperationHandler[TagTelemetry]):
    @classmethod
    def get_optype(cls):
        return TagTelemetry

    def handle(self, operations: list[TagTelemetry]):
        producer = KafkaProducerFactory.get_producer()
        success, failed = [], []

        for op in operations:
            message = json.dumps(
                {
                    "timestamp": op.timestamp,
                    "tag": op.tag,
                    "value": op.value,
                    "edgeconnector": op.edgeconnector,
                }
            )

            def callback(err, msg):
                if err:
                    logger.error(f"Error writing to kafka: {err}")
                    failed.append(op)
                else:
                    success.append(op)

            producer.produce(
                TELEMETRY_TOPIC,
                key=str(op.edgeconnector),
                value=message,
                on_delivery=callback,
            )

        try:
            producer.flush()
        except Exception:
            logger.exception(f"Producer flush failed")
        return success, failed
