from datetime import datetime

from numpy import ndarray


def validate_strptime_pattern(data: ndarray, pattern: str) -> bool:
    validated: bool = False
    for value in data:
        try:
            if isinstance(value, str):  # For security reasons & skip nan values
                datetime.strptime(value, pattern)
                validated = True
        except ValueError:
            return False
    return validated
