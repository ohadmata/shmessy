import locale
import logging
from typing import Any, Optional, Tuple

import numpy as np
from numpy import ndarray
from pandas import Series, to_numeric
from pandas.api.types import is_numeric_dtype

from ..schema import InferredField
from .base import BaseType

logger = logging.getLogger(__name__)


class IntegerType(BaseType):
    weight = 7
    MAX_BOUNDARY: int = 9223372036854775807  # BIGINT max value
    MIN_BOUNDARY: int = -9223372036854775807  # BIGINT min value

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for value in data:
            try:
                casted_values = self.cast_value(value)
                if (
                    casted_values > self.MAX_BOUNDARY
                    or casted_values < self.MIN_BOUNDARY
                ):
                    logger.debug(
                        f"Value '{value}' does not match to {self.name} boundaries"
                    )
                    return None
            except Exception:  # noqa
                logger.debug(f"Cannot cast the value '{value}' to {self.name}")
                return None
        return InferredField(inferred_type=self.name)

    @property
    def prefer_column_casting(self) -> bool:
        return True

    def cast_column(self, column: Series, inferred_field: InferredField) -> Series:
        if is_numeric_dtype(column):
            return column
        return to_numeric(column.apply(locale.atoi))

    def cast_value(self, value: Any, pattern: Optional[Any] = None) -> Optional[Any]:
        if isinstance(value, str):
            return int(locale.atoi(value))
        return int(value)

    def ignore_cast_for_types(self) -> Tuple[Any]:
        return (np.dtype("int64"),)
