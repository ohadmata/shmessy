import locale
import logging
from typing import Optional

from numpy import ndarray
from pandas import Series, to_numeric
from pandas.api.types import is_numeric_dtype

from ..schema import InferredField
from .base import BaseType

logger = logging.getLogger(__name__)


class IntegerType(BaseType):
    weight = 7

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for value in data:
            try:
                if isinstance(value, str):
                    int(locale.atoi(value))
                else:
                    int(value)
            except Exception:  # noqa
                logger.debug(f"Cannot cast the value '{value}' to {self.name}")
                return None
        return InferredField(inferred_type=self.name)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        if is_numeric_dtype(column):
            return column
        return to_numeric(column.apply(locale.atoi))


def get_type() -> IntegerType:
    return IntegerType()
