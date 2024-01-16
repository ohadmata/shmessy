from abc import ABC, abstractmethod
from typing import Optional

from numpy import ndarray
from pandas import Series

from ..schema import InferredField


class BaseType(ABC):
    weight: int = 0

    @abstractmethod
    def validate(self, data: ndarray) -> Optional[InferredField]:
        pass

    @abstractmethod
    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        pass

    @property
    def name(self) -> str:
        return str(self.__class__.__name__.replace("Type", ""))
