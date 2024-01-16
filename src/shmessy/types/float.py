from typing import Optional

from numpy import ndarray
from pandas import Series

from ..schema import InferredField
from .base import BaseType


class FloatType(BaseType):
    weight = 8

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for column in data:
            try:
                float(column)
            except Exception:  # noqa
                return None
        return InferredField(inferred_type=self.name)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        raise NotImplementedError()


def get_type() -> FloatType:
    return FloatType()
