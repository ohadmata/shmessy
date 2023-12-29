from datetime import datetime
from typing import Optional

from numpy import ndarray
from pandas import Series, to_datetime

from ..schema import InferredField, ValidatorTypes
from .base import BaseValidator


class Validator(BaseValidator):
    validator_type = ValidatorTypes.STRING
    patterns: list[str] = [
        "%m/%d/%y %H:%M:%S",
        "%m-%d-%y %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
        "%m-%d-%Y %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S.%fZ",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%fZ",
    ]

    def validate(self, data: ndarray) -> Optional[InferredField]:
        try:
            self.check_validation_type(dtype=data.dtype)
        except ValueError:
            return None

        for pattern in self.patterns:
            valid: bool = True
            for value in data:
                try:
                    if isinstance(value, str):
                        datetime.strptime(value, pattern)
                except ValueError:
                    valid = False
                    break
            if valid:
                return InferredField(inferred_type=datetime, inferred_pattern=pattern)

    def fix(self, column: Series, sample_size: int) -> Series:
        sample_data = column[:sample_size]
        inferred = self.validate(sample_data)
        if inferred:
            return to_datetime(column, format=inferred.inferred_pattern)
