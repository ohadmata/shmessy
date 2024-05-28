import logging
from typing import Any, Optional, Tuple

import numpy as np
from numpy import ndarray
from pandas import Series, to_datetime

from ..date_utils import cast_value, validate
from ..schema import InferredField
from .base import BaseType

logger = logging.getLogger(__name__)


class DateType(BaseType):
    weight = 2
    delimiters: list[str] = {"/", ".", "-", " "}
    static_patterns: list[str] = ["%B %d, %Y"]
    dynamic_patterns: list[list[str]] = [
        ["%m", "%d", "%Y"],
        ["%d", "%m", "%Y"],
        ["%m", "%d", "%y"],
        ["%d", "%m", "%y"],
        ["%Y", "%m", "%d"],
        ["%y", "%m", "%d"],
        ["%d", "%b", "%Y"],
        ["%d", "%b", "%y"],
        ["%b", "%d", "%Y"],
        ["%Y", "%m"],
    ]

    @classmethod
    def get_patterns(cls) -> list[str]:
        # The value returned cannot be set since the order is important!
        results: list[str] = []
        for pattern in cls.dynamic_patterns:
            for delimiter in cls.delimiters:
                results.append(delimiter.join(pattern))
        return results + cls.static_patterns

    def validate(self, data: ndarray) -> Optional[InferredField]:
        return validate(
            data=data, patterns=self.get_patterns(), inferred_type=self.name
        )

    @property
    def prefer_column_casting(self) -> bool:
        return True

    def cast_column(self, column: Series, inferred_field: InferredField) -> Series:
        return to_datetime(column, format=inferred_field.inferred_pattern)

    def cast_value(self, value: Any, pattern: Optional[Any] = None) -> Optional[Any]:
        return cast_value(value, pattern)

    def ignore_cast_for_types(self) -> Tuple[Any]:
        return (np.dtype("datetime64"),)
