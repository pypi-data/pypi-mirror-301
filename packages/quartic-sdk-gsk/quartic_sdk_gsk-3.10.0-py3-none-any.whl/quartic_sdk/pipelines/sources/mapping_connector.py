import pandas as pd
from typing import Dict, Optional

from quartic_sdk import GraphqlClient
from quartic_sdk.pipelines.sources.base_source import SourceApp
from quartic_sdk.utilities.kafka import KafkaBatchConsumer
from quartic_sdk.pipelines.settings import settings
from quartic_sdk.pipelines.sources.mapping.utils import get_processor
from quartic_sdk.pipelines.sources.kafka_producer import KafkaConnector

GET_CONNECTORS_QUERY = """
query MyQuery($ids: [String!]) {
  ConnectorApp(id_In: $ids) {
    id
    name
    connectorClass
  }
}
"""


class MappingConntector(SourceApp):
    source_map: Dict[str, str] = {}
    kafka_producer: Optional[KafkaConnector] = None
    sink_topic: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    def start(self, id, kafka_topics, source):
        self.id = id
        self.source = source
        self.kafka_producer = KafkaConnector()
        client = GraphqlClient.get_graphql_client_from_env()
        # Fetch source connector details
        response = client.execute_query(
            GET_CONNECTORS_QUERY,
            {"ids": [str(s) for s in source]},
        )
        self.source_map = {}
        for connector in response["data"]["ConnectorApp"]:
            self.source_map[connector["id"]] = connector["connectorClass"]

        self.logger.info(f"Loaded source map {self.source_map}")

        # Start kafka consumer
        self.sink_topic = next(
            filter(lambda t: t.split("_")[1] == str(self.id), kafka_topics)
        )
        source_topics = [t for t in kafka_topics if t != self.sink_topic]
        consumer = KafkaBatchConsumer(
            conf={
                **settings.get_kafka_config(),
                "group.id": f"MappingConnector_{id}",
                "auto.offset.reset": "latest",
                "enable.auto.commit": False,
                "receive.message.max.bytes": 2000000000,
            },
            topics=source_topics,
        )

        while True:
            df = consumer.get()
            self.logger.info(f"DF: {df}")
            self.process_records(df)
            consumer.commit()

    def process_records(self, df: pd.DataFrame):
        df["source_class"] = df["topic"].apply(
            lambda t: self.source_map[t.split("_")[1]]
        )
        groups = df.groupby("source_class")
        for source_class, group_df in groups:
            messages = get_processor(source_class).process(group_df, self.id)
            self.logger.info(f"Got enriched messages {len(messages)}")
            for key, message in messages:
                self.kafka_producer.upload_data(message, self.sink_topic, key)
