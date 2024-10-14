import time
import json
from typing import Optional

from .base_sink import SparkSinkApp
from quartic_sdk.pipelines.connector_app import CONNECTOR_CLASS
from quartic_sdk.pipelines.config.opcua import OPCUASecurityConfig, OPCUASinkConfig
from quartic_sdk.utilities.opcua import get_client, get_security_string
from pydantic import BaseModel, PrivateAttr
import pandas as pd
from opcua import Client
from opcua.ua import DataValue

MAX_RETRY_ATTEMPTS = 3


class OPCUASinkApp(SparkSinkApp):
    """
    OPCUA write sink application.

    Sample event:
        {
          "node": "ns=3;i=1907",
          "values": [2,45,5,6],
        }
    """

    connector_class: str = CONNECTOR_CLASS.Opcua.value
    connector_config: OPCUASinkConfig
    _client: Optional[Client] = PrivateAttr(default=None)
    _nodes: dict = PrivateAttr(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    def __connect_opcua(self):
        try:
            if not self._client:
                self._client = get_client(self.connector_config)
                security_string = get_security_string(self.connector_config)
                if security_string:
                    self._client.set_security_string(security_string)
                self._client.connect()
                self.logger.info(
                    f"Connected to OPC UA server at {self.connector_config.opcua_url}"
                )
        except Exception as e:
            self.logger.exception(f"Failed to connect to OPC UA server")
            raise e

    def __get_opcua_node(self, node_id: str):
        while True:
            try:
                if node_id not in self._nodes:
                    self._nodes[node_id] = self._client.get_node(node_id)
                return self._nodes[node_id]
            except Exception as e:
                self.logger.exception(f"Failed to get OPC UA node {node_id}")
                self.__connect_opcua()
                time.sleep(self.WAIT_BEFORE_RETRY_SECONDS)
                continue

    def validate_transformation_output(**kwargs):
        batch_dict = kwargs["data"]
        assert isinstance(
            batch_dict, dict
        ), "Output of transformation/Input to write_data must be a dictionary"
        for key, value in batch_dict.items():
            assert isinstance(
                key, str
            ), "Key of the transformation output dictionary must be a string (node id)"
            assert isinstance(
                value, list
            ), "Values of the transformation output dictionary must be a list (list[DataValue])"
            for data_value in value:
                assert isinstance(
                    data_value, DataValue
                ), "Values of the transformation output dictionary must be a list of DataValue objects"

    def write_data(self, batch_df: pd.DataFrame, spark):
        if batch_df is None or batch_df.empty:
            return
        self.__connect_opcua()
        messages = [json.loads(m) for m in batch_df["value"]]

        for message in messages:
            try:
                node_name = message["node"]
                values = message["values"]
                node = self.__get_opcua_node(node_name)
                for value in values:
                    self.__write_value(node, value)
            except Exception:
                self.logger.exception(f"Could not process message {message}")

    def __write_value(self, node, value, max_retry_attempts=MAX_RETRY_ATTEMPTS):
        attempts = 0
        while attempts < max_retry_attempts:
            attempts += 1
            try:
                node.set_value(value)
                self.logger.info(f"Write to {node} successful")
                break
            except Exception as e:
                self.logger.exception(
                    f"Error while writing to OPCUA node {node}. ({attempts}/{max_retry_attempts})"
                )
                self.__connect_opcua()
                time.sleep(self.WAIT_BEFORE_RETRY_SECONDS)
