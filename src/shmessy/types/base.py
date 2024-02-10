import math
from abc import ABC, abstractmethod
from typing import Any, Optional

from numpy import ndarray

from ..schema import InferredField


class BaseType(ABC):
    weight: int = 0

    @abstractmethod
    def validate(self, data: ndarray) -> Optional[InferredField]:
        pass

    @abstractmethod
    def cast(self, value: Any, pattern: Optional[Any] = None) -> Optional[Any]:
        pass

    @property
    def name(self) -> str:
        return str(self.__class__.__name__.replace("Type", ""))

    @staticmethod
    def is_empty_value(value: Any) -> bool:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return True
        return False
