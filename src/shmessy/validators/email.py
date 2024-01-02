from typing import Optional

from numpy import ndarray
from pandas import Series
from pydantic import BaseModel, EmailStr

from ..schema import InferredField, ValidatorTypes
from .base import BaseValidator


class Model(BaseModel):
    email: EmailStr


class Validator(BaseValidator):
    validator_types = (ValidatorTypes.STRING,)

    def validate(self, data: ndarray) -> Optional[InferredField]:
        if not self.is_validator_type_valid(dtype=data.dtype):
            return None

        for value in data:
            try:
                Model(email=value)
            except ValueError:
                return None
        return InferredField(inferred_type=str, inferred_virtual_type=EmailStr)

    def fix(self, column: Series, sample_size: int) -> Series:
        # Email defined as a virtual data-type. Fix is not relevant.
        raise NotImplementedError()
