from datetime import datetime

from numpy import ndarray


def validate_strptime_pattern(data: ndarray, pattern: str) -> bool:
    for value in data:
        try:
            if isinstance(value, str):
                datetime.strptime(value, pattern)
        except ValueError:
            return False
    return True
