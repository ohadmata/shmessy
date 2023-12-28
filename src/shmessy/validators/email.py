from typing import Optional

from numpy import ndarray
from pandas import Series
from pydantic import EmailStr, BaseModel

from .base import BaseValidator
from ..schema import InferredField, ValidatorTypes


class Model(BaseModel):
    email: EmailStr


class Validator(BaseValidator):
    validator_type = ValidatorTypes.STRING

    def validate(self, data: ndarray) -> Optional[InferredField]:
        try:
            self.check_validation_type(dtype=data.dtype)
        except ValueError:
            return None

        for value in data:
            try:
                Model(email=value)
            except ValueError:
                return None
        return InferredField(
            inferred_type=str,
            inferred_virtual_type=EmailStr
        )

    def fix(self, column: Series, sample_size: int) -> Series:
        sample_data = column[:sample_size]
        inferred = self.validate(sample_data)
        if inferred:
            return column
