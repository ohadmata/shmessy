from typing import Optional, Tuple

import numpy as np
from numpy import ndarray
from pandas import Series

from ..schema import InferredField
from .base import BaseType


class BooleanType(BaseType):
    weight = 1
    patterns: list[Tuple] = [  # The first member should be the true value
        ("YES", "NO"),
        ("TRUE", "FALSE"),
        ("T", "F"),
        ("Y", "N"),
        (1, 0),
    ]

    @staticmethod
    def _validate_value_pattern(data: ndarray, pattern: Tuple) -> bool:
        match_first_value: bool = False
        match_second_value: bool = False

        for value in data:
            if isinstance(value, str):
                value = value.lower()
            if isinstance(pattern[0], str):
                pattern = (pattern[0].lower(), pattern[1].lower())
            if value == pattern[0]:
                match_first_value = True
            elif value == pattern[1]:
                match_second_value = True
            else:
                return False
        if match_first_value and match_second_value:
            return True
        return False

    def validate(self, data: ndarray) -> Optional[InferredField]:
        if data.dtype == np.dtype("bool"):
            return InferredField(inferred_type=self.name)
        for pattern in self.patterns:
            if self._validate_value_pattern(data, pattern):
                return InferredField(inferred_type=self.name, inferred_pattern=pattern)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        if not inferred_field.inferred_pattern:
            raise NotImplementedError()  # Missing pattern - Mean that the column recognized as boolean by pandas

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
