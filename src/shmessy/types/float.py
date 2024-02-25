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


class FloatType(BaseType):
    weight = 8

    def validate(self, data: ndarray) -> Optional[InferredField]:
        at_least_single_not_empty_value: bool = False
        for value in data:
            try:
                self.cast_value(value)
                if not at_least_single_not_empty_value and not self.is_empty_value(
                    value
                ):
                    at_least_single_not_empty_value = True
            except Exception:  # noqa
                logger.debug(f"Cannot cast the value '{value}' to {self.name}")
                return None
        if at_least_single_not_empty_value:
            return InferredField(inferred_type=self.name)

    @property
    def prefer_column_casting(self) -> bool:
        return True

    def cast_column(self, column: Series, inferred_field: InferredField) -> Series:
        if is_numeric_dtype(column):
            return column
        return to_numeric(column.apply(locale.atof))

    def cast_value(self, value: Any, pattern: Optional[Any] = None) -> Optional[Any]:
        if isinstance(value, str):
            return float(locale.atof(value))
        return float(value)

    def ignore_cast_for_types(self) -> Tuple[Any]:
        return (np.dtype("float64"),)
