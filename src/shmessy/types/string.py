from typing import Optional

from numpy import ndarray
from pandas import Series

from ..schema import CastingTypes, InferredField
from .base import BaseType


class StringType(BaseType):
    weight = 9
    casting_types = (CastingTypes.STRING, CastingTypes.NUMERIC)

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for column in data:
            try:
                str(column)
            except Exception:  # noqa
                return None
        return InferredField(inferred_type=self.name)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        raise NotImplementedError()


def get_type() -> StringType:
    return StringType()
