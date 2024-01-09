from typing import Optional

from numpy import ndarray
from pandas import Series
from pydantic import BaseModel, EmailStr

from ..schema import CastingTypes, InferredField
from .base import BaseType


class Model(BaseModel):
    email: EmailStr


class EmailType(BaseType):
    weight = 5
    casting_types = (CastingTypes.STRING,)

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for value in data:
            try:
                Model(email=value)
            except ValueError:
                return None
        return InferredField(inferred_type=self.name)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        # Email defined as a virtual data-type. Fix is not relevant.
        raise NotImplementedError()


def get_type() -> EmailType:
    return EmailType()
