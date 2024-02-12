import math
from typing import Any, Optional, Tuple

import numpy as np
from numpy import ndarray
from pandas import Series

from ..schema import InferredField
from .base import BaseType


class BooleanType(BaseType):
    weight = 1
    patterns: list[Tuple] = [  # The first member should be the true value
        ("YES", "NO"),
        ("TRUE", "FALSE"),
        ("T", "F"),
        ("Y", "N"),
        (1, 0),
    ]

    def _match_bool_pattern(self, data: ndarray, pattern: Tuple) -> bool:
        match_positive: bool = False
        match_negative: bool = False

        for value in data:
            casted_value = self.cast_value(value, pattern)
            if casted_value is None:
                return False
            if casted_value is True:
                match_positive = True
            else:
                match_negative = True

        if match_positive and match_negative:
            return True
        return False

    def validate(self, data: ndarray) -> Optional[InferredField]:
        if data.dtype == np.dtype("bool"):
            return InferredField(inferred_type=self.name)
        for pattern in self.patterns:
            if self._match_bool_pattern(data, pattern):
                return InferredField(inferred_type=self.name, inferred_pattern=pattern)

    def cast_column(self, column: Series, inferred_field: InferredField) -> Series:
        raise NotImplementedError()

    def cast_value(self, value: Any, pattern: Optional[Any] = None) -> Optional[Any]:
        if pattern is None:
            return value
        if isinstance(pattern[0], str) and isinstance(value, str):
            return (
                None
                if isinstance(value, float) and math.isnan(value)
                else (True if value.lower() == pattern[0].lower() else False)  # noqa
            )

        if isinstance(pattern[0], (bool, int)):
            if value == pattern[0]:
                return True
            if value == pattern[1]:
                return False

    def ignore_cast_for_types(self) -> Tuple[Any]:
        return (np.dtype("bool"),)
