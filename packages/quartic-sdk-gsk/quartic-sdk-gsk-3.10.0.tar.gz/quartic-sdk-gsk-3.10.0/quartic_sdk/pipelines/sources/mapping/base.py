from abc import ABC, abstractmethod
from typing import Tuple

import pandas as pd


class MappingProcessor(ABC):
    """
    Base class for enriching/mapping source connector data
    """

    @classmethod
    @abstractmethod
    def get_source_classes(cls) -> list[str]:
        raise NotImplemented

    @abstractmethod
    def process(self, df: pd.DataFrame, connector_id: int) -> list[Tuple[str, dict]]:
        raise NotImplemented
