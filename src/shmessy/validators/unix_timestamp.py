import logging
from datetime import datetime
from typing import Optional
import math

from numpy import ndarray
from pandas import Series, to_datetime

from .base import BaseValidator
from ..schema import InferredField, ValidatorTypes

logger = logging.getLogger(__name__)


class Validator(BaseValidator):
    validator_type = ValidatorTypes.NUMERIC
    ignore_nan: bool = True

    def validate(self, data: ndarray) -> Optional[InferredField]:
        try:
            self.check_validation_type(dtype=data.dtype)
            for value in data:
                if not math.isnan(value):
                    parsed_value = datetime.utcfromtimestamp(value)
                    if parsed_value.year < 1990 or parsed_value.year > 2100:
                        return None

            return InferredField(
                inferred_type=datetime
            )
        except ValueError:
            return None

    def fix(self, column: Series, sample_size: int) -> Series:
        sample_data = column[:sample_size]
        inferred = self.validate(sample_data)
        if inferred:
            return to_datetime(column, unit="s")
