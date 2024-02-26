import logging
from datetime import datetime
from typing import Any, Optional, Tuple

import numpy as np
from numpy import ndarray
from pandas import Series, to_datetime

from ..schema import InferredField
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
        "%d %b %y",  # 04 Jul 96
    ]

    def validate(self, data: ndarray) -> Optional[InferredField]:
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
            if isinstance(value, str):  # For security reasons & skip nan values
                return datetime.strptime(value, pattern)
            raise Exception(f"Input value for {self.name} casting must be string.")
        except ValueError as e:
            logger.debug(f"Cannot cast the value '{value}' using pattern '{pattern}'")
            raise e

    def ignore_cast_for_types(self) -> Tuple[Any]:
        return (np.dtype("datetime64"),)
