import re
from typing import Any, Optional


def exception_router(exception: Exception):
    error_message = str(exception)

    match = re.match(
        r"(.*)'(.*)' codec can't decode byte (.*) in position (.*):(.*)", error_message
    )
    if match is not None:
        raise WrongEncodingException(match.group(2))

    match = re.match(
        r"(.*)Expected (.*) fields in line (.*), saw (.*)\n", error_message
    )
    if match is not None:
        raise WrongNumberOfColumnException(
            num_of_expected=match.group(2),
            num_of_saw=match.group(4),
            line_number=match.group(3),
        )
    raise exception


class ShmessyException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class WrongNumberOfColumnException(ShmessyException):
    def __init__(self, num_of_expected: int, num_of_saw: int, line_number: int):
        super().__init__(
            f"Error in line {line_number}: Expected {num_of_expected} fields, found {num_of_saw}."
        )


class FieldCastingException(ShmessyException):
    def __init__(
        self,
        type_: str,
        bad_value: str,
        line_number: int,
        column_name: str,
        pattern: Optional[Any] = None,
    ):
        pattern_str = f"[{pattern}]" if pattern else ""
        super().__init__(
            f'Error in line {line_number:,} for column "{column_name}": '
            f'Couldn\'t cast value "{bad_value}" to type {type_}{pattern_str}.'
        )


class WrongEncodingException(ShmessyException):
    def __init__(self, expected_encoding: str):
        super().__init__(
            f"The given file cannot be read using {expected_encoding} encoding."
        )


class TooManyColumnException(ShmessyException):
    def __init__(self, existing_columns_num: int, max_columns_num: int):
        super().__init__(
            f"The input table contains {existing_columns_num} columns. "
            f"The maximum number of columns we support is {max_columns_num}."
        )
