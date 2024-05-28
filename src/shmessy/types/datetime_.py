import logging
from typing import Any, Optional, Tuple

import numpy as np
from numpy import ndarray
from pandas import Series, to_datetime

from ..date_utils import cast_value, validate
from ..schema import InferredField
from .base import BaseType

logger = logging.getLogger(__name__)


class DatetimeType(BaseType):
    weight = 3
    patterns: list[str] = [
        "%d-%m-%Y %H:%M",  # 11-14-2003 00:00
        "%m/%d/%y %H:%M:%S",  # 12/15/22 00:00:00
        "%m-%d-%y %H:%M:%S",  # 12-30-2022 00:00:00
        "%m/%d/%Y %H:%M:%S",  # 12/30/2022 00:00:00
        "%m-%d-%Y %H:%M:%S",  # 12-30-2022 00:00:00
        "%Y/%m/%d %H:%M:%S",  # 2022/12/30 00:00:00
        "%Y-%m-%d %H:%M:%S",  # 2022-12-30 00:00:00
        "%Y-%m-%d %H:%M:%SZ",  # 2022-12-30 00:00:00Z
        "%Y-%m-%dT%H:%M:%SZ",  # 2022-12-30T00:00:00Z
        "%Y-%m-%dT%H:%M:%S.%f",  # 2022-12-30T00:00:00.000
        "%Y-%m-%d %H:%M:%S.%fZ",  # 2022-12-30 00:00:00.000Z
        "%Y-%m-%d %H:%M:%S.%f",  # 2022-12-30 00:00:00.000
        "%Y-%m-%dT%H:%M:%S.%fZ",  # 2022-12-30T00:00:00.000Z
        "%Y-%m-%dT%H:%M:%S",  # 2022-12-30T00:00:00
        "%d/%m/%Y %H:%M",  # 30/12/2022 00:00
        "%m/%d/%Y %H:%M",  # 12/30/2022 00:00
        "%d/%m/%y %H:%M",  # 12/30/22 00:00
        "%Y-%m-%d %H:%M",  # 2020-09-24 11:57
        "%Y-%m-%d %H:%M:%S %Z",  # 2020-09-24 11:57:27 UTC
        "%Y-%m-%d %H:%M:%S %z",  # 2022-12-30 11:57:27 +00:00"
    ]

    def validate(self, data: ndarray) -> Optional[InferredField]:
        return validate(data=data, patterns=self.patterns, inferred_type=self.name)

    @property
    def prefer_column_casting(self) -> bool:
        return True

    def cast_column(self, column: Series, inferred_field: InferredField) -> Series:
        return to_datetime(column, format=inferred_field.inferred_pattern)

    def cast_value(self, value: Any, pattern: Optional[Any] = None) -> Optional[Any]:
        return cast_value(value, pattern)

    def ignore_cast_for_types(self) -> Tuple[Any]:
        return (np.dtype("datetime64"),)
