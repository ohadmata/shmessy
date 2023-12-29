from datetime import date
from typing import Optional

from numpy import ndarray
from pandas import Series, to_datetime

from ..schema import InferredField, ValidatorTypes
from . import validate_strptime_pattern
from .base import BaseValidator


class Validator(BaseValidator):
    validator_type = ValidatorTypes.STRING
    patterns: list[str] = [
        "%m/%d/%Y",  # 12/01/2022
        "%m-%d-%Y",  # 12-01-2022
        "%m.%d.%Y",  # 12.01.2022
        "%m/%d/%y",  # 12/01/22
        "%m-%d-%y",  # 12.01.2022
        "%m.%d.%y",  # 12.01.22
        "%Y/%m/%d",  # 2022/12/01
        "%Y-%m-%d",  # 2022-12-01
        "%Y.%m.%d",  # 2022.12.01
        "%d/%m/%Y",  # 01/12/2022
        "%d-%m-%Y",  # 01-12-2022
        "%d.%m.%Y",  # 01.12.2022
        "%d/%b/%Y",  # 01/Mar/2022
        "%d-%b-%Y",  # 01-Mar-2022
        "%-d-%b-%y",  # 1-Mar-22
        "%Y-%m",  # 2022-07
    ]

    def validate(self, data: ndarray) -> Optional[InferredField]:
        if not self.is_validator_type_valid(dtype=data.dtype):
            return None

        for pattern in self.patterns:
            if validate_strptime_pattern(data, pattern):
                return InferredField(inferred_type=date, inferred_pattern=pattern)

    def fix(self, column: Series, sample_size: int) -> Series:
        sample_data = column[:sample_size]
        inferred = self.validate(sample_data)
        if inferred:
            return to_datetime(column, format=inferred.inferred_pattern)
