from typing import final
from abc import abstractmethod
import pandas as pd
import os
from quartic_sdk.pipelines.connector_app import ConnectorApp, CONNECTOR_CLASS, get_truststore_password
from quartic_sdk.utilities.kafka import KafkaBatchConsumer
from quartic_sdk.pipelines.settings import settings
from pydantic import validator


SINK_CONNECTOR_PROTOCOLS = [
    CONNECTOR_CLASS.Http.value,
    CONNECTOR_CLASS.HttpSoap.value,
    CONNECTOR_CLASS.External.value,
    CONNECTOR_CLASS.Custom.value,
    CONNECTOR_CLASS.EventHub.value,
    CONNECTOR_CLASS.Internal.value,
]


class SinkApp(ConnectorApp):
    connector_type: str = "SINK"
    connector_class: str = CONNECTOR_CLASS.Custom.value

    @abstractmethod
    def start(self, id: int, kafka_topics: list[str], source: list[int]):
        raise NotImplemented

    @validator("connector_class")
    def validate_option(cls, v):
        assert v in SINK_CONNECTOR_PROTOCOLS, f"Invalid protocol for Sink Connector {v}"
        return v

    @abstractmethod
    def write_data(self, batch_df: pd.DataFrame, spark):
        raise NotImplementedError

    @final
    def process_records(self, batch_df, spark):
        print(f"Transformation is {self.transformation}")
        if self.transformation:
            batch_df = self.transformation(batch_df)
        self.write_data(batch_df, spark)


class SparkSinkApp(SinkApp):
    """
    Spark application connector sink
    """

    @final
    def start(self, id: int, kafka_topics: list[str], source: list[int]):
        self.id = id
        self.source = source

        from pyspark.sql import SparkSession

        spark = SparkSession.builder.appName(f"SinkConnector_{self.id}").getOrCreate()

        df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", os.environ.get('KAFKA_BROKER_URL', 'broker:9092')) \
            .option("auto.offset.reset", "latest") \
            .option("subscribe", kafka_topics[0]) \
            .option("maxOffsetsPerTrigger", int(os.environ.get('KAFKA_POLL_BATCH_SIZE', '3200000'))) \
            .option("kafkaConsumer.pollTimeoutMs", int(os.environ.get('KAFKA_POLL_TIMEOUT_MS', '5000'))) \
            .option("failOnDataLoss", "false") \
            .option("kafka.security.protocol", os.environ.get('KAFKA_SECURITY_PROTOCOL')) \
            .option("kafka.sasl.mechanism", os.environ.get('KAFKA_SASL_MECHANISM')) \
            .option("kafka.sasl.jaas.config", f'org.apache.kafka.common.security.scram.ScramLoginModule required username="{os.environ.get("KAFKA_SASL_USERNAME")}" password="{os.environ.get("KAFKA_SASL_PASSWORD")}";') \
            .option("kafka.ssl.endpoint.identification.algorithm", os.environ.get('KAFKA_SSL_ALGORITHM', ' ')) \
            .option("kafka.ssl.truststore.location", os.environ.get('KAFKA_SSL_TRUSTSTORE_LOCATION'))\
            .option("kafka.ssl.truststore.password", get_truststore_password())\
            .option("kafka.ssl.truststore.type", os.environ.get('KAFKA_SSL_TRUSTSTORE_TYPE')) \
            .load()

        query = df.selectExpr("CAST(value AS STRING)") \
        .writeStream.foreachBatch(
        lambda df, epochId: self.process_records(df.toPandas(), spark))\
        .option("checkpointLocation", os.environ.get('SPARK_CHECKPOINTS_LOCATION', f'/app/data/pipelines/checkpoints/{self.id}'))\
        .start()
        query.awaitTermination()
    
    # def _set_batch_status():
    #     # Responsible for avoiding reprocessing of the data in case of mid batch failure
    #     # TODO: Implement this in next version
    #     pass


class KafkaSinkApp(SinkApp):
    @final
    def start(self, id: int, kafka_topics: list[str], source: list[int]):
        self.id = id
        self.source = source
        consumer = KafkaBatchConsumer(
            conf={
                **settings.get_kafka_config(),
                "group.id": f"KafkaSinkApp_{id}",
                "auto.offset.reset": "latest",
                "enable.auto.commit": False,
            },
            topics=kafka_topics,
        )

        while True:
            df = consumer.get()
            self.logger.info(f"DF: {df}")
            self.process_records(df)
            consumer.commit()
