import logging
from typing import Optional

from numpy import ndarray
from pandas import Series
from pydantic import BaseModel, EmailStr

from ..schema import InferredField
from .base import BaseType

logger = logging.getLogger(__name__)


class Model(BaseModel):
    email: EmailStr


class EmailType(BaseType):
    weight = 5

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for value in data:
            try:
                Model(email=value)
            except ValueError:
                logger.debug(f"Cannot cast the value '{value}' to {self.name}")
                return None
        return InferredField(inferred_type=self.name)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        # Email defined as a virtual data-type. Fix is not relevant.
        raise NotImplementedError()


def get_type() -> EmailType:
    return EmailType()
