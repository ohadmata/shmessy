import logging
from datetime import datetime
from typing import Optional

from numpy import ndarray

from .base import BaseValidator
from ..schema import InferredField, ValidatorTypes

logger = logging.getLogger(__name__)


class Validator(BaseValidator):
    validator_type = ValidatorTypes.NUMERIC
    ignore_nan: bool = True

    @classmethod
    def validate(cls, data: ndarray) -> Optional[InferredField]:
        for value in data:
            try:
                parsed_value = datetime.utcfromtimestamp(value)
                if parsed_value.year < 1990 or parsed_value.year > 2100:
                    return None
            except ValueError as e:
                break
        return InferredField(
            inferred_type=datetime
        )
