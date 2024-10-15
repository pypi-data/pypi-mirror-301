import os
from typing import Callable
from itertools import groupby

import pandas as pd
import cloudpickle
from quartic_sdk.pipelines.sinks.base_sink import KafkaSinkApp, CONNECTOR_CLASS
from quartic_sdk.pipelines.connector_app import AppConfig
from quartic_sdk.pipelines.sinks.internal.operations.operations import InternalOperation
from quartic_sdk.pipelines.sinks.internal.operations.handlers.utils import get_handler
from quartic_sdk.pipelines.settings import settings


STATE_BASE_DIR = settings.internal_sink_state_directory


class InternalPlatformSink(KafkaSinkApp):
    transformation: Callable[[pd.DataFrame, dict], list[InternalOperation]]
    connector_class: str = CONNECTOR_CLASS.Internal.value

    def write_data(self, operations: list[InternalOperation]):
        self.logger.info(f"Process {len(operations)} operations")
        if not operations:
            return

        handler = get_handler(operations[0])
        self.logger.info(f"Using handler {handler}")
        success, failed = handler.handle(operations)
        self.logger.info(f"{success=} {failed=}")
        # TODO: Raise error here if failed > 0?
        # Or the user could provide a on_success/on_failure callback?
        assert not failed, f"Failed operations: {failed}"

    def process_records(self, data: pd.DataFrame):
        if not self.transformation:
            self.logger.exception(
                f"Unexpected empty transformation in internal sink {self.transformation}"
            )
            return

        state = self.__get_state()
        operations = self.transformation(data, state)
        self.__write_state(state)
        if not operations:
            self.logger.warning(f"Empty opreations return from transformation")
            return

        grouped_operations = self.__group_operations(operations)
        self.logger.debug(f"Operations: {grouped_operations}")
        for op_group in grouped_operations:
            self.write_data(op_group)

    def __group_operations(self, operations: list[InternalOperation]):
        """
        Returns adjacent groups of operations.

        Example:
        Grouping operations [A, A, B, C, A]
        Returns: [[A, A], [B], [C], [A]]

        This is to preserve the order of operations during evaluation.
        """
        groups = groupby(operations, lambda op: op.optype)
        return [list(group) for _, group in groups]

    def __get_state_pickle_file(self):
        if not os.path.exists(STATE_BASE_DIR):
            self.logger.info(f"Creating state dir {STATE_BASE_DIR}")
            os.system(f"mkdir -p {STATE_BASE_DIR}")

        return f"{STATE_BASE_DIR}/state_{self.id}.pkl"

    def __get_state(self):
        filename = self.__get_state_pickle_file()
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                return cloudpickle.load(f) or {}
        return {}

    def __write_state(self, state: dict):
        filename = self.__get_state_pickle_file()
        with open(filename, "wb") as f:
            cloudpickle.dump(state, f)
