import logging
from typing import Optional

import numpy as np
from numpy import ndarray
from pandas import Series, to_datetime

from ..exceptions import FieldCastingException
from ..schema import InferredField
from . import extract_bad_value_strptime, validate_strptime_pattern
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
        "%Y-%m-%dT%H:%M:%S",
    ]

    def validate(self, data: ndarray) -> Optional[InferredField]:
        if data.dtype.type == np.dtype("datetime64"):
            return InferredField(inferred_type=self.name)

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


def get_type() -> DatetimeType:
    return DatetimeType()
