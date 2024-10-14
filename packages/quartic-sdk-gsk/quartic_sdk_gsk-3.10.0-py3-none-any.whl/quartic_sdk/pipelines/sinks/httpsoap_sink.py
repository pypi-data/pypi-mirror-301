from .http_sink import HttpSink, HttpConfig
from quartic_sdk.pipelines.connector_app import CONNECTOR_CLASS

class HttpSoapConfig(HttpConfig):
    headers: dict[str, str] = {'Content-Type': 'application/soap+xml'} # SOAP 1.2
    # headers: dict[str, str] = {'Content-Type': 'text/xml'} # SOAP 1.1


class HttpSoapSink(HttpSink):
    connector_class: str = CONNECTOR_CLASS.HttpSoap.value
    connector_config: HttpSoapConfig
