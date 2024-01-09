from typing import Optional

from numpy import ndarray
from pandas import Series
from pydantic import BaseModel, EmailStr

from ..schema import InferredField, ValidatorTypes
from .base import BaseType


class Model(BaseModel):
    email: EmailStr


class EmailType(BaseType):
    weight = 5
    validator_types = (ValidatorTypes.STRING,)

    def validate(self, data: ndarray) -> Optional[InferredField]:
        if not self.is_validator_type_valid(dtype=data.dtype):
            return None

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
