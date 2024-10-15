from quartic_sdk.pipelines.sources.base_source import SourceApp
from quartic_sdk.pipelines.connector_app import CONNECTOR_CLASS, get_truststore_password
from pydantic import BaseModel
import os
import json


class EventHubConfig(BaseModel):
    EVENT_HUB_CONNECTION_STRING: str



class EventHubSource(SourceApp):
    connector_class: str = CONNECTOR_CLASS.EventHub.value
    connector_config: EventHubConfig
    topic_to_push_to: str = None
    

    def process_records(self, spark, batch_df):
        if batch_df.empty:
            return
        if self.transformation:
            batch_df = self.transformation(batch_df)
        self.write_data(spark, batch_df)
        

        
    def start(self, id, kafka_topics, source=[]):
        self.id = id
        self.topic_to_push_to = kafka_topics[0]
        from pyspark.sql import SparkSession

        spark = SparkSession.builder \
            .appName(f"SourceConnector_{self.id}").getOrCreate()
        connection_string = self.connector_config.EVENT_HUB_CONNECTION_STRING
        ehConf = {
        'eventhubs.connectionString' : spark._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(connection_string),
        }

        df = spark \
        .readStream \
        .format("eventhubs") \
        .options(**ehConf) \
        .load()
        query = df.selectExpr("cast(body as string) as value") \
            .writeStream.foreachBatch(
                lambda df, epochId: self.process_records(spark, df.toPandas())) \
            .option("checkpointLocation", os.environ.get('SPARK_CHECKPOINTS_LOCATION', f'/app/data/pipelines/checkpoints/{self.id}')) \
            .start()
        
        query.awaitTermination()
