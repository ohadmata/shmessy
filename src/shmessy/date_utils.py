import logging
import math
from datetime import datetime
from typing import Any, Optional

from numpy import datetime64, ndarray
from pandas import Timestamp

from .schema import InferredField

logger = logging.getLogger(__name__)


def is_empty_value(value: Any) -> bool:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return True
    return False


def cast_value(value: Any, pattern: Optional[Any] = None) -> Optional[Any]:
    if is_empty_value(value):
        return None
    if isinstance(value, (datetime64, Timestamp)):
        return value
    if isinstance(value, str):
        return datetime.strptime(value, pattern)
    raise Exception("Input type for date/datetime casting must be string.")


def validate(
    data: ndarray, patterns: list[str], inferred_type: str
) -> Optional[InferredField]:
    for pattern in patterns:
        valid_pattern = True
        at_least_single_not_nan_value = False
        for value in data:
            try:
                cast_value(value, pattern)
                if not is_empty_value(value):
                    at_least_single_not_nan_value = True
            except ValueError as e:  # Not match the pattern
                logger.debug(e)
                valid_pattern = False
                break
            except Exception as e:  # Any other exception
                logger.debug(e)
                return None

        if valid_pattern and at_least_single_not_nan_value:
            return InferredField(inferred_type=inferred_type, inferred_pattern=pattern)
