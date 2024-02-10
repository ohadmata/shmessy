import logging
from datetime import datetime
from typing import Any, Callable, Tuple

from numpy import ndarray
from pandas import Series

logger = logging.getLogger(__name__)


def validate_strptime_pattern(data: ndarray, pattern: str) -> bool:
    validated: bool = False
    for value in data:
        try:
            if isinstance(value, str):  # For security reasons & skip nan values
                datetime.strptime(value, pattern)
                validated = True
        except ValueError:
            logger.debug(f"Cannot cast the value '{value}' using pattern '{pattern}'")
            return False
    return validated


def extract_bad_value(column: Series, func: Callable) -> Tuple[int, Any]:
    for idx, row in enumerate(column):
        try:
            func(row)  # noqa
        except Exception:  # noqa
            return idx + 2, row

    # If we reached this piece of code - The dtype is probably an object - do nothing!
    raise NotImplementedError()
