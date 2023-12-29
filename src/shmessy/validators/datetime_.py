from datetime import datetime
from typing import Optional

from numpy import ndarray
from pandas import Series, to_datetime

from ..schema import InferredField, ValidatorTypes
from . import validate_strptime_pattern
from .base import BaseValidator


class Validator(BaseValidator):
    validator_type = ValidatorTypes.STRING
    patterns: list[str] = [
        "%m/%d/%Y %-H:%M",  # 11/14/2003 0:00
        "%d-%m-%Y %H:%M",  # 11-14-2003 00:00
        "%d-%m-%Y %-H:%M",  # 11-14-2003 0:00
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
        "%b %-d, %Y %H:%M %p",  # Jul 3, 2023 12:10 PM
    ]

    def validate(self, data: ndarray) -> Optional[InferredField]:
        if not self.is_validator_type_valid(dtype=data.dtype):
            return None

        for pattern in self.patterns:
            if validate_strptime_pattern(data, pattern):
                return InferredField(inferred_type=datetime, inferred_pattern=pattern)

    def fix(self, column: Series, sample_size: int) -> Series:
        sample_data = column[:sample_size]
        inferred = self.validate(sample_data)
        if inferred:
            return to_datetime(column, format=inferred.inferred_pattern)
