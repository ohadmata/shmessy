import logging
import math
from datetime import datetime

from numpy import ndarray

logger = logging.getLogger(__name__)


def validate_strptime_pattern(data: ndarray, pattern: str) -> bool:
    validated: bool = False
    for value in data:
        try:
            if isinstance(value, str) or not math.isnan(value):
                datetime.strptime(str(value), pattern)
                validated = True
        except ValueError:
            logger.debug(f"Cannot cast the value '{value}' using pattern '{pattern}'")
            return False
    return validated
