import re


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

    match = re.match(
        r"(.*)data (.*) doesn't match format (.*), at position(.*)", error_message
    )
    if match is not None:
        raise FormatCastingException(
            bad_value=match.group(2), expected_format=match.group(3)
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


class FormatCastingException(ShmessyException):
    def __init__(self, bad_value: str, expected_format: str):
        super().__init__(
            f"The value {bad_value} doesn't match format {expected_format}."
        )


class FieldCastingException(ShmessyException):
    def __init__(self, type_: str, bad_value: str, line_number: int):
        super().__init__(
            f'Error in line: {line_number}: Couldn\'t cast value "{bad_value}" to type {type_}.'
        )


class WrongEncodingException(ShmessyException):
    def __init__(self, expected_encoding: str):
        super().__init__(
            f"The given file cannot be read using {expected_encoding} encoding."
        )
