import logging
from typing import Optional

from numpy import ndarray
from pandas import Series

from .base import BaseType
from ..schema import InferredField

logger = logging.getLogger(__name__)


class StringType(BaseType):
    weight = 9

    def validate(self, data: ndarray) -> Optional[InferredField]:
        str_dtype = str(data.dtype).lower()
        if str_dtype.startswith('datetime') or str_dtype.startswith('timedelta'):
            return None
        for value in data:
            try:
                str(value)
            except Exception:  # noqa
                logger.debug(f"Cannot cast the value '{value}' to {self.name}")
                return None
        return InferredField(inferred_type=self.name)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        raise NotImplementedError()


def get_type() -> StringType:
    return StringType()
