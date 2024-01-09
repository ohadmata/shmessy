from typing import Optional

from numpy import ndarray
from pandas import Series

from ..schema import CastingTypes, InferredField
from .base import BaseType


class IntegerType(BaseType):
    weight = 7
    casting_types = (CastingTypes.STRING, CastingTypes.NUMERIC)

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for column in data:
            try:
                int(column)
            except Exception:  # noqa
                return None
        return InferredField(inferred_type=self.name)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        raise NotImplementedError()


def get_type() -> IntegerType:
    return IntegerType()
