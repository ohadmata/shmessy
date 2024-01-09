import logging
import math
from datetime import datetime
from enum import Enum
from typing import Optional

from numpy import ndarray
from pandas import Series, to_datetime

from ..schema import CastingTypes, InferredField
from .base import BaseType

logger = logging.getLogger(__name__)


class TimestampResolution(str, Enum):
    SECONDS = "s"
    MILLISECONDS = "ms"
    NANOSECONDS = "ns"


class UnixTimestampType(BaseType):
    weight = 4
    casting_types = (CastingTypes.NUMERIC,)
    min_valid_year: int = 1980
    max_valid_year: int = 2100

    @staticmethod
    def _unix_timestamp_resolution(value: float) -> TimestampResolution:
        number_of_digits = len(str(int(value)))
        if number_of_digits == 10:
            return TimestampResolution.SECONDS
        if number_of_digits == 13:
            return TimestampResolution.MILLISECONDS
        if number_of_digits == 16:
            return TimestampResolution.NANOSECONDS

    @staticmethod
    def _fix_input_resolution(
        value: float, selected_resolution: TimestampResolution
    ) -> float:
        if selected_resolution == TimestampResolution.SECONDS:
            return value
        if selected_resolution == TimestampResolution.MILLISECONDS:
            return value / 1000
        if selected_resolution == TimestampResolution.NANOSECONDS:
            return value / 1000 / 1000

    def validate(self, data: ndarray) -> Optional[InferredField]:
        try:
            selected_resolution = self._unix_timestamp_resolution(float(data[0]))
            if not selected_resolution:
                return None
            for value in data:
                if not math.isnan(value):
                    parsed_value = datetime.utcfromtimestamp(
                        self._fix_input_resolution(value, selected_resolution)
                    )
                    if (
                        parsed_value.year < self.min_valid_year
                        or parsed_value.year > self.max_valid_year
                    ):
                        return None

            return InferredField(
                inferred_type=self.name, inferred_pattern=selected_resolution
            )
        except ValueError:
            return None

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        return to_datetime(column, unit=inferred_field.inferred_pattern.value)


def get_type() -> UnixTimestampType:
    return UnixTimestampType()
