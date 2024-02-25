import logging
from typing import Any, Optional, Tuple

from numpy import ndarray
from pandas import Series

from ..schema import InferredField
from .base import BaseType

logger = logging.getLogger(__name__)


class StringType(BaseType):
    weight = 9

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for value in data:
            try:
                str(value)
            except Exception:  # noqa
                logger.debug(f"Cannot cast the value '{value}' to {self.name}")
                return None
        return InferredField(inferred_type=self.name)

    @property
    def prefer_column_casting(self) -> bool:
        return True

    def cast_column(self, column: Series, inferred_field: InferredField) -> Series:
        return column.apply(lambda x: str(x))

    def cast_value(self, value: Any, pattern: Optional[Any] = None) -> Optional[Any]:
        return str(value)

    def ignore_cast_for_types(self) -> Tuple[Any]:
        return tuple()
