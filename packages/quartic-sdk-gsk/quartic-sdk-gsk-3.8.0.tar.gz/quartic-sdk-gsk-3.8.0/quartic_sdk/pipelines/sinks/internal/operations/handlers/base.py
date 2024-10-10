import logging
from abc import ABC, abstractmethod
from typing import Type, Tuple, Generic, TypeVar, Optional

from quartic_sdk.graphql_client import GraphqlClient
from quartic_sdk.pipelines.sinks.internal.operations.operations import InternalOperation

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=InternalOperation)


class OperationHandler(ABC, Generic[T]):
    """Base class for internal operation handlers"""

    @abstractmethod
    def handle(self, operations: list[T]) -> Tuple[list[T], list[T]]:
        """Evaluates operations and returns (success_operations, failed_operations)"""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_optype(cls) -> Type[T]:
        raise NotImplementedError()


class GQLOperationHandler(OperationHandler[T]):
    """
    Base handler for simple GQL operations. Complex GQL queries should not implement this.
    """

    @abstractmethod
    def get_query(self, op: T) -> Tuple[str, dict]:
        raise NotImplemented

    def get_success_field(self) -> Optional[str]:
        """
        Returns a `.` separated boolean field path to check in the json response for success.
        If None then only the response status_code is used to determine operation success.
        """
        return None

    def handle(self, operations: list[T]) -> Tuple[list[T], list[T]]:
        client = GraphqlClient.get_graphql_client_from_env()
        success_operations, failed_operations = [], []
        for op in operations:
            mutation, variables = self.get_query(op)
            try:
                response = client.execute_query(mutation, variables)
                if response and self._is_ok(response):
                    logger.debug(f"GQL mutation successful {response}")
                    success_operations.append(op)
                else:
                    failed_operations.append(op)
            except Exception:
                logger.exception(f"Failed to execute operation {op}")
                failed_operations.append(op)
        return success_operations, failed_operations

    def _is_ok(self, response: dict):
        success_path = self.get_success_field()
        if not success_path:
            return True

        assert isinstance(response, dict), f"Unexpected response type {type(response)}"
        node = response
        for key in success_path.split("."):
            try:
                node = node[key]
            except KeyError as e:
                logger.exception(f"Error while accessing success field")
                return False

        logger.debug(f"Success node value: {node}")
        return node
