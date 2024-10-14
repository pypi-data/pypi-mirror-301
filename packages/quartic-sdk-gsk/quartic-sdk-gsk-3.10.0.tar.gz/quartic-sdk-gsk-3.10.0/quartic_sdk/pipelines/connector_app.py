import logging
from pydantic import BaseModel, PrivateAttr
import sys
from typing import final
from quartic_sdk.model.helpers import ModelUtils
from pydantic import BaseModel, Field
from typing import Callable, Optional
from abc import abstractmethod
from typing import Any
from enum import Enum

MAX_CONNECTOR_PKL_SIZE = 10 * 1024 * 1024  # 10 MB

class AppConfig(BaseModel):
    kafka_partition: str = '3'
    executor_core_request: str = '500m'
    driver_core_request: str = '500m'
    driver_memory_request: str = '500m'
    executor_memory_request: str = '500m'
    executor_instance: str = '1'


class CONNECTOR_CLASS(Enum):
    Http = "HTTP"
    HttpSoap = "HTTP_SOAP"
    EventHub = "AZURE_EVENT_HUB"
    External = "EXTERNAL"
    Internal = "INTERNAL"
    Custom = "Custom Python"
    DeltaV = 'DELTA_V_SQL'
    Opcua = 'OPCUA'




class ConnectorApp(BaseModel):
    '''
    Abstract Base class for all connectors
    connector_config is nullable for external connectors
    transformation and connector_config is stored in the pickle and not in the database
    '''

    id: int = None
    name: str
    source: Optional[list[int]] = None
    transformation: Optional[Callable[[Any], Any]] = Field(default=None)
    connector_type: str # Source, Sink
    app_config: AppConfig = AppConfig()
    connector_config: BaseModel = None
    connector_class: str

    WAIT_BEFORE_RETRY_SECONDS = 5
    _logger: Optional[logging.Logger] = PrivateAttr(default=None)


    @abstractmethod
    def start(self, 
              id: int,
              kafka_topics: list[str],
              source: Optional[list[int]] = None):
        raise NotImplementedError

    @final
    def save(self, client):
        from quartic_sdk import GraphqlClient

        assert isinstance(client, GraphqlClient)

        connector_pkl = ModelUtils.get_pickled_object(self)
        assert sys.getsizeof(connector_pkl) <= MAX_CONNECTOR_PKL_SIZE, \
            f"Connector pickle size can't be more than {MAX_CONNECTOR_PKL_SIZE} MB"

        variables = {
            'name': self.name,
            'sourceConnectors': self.source,
            'connectorType': self.connector_type,
            'appConfig': self.app_config.dict(),
            'model': connector_pkl,
            'connectorClass': self.connector_class
        }
        SINK_CONNECTOR_CREATE_MUTATION = """
        mutation createConnector(
            $name: String!,
            $sourceConnectors: [ID],
            $connectorType: ConnectorAppConnectorTypeEnumCreate!,
            $appConfig: CustomDict!,
            $model: String!,
            $connectorClass: ConnectorAppConnectorClassEnumCreate!
            ) {
            ConnectorappCreate(
                newConnectorapp: {
                    name: $name,
                    sourceConnectors: $sourceConnectors,
                    connectorType: $connectorType,
                    appConfig: $appConfig,
                    model: $model,
                    connectorClass: $connectorClass
                }) 
                {
                    connectorapp {
                        id
                    }
                    ok
                    errors {
                        field
                        messages
                    }
                }
            }
        """
        print("Saving the Connector to Quartic Platform")
        response = client.execute_query(SINK_CONNECTOR_CREATE_MUTATION, variables)
        print(response)
        if not response['data']['ConnectorappCreate']['ok']:
            raise Exception(response['data']['ConnectorappCreate']['errors'])
        
        self.id = int(response['data']['ConnectorappCreate']['connectorapp']['id'])
        print("Successfully saved the Connector to Quartic Platform")

    @final
    def deploy(self, client):
        from quartic_sdk import GraphqlClient

        assert isinstance(client, GraphqlClient)

        variables = {
            'id': self.id
        }
        DEPLOY_CONNECTOR_QUERY = """
        query deployConnector($id: Int!) {
            deployConnector(connectorId: $id) 
        }
        """
        response = client.execute_query(DEPLOY_CONNECTOR_QUERY, variables)
        if not response['data']['deployConnector']['status'] == 200:
            raise Exception(response['data']['deployConnector']['status'])
        print("Successfully deployed the Connector to Quartic Platform")

    @staticmethod
    def get_connectors(client, id=None, name=None):
        '''
        Get connectcors from QPro
        '''
        from quartic_sdk import GraphqlClient

        assert isinstance(client, GraphqlClient)

        if id:
            variables = {'id': id}
            GET_CONNECTORS_BY_ID_QUERY = """
                query getConnectors($id: Float!) {
                    __typename
                    ConnectorApp(id: $id) {
                        createdAt
                        connectorType
                        appConfig
                        id
                        isDeployed
                        connectorClass
                        modelStr
                        updatedAt
                        sourceConnectors {
                        id
                        name
                        isDeployed
                        }
                    }
                }
            """
            connector = client.execute_query(GET_CONNECTORS_BY_ID_QUERY, variables)
            return connector

        elif name:
            variables = {'name': name}
            GET_CONNECTORS_BY_NAME_QUERY = """
                query getConnectors($name: String!) {
                    __typename
                    ConnectorApp(name: $name) {
                        createdAt
                        connectorType
                        appConfig
                        id
                        isDeployed
                        connectorClass
                        modelStr
                        updatedAt
                        sourceConnectors {
                        id
                        name
                        isDeployed
                        }
                    }
                }
            """
            connector = client.execute_query(GET_CONNECTORS_BY_NAME_QUERY, variables)
            return connector

        GET_CONNECTORS_QUERY = """
        query getConnectors {
            __typename
            ConnectorApp {
                createdAt
                connectorType
                appConfig
                id
                isDeployed
                connectorClass
                modelStr
                updatedAt
                sourceConnectors {
                id
                name
                isDeployed
                }
            }
        }
        """
        connectors = client.execute_query(GET_CONNECTORS_QUERY)
        return connectors

    @property
    def logger(self):
        if not getattr(self, "_logger", None):
            self._logger = logging.getLogger(f"{self.__class__.__name__}:{self.id}")
            self.configure_logger(self._logger)
        return self._logger

    def configure_logger(self, logger: logging.Logger):
        """Called first time after a logger is created"""
        logger.setLevel(logging.INFO)


class ExternalApp(ConnectorApp):
    """Generic external connector application implementation"""
    connector_class = CONNECTOR_CLASS.External.value

    @final
    def start(self, *args, **kwargs):
        raise NotImplementedError("Can't start external connectors")
    
    @final
    def deploy(self, client):
        raise NotImplementedError("Can't deploy external connectors")


def get_truststore_password() -> str:
    """
    Read Kafka SSL truststore password from file

    Returns:
        str: password
    """
    import os
    truststore_path = os.getenv('KAFKA_SSL_TRUSTSTORE_PASSWORD',"")
    if not truststore_path:
        return truststore_path
    with open(truststore_path, 'r') as file:
        password = file.read().strip()
    return password
