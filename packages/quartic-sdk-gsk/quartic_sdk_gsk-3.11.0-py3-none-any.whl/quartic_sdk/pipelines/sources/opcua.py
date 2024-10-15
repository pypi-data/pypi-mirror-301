
import asyncio
from asyncua import Client, ua
from pydantic import BaseModel
from pytz import timezone

from quartic_sdk.pipelines.connector_app import AppConfig
from quartic_sdk.pipelines.sources.base_source import SourceApp
from quartic_sdk.pipelines.connector_app import CONNECTOR_CLASS
from quartic_sdk.pipelines.sources.kafka_producer import KafkaConnector
from quartic_sdk.pipelines.config.opcua import OPCUASourceConfig
from quartic_sdk.utilities.opcua import get_client, get_security_string
from datetime import datetime
from typing import List, Any, Union
# Function to create and configure Spark session
def to_epoch(
            date: datetime, timezone_string: Union[str, None] = None) -> \
            Union[int, None]:
        """
        Converts datetime objects to epoch timestamps. If the timezone string is passed then that
        timezone is used to convert the object while converting to epoch value.
        :param date: An aware datetime.datetime object.
        :param timezone_string: A string representing the timezone.

        :return: The epoch timestamp value.
        """
        if not date:
            return date

        if timezone_string:

            try:
                # Label the datetime object with the user timezone. This will not do any
                # addition/subtraction.
                date = timezone(timezone_string).localize(date)

            except Exception:
                _logger.exception("Invalid timezone string found! Using system time!")

        return int(date.timestamp() * 1000.)


# OPC UA async streamer class
class Opcua(SourceApp):
    connector_class: str = CONNECTOR_CLASS.Opcua.value
    connector_config: OPCUASourceConfig
    topic_to_push_to: str = None
    kafka_producer: Any = None
    client: Any = None
    app_config = AppConfig(driver_memory_request="1g")

    async def datachange_notification(self, node, val, data):
        # This method is called whenever a value change is detected
        timestamp = None

        if data.monitored_item.Value.SourceTimestamp:
            timestamp = data.monitored_item.Value.SourceTimestamp

        elif data.monitored_item.Value.ServerTimestamp:
            timestamp = data.monitored_item.Value.ServerTimestamp
            print("Could not find SourceTimestamp for data. Using ServerTimestamp.")

        else:
            e = AttributeError("Could not find a valid timestamp for this data. Skipping it.")
            print(e)
        
            # Optionally raise it.
        if timestamp:
            json_data = {
                'timestamp': to_epoch(timestamp),
                'connector_id': self.id,
                'datapoints': [
                    {
                        'id': node.nodeid.to_string(),
                        'value': val,
                        'quality': 100
                    }
                ]
            }
        self.kafka_producer.upload_data(json_data, self.topic_to_push_to, self.id)

    async def subscribe_to_nodes(self):

        # async with self.client:
        subscription = await self.client.create_subscription(100, self)
        for node_id in self.connector_config.node_ids:
            try:
                node = self.client.get_node(node_id)
                await subscription.subscribe_data_change(node,sampling_interval=500)
            except Exception:
                self.logger.exception(f"Error while subscribing to {node_id}")
        while(True):
            await asyncio.sleep(1)
    
    async def connect(self):
        self.client = get_client(self.connector_config, Client)
        security_string = get_security_string(self.connector_config)
        if security_string:
            self.logger.info(f"Using security string {security_string}")
            await self.client.set_security_string(security_string)
        await self.client.connect()

    async def start(self, id, kafka_topics, source=[]):
        self.id = id
        self.topic_to_push_to = kafka_topics[0]
        self.kafka_producer = KafkaConnector()
        await self.connect()
        await self.subscribe_to_nodes()

