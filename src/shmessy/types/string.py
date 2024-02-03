import logging
from typing import Optional

from numpy import ndarray
from pandas import Series

from ..schema import InferredField
from .base import BaseType

logger = logging.getLogger(__name__)


class StringType(BaseType):
    weight = 9

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for value in data:
            try:
                str(value)
            except Exception:  # noqa
                logger.debug(f"Cannot cast the value '{value}' to {self.name}")
                return None
        return InferredField(inferred_type=self.name)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        return column.apply(lambda x: str(x))


def get_type() -> StringType:
    return StringType()
