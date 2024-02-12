import math
from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple

from numpy import ndarray
from pandas import Series

from ..schema import InferredField


class BaseType(ABC):
    weight: int = 0

    @abstractmethod
    def validate(self, data: ndarray) -> Optional[InferredField]:
        pass

    @abstractmethod
    def cast_value(self, value: Any, pattern: Optional[Any] = None) -> Optional[Any]:
        pass

    @abstractmethod
    def cast_column(
        self, column: Series, inferred_field: InferredField
    ) -> Optional[Any]:
        pass

    @abstractmethod
    def ignore_cast_for_types(self) -> Tuple[Any]:
        pass

    @property
    def name(self) -> str:
        return str(self.__class__.__name__.replace("Type", ""))

    @property
    def prefer_column_casting(self) -> bool:
        return False

    @staticmethod
    def is_empty_value(value: Any) -> bool:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return True
        return False
