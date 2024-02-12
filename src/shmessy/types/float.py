import locale
import logging
from typing import Any, Optional, Tuple

import numpy as np
from numpy import ndarray

from ..schema import InferredField
from .base import BaseType

logger = logging.getLogger(__name__)


class FloatType(BaseType):
    weight = 8

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for value in data:
            try:
                self.cast(value)
            except Exception:  # noqa
                logger.debug(f"Cannot cast the value '{value}' to {self.name}")
                return None
        return InferredField(inferred_type=self.name)

    def cast(self, value: Any, pattern: Optional[Any] = None) -> Optional[Any]:
        if isinstance(value, str):
            return float(locale.atof(value))
        return float(value)

    def ignore_cast_for_types(self) -> Tuple[Any]:
        return (np.dtype("float64"),)
