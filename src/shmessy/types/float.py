import locale
import logging
from typing import Any, Optional, Tuple

from numpy import ndarray
from pandas import Series, to_numeric
from pandas.api.types import is_numeric_dtype

from ..exceptions import FieldCastingException
from ..schema import InferredField
from .base import BaseType

logger = logging.getLogger(__name__)


class FloatType(BaseType):
    weight = 8

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for value in data:
            try:
                if isinstance(value, str):
                    float(locale.atof(value))
                else:
                    float(value)
            except Exception:  # noqa
                logger.debug(f"Cannot cast the value '{value}' to {self.name}")
                return None
        return InferredField(inferred_type=self.name)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        if is_numeric_dtype(column):
            return column
        try:
            return to_numeric(column.apply(locale.atof))
        except Exception as e:
            logger.debug(f"Couldn't cast column to type {self.name}: {e}")
            line_number, bad_value = self._extract_bad_value(column)
            raise FieldCastingException(
                type_=self.name, line_number=line_number, bad_value=bad_value
            )

    @staticmethod
    def _extract_bad_value(column: Series) -> Tuple[int, Any]:
        for idx, row in enumerate(column):
            try:
                float(row)  # noqa
            except Exception:  # noqa
                return idx, row

        # If we reached this piece of code - The dtype is probably an object - do nothing!
        raise NotImplementedError()


def get_type() -> FloatType:
    return FloatType()
