import logging
from datetime import datetime
from typing import Any, Optional, Tuple

import numpy as np
from numpy import ndarray
from pandas import Series, Timestamp, to_datetime

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
        "%Y-%m-%d %H:%M:%S %Z",  # 2020-09-24 11:57:27 UTC
    ]

    def validate(self, data: ndarray) -> Optional[InferredField]:
        if data.dtype.type == np.dtype("datetime64"):
            return InferredField(inferred_type=self.name)

        for pattern in self.patterns:
            valid_pattern = True
            at_least_single_not_nan_value = False
            for value in data:
                try:
                    self.cast_value(value, pattern)
                    if not self.is_empty_value(value):
                        at_least_single_not_nan_value = True
                except Exception as e:
                    logger.debug(e)
                    valid_pattern = False

            if valid_pattern and at_least_single_not_nan_value:
                return InferredField(inferred_type=self.name, inferred_pattern=pattern)

    @property
    def prefer_column_casting(self) -> bool:
        return True

    def cast_column(self, column: Series, inferred_field: InferredField) -> Series:
        return to_datetime(column, format=inferred_field.inferred_pattern)

    def cast_value(self, value: Any, pattern: Optional[Any] = None) -> Optional[Any]:
        try:
            if self.is_empty_value(value):
                return None
            if isinstance(value, (np.datetime64, Timestamp)):
                return value
            if isinstance(value, str):
                return datetime.strptime(value, pattern)
            raise Exception(f"Input value for {self.name} casting must be string.")
        except ValueError as e:
            logger.debug(f"Cannot cast the value '{value}' using pattern '{pattern}'")
            raise e

    def ignore_cast_for_types(self) -> Tuple[Any]:
        return (np.dtype("datetime64"),)
