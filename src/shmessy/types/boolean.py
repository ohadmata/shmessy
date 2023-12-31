from typing import Optional, Tuple

from numpy import ndarray
from pandas import Series

from ..schema import InferredField, ValidatorTypes
from .base import BaseType


class BooleanType(BaseType):
    weight = 1
    validator_types = (ValidatorTypes.STRING, ValidatorTypes.NUMERIC)
    patterns: list[Tuple] = [  # The first member should be the true value
        ("YES", "NO"),
        ("TRUE", "FALSE"),
        ("T", "F"),
        ("Y", "N"),
        (1, 0),
    ]

    @staticmethod
    def _validate_value_pattern(data: ndarray, pattern: Tuple) -> bool:
        for value in data:
            if isinstance(value, str):
                value = value.lower()
            if isinstance(pattern[0], str):
                pattern = (pattern[0].lower(), pattern[1].lower())
            if value not in (pattern[0], pattern[1]):
                return False
        return True

    def validate(self, data: ndarray) -> Optional[InferredField]:
        if not self.is_validator_type_valid(dtype=data.dtype):
            return None

        for pattern in self.patterns:
            if self._validate_value_pattern(data, pattern):
                return InferredField(inferred_type=self.name, inferred_pattern=pattern)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        if isinstance(inferred_field.inferred_pattern[0], str):
            return column.apply(
                lambda x: True
                if x.lower() == inferred_field.inferred_pattern[0].lower()
                else False
            )

        return column.apply(
            lambda x: True if x == inferred_field.inferred_pattern[0] else False
        )


def get_type() -> BooleanType:
    return BooleanType()
