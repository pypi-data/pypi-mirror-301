from pydantic import BaseModel
from quartic_sdk.pipelines.sinks.base_sink import SparkSinkApp
from quartic_sdk.pipelines.connector_app import CONNECTOR_CLASS


class EventHubConfig(BaseModel):
    EVENT_HUB_CONNECTION_STRING: str

class EventHubSink(SparkSinkApp):
    connector_class: str = CONNECTOR_CLASS.EventHub.value
    connector_config: EventHubConfig
    
    def write_data(self, batch_df, spark):
        if batch_df.empty:
            return
        # Todo: Data Format to change to
        batch_df = batch_df.rename(columns={'value': 'body'})
        messages_df = spark.createDataFrame(batch_df)
        connection_string = self.connector_config.EVENT_HUB_CONNECTION_STRING
        ehConf = {
        'eventhubs.connectionString' : spark._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(connection_string),
        }
        messages_df \
            .select("body")\
            .write \
            .format("eventhubs") \
            .options(**ehConf) \
            .option("checkpointLocation", f"/app/data/pipelines/checkpoints/{self.id}/eventhub") \
            .save()
