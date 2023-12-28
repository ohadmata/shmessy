from typing import Optional

from numpy import ndarray
from pydantic import EmailStr, BaseModel

from .base import BaseValidator
from ..schema import InferredField, ValidatorTypes


class Model(BaseModel):
    email: EmailStr


class Validator(BaseValidator):
    validator_type = ValidatorTypes.STRING

    @classmethod
    def validate(cls, data: ndarray) -> Optional[InferredField]:
        for value in data:
            try:
                Model(email=value)
            except ValueError:
                return None
        return InferredField(
            inferred_type="string",
            inferred_virtual_type=EmailStr
        )
