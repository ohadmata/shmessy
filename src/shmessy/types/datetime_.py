import logging
from typing import Any, Optional, Tuple

import numpy as np
from numpy import ndarray
from pandas import Series, to_datetime

from ..date_utils import cast_value, validate
from ..schema import InferredField
from .base import BaseType
from .date import DateType

logger = logging.getLogger(__name__)


class DatetimeType(BaseType):
    weight = 3
    static_patterns: list[str] = [
        "%Y-%m-%d %H:%M:%SZ",  # 2022-12-30 00:00:00Z
        "%Y-%m-%dT%H:%M:%SZ",  # 2022-12-30T00:00:00Z
        "%Y-%m-%d %H:%M:%S.%fZ",  # 2022-12-30 00:00:00.000Z
        "%Y-%m-%dT%H:%M:%S.%fZ",  # 2022-12-30T00:00:00.000Z
    ]
    date_time_delimiters: set[str] = {" ", "T"}
    dynamic_patterns: list[str] = [
        "%H:%M",  # 00:00
        "%H:%M:%S",  # 00:00:00
        "%H:%M:%S.%f",  # 00:00:00.000
        "%H:%M:%S %Z",  # 00:00:00 UTC
        "%H:%M:%S %z",  # 00:00:00 +00:00
    ]

    @classmethod
    def get_patterns(cls) -> list[str]:
        result: list[str] = []
        for date in DateType.get_patterns():
            for date_time_delimiter in cls.date_time_delimiters:
                for dynamic_pattern in cls.dynamic_patterns:
                    result.append(date + date_time_delimiter + dynamic_pattern)
        return result + cls.static_patterns

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
