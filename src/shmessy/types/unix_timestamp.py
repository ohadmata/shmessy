import logging
import math
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from numpy import ndarray
from pandas import Series, to_datetime

from ..schema import InferredField
from .base import BaseType

logger = logging.getLogger(__name__)


class TimestampResolution(str, Enum):
    SECONDS = "s"
    MILLISECONDS = "ms"
    NANOSECONDS = "ns"


class UnixTimestampType(BaseType):
    weight = 4
    min_valid_year: int = 1980
    max_valid_year: int = 2100

    resolution: Optional[TimestampResolution] = None

    @staticmethod
    def _unix_timestamp_resolution(value: int) -> TimestampResolution:
        number_of_digits = len(str(int(value)))
        if number_of_digits == 10:
            return TimestampResolution.SECONDS
        if number_of_digits == 13:
            return TimestampResolution.MILLISECONDS
        if number_of_digits == 16:
            return TimestampResolution.NANOSECONDS

    @staticmethod
    def _fix_input_resolution(
        value: int, selected_resolution: TimestampResolution
    ) -> int:
        if selected_resolution == TimestampResolution.SECONDS:
            return int(value)
        if selected_resolution == TimestampResolution.MILLISECONDS:
            return int(int(value) / 1000)
        if selected_resolution == TimestampResolution.NANOSECONDS:
            return int(int(value) / 1000 / 1000)

    def _is_valid_unix_timestamp(self, value: Any) -> bool:
        if isinstance(value, float) and math.isnan(value):
            return True

        if isinstance(value, float) and math.isinf(value):
            return False

        if not self.resolution:
            self.resolution = self._unix_timestamp_resolution(int(value))

        if self.resolution:
            parsed_value = datetime.utcfromtimestamp(
                self._fix_input_resolution(value, self.resolution)
            )
            if self.min_valid_year <= parsed_value.year <= self.max_valid_year:
                return True
        return False

    def validate(self, data: ndarray) -> Optional[InferredField]:
        self.resolution = None
        try:
            for value in data:
                if not self._is_valid_unix_timestamp(value):
                    return None

            if not self.resolution:
                return None

            return InferredField(
                inferred_type=self.name, inferred_pattern=self.resolution
            )

        except (ValueError, OSError, OverflowError) as e:
            logger.debug(f"Cannot cast the given data to {self.name}: {e}")
            return None

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        return to_datetime(column, unit=inferred_field.inferred_pattern.value)


def get_type() -> UnixTimestampType:
    return UnixTimestampType()
