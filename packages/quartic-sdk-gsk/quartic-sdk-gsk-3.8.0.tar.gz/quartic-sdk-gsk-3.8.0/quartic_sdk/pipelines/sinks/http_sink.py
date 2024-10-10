from .base_sink import SparkSinkApp
from typing import Callable, Optional
from quartic_sdk.pipelines.connector_app import CONNECTOR_CLASS
from pydantic import BaseModel
from typing import Literal
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
import pandas as pd
import time


class HttpConfig(BaseModel):
    endpoint: str
    auth_type: str = None
    username: str = None
    password: str = None
    group_messages: bool = False
    headers: dict[str, str] = {'Content-Type': 'application/json'}
    timeout: int = 10

class HttpSink(SparkSinkApp):
    connector_class: str = CONNECTOR_CLASS.Http.value
    success_response_callback: Optional[Callable] = None
    connector_config: HttpConfig
    
    def _create_session(self) -> requests.Session:
        """Create an HTTP session with basic authentication."""
        # TODO: Check session timeout?
        session = requests.Session()
        if self.connector_config.auth_type == 'Basic':
            session.auth = HTTPBasicAuth(self.connector_config.username, self.connector_config.password)
        session.headers.update(self.connector_config.headers)
        return session

    def write_data(self, data: pd.DataFrame, spark=None):
        session = self._create_session()
        series = data['value']
        data = series.to_list()
        if self.connector_config.group_messages:
            while True:
                try:
                    self.__send_post_request(session, data)
                except Exception as e:
                    time.sleep(self.WAIT_BEFORE_RETRY_SECONDS)
                    continue
                break
                
        else:
            for item in data:
                while True:
                    try:
                        self.__send_post_request(session, item)
                    except Exception as e:
                        time.sleep(self.WAIT_BEFORE_RETRY_SECONDS)
                        continue
                    break
    
    def __send_post_request(self, session, data):
        """Send a POST request with the given data"""
        try:
            response = session.post(self.connector_config.endpoint, data=data, timeout=self.connector_config.timeout)
            response.raise_for_status()
            if self.success_response_callback:
                self.success_response_callback(response)
            print(f"Successfully written data: {data}.")
            print(f"Response: {response.text}")
        except RequestException as e:
            print(f"Failed to write data: {data}. Error: {e}")
            print(f"Response: {response.text}")
            raise e
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e
        session.close()
