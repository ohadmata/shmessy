import logging
from typing import Optional

from numpy import ndarray
from pandas import Series, to_datetime

from ..exceptions import FieldCastingException
from ..schema import InferredField
from . import extract_bad_value_strptime, validate_strptime_pattern
from .base import BaseType

logger = logging.getLogger(__name__)


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
        try:
            return to_datetime(column, format=inferred_field.inferred_pattern)
        except Exception as e:
            logger.debug(f"Couldn't cast column to type {self.name}: {e}")
            line_number, bad_value = extract_bad_value_strptime(
                column, inferred_field.inferred_pattern
            )
            raise FieldCastingException(
                type_=f"{self.name}[{inferred_field.inferred_pattern}]",
                line_number=line_number,
                bad_value=bad_value,
                column_name=str(column.name),
            )


def get_type() -> DateType:
    return DateType()
