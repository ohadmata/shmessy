from typing import Optional

import numpy as np
from numpy import ndarray
from pandas import Series, to_datetime

from ..schema import InferredField
from . import validate_strptime_pattern
from .base import BaseType


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
        "%Y-%m-%dT%H:%M:%S",
    ]

    def validate(self, data: ndarray) -> Optional[InferredField]:
        if data.dtype.type == np.dtype("datetime64"):
            return InferredField(inferred_type=self.name)

        for pattern in self.patterns:
            if validate_strptime_pattern(data, pattern):
                return InferredField(inferred_type=self.name, inferred_pattern=pattern)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        return to_datetime(column, format=inferred_field.inferred_pattern)


def get_type() -> DatetimeType:
    return DatetimeType()
