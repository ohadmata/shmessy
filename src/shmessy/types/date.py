from typing import Optional

from numpy import ndarray
from pandas import Series, to_datetime

from ..schema import InferredField
from . import validate_strptime_pattern
from .base import BaseType


class DateType(BaseType):
    weight = 2
    patterns: list[str] = [
        "%m/%d/%Y",  # 12/01/2022
        "%m-%d-%Y",  # 12-01-2022
        "%m.%d.%Y",  # 12.01.2022
        "%m/%d/%y",  # 12/01/22
        "%m-%d-%y",  # 12.01.2022
        "%m.%d.%y",  # 12.29.22
        "%d.%m.%y",  # 29.01.22
        "%Y/%m/%d",  # 2022/12/01
        "%Y-%m-%d",  # 2022-12-01
        "%Y.%m.%d",  # 2022.12.01
        "%d/%m/%Y",  # 01/12/2022
        "%d-%m-%Y",  # 01-12-2022
        "%d.%m.%Y",  # 01.12.2022
        "%d/%b/%Y",  # 01/Mar/2022
        "%d-%b-%Y",  # 01-Mar-2022
        "%Y-%m",  # 2022-07
        "%d %b %Y",  # 13 Jan 2023
    ]

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for pattern in self.patterns:
            if validate_strptime_pattern(data, pattern):
                return InferredField(inferred_type=self.name, inferred_pattern=pattern)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        return to_datetime(column, format=inferred_field.inferred_pattern)


def get_type() -> DateType:
    return DateType()
