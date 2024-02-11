import logging
from typing import Any, Optional, Tuple

import numpy as np
from numpy import ndarray

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

    def cast(self, value: Any, pattern: Optional[Any] = None) -> Optional[Any]:
        return str(value)

    def ignore_cast_for_types(self) -> Tuple[Any]:
        return (np.dtype("O"),)


def get_type() -> StringType:
    return StringType()
