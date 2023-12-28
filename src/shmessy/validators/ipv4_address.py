from typing import Optional

from numpy import ndarray
from pydantic import BaseModel
from pydantic.networks import IPv4Address  # noqa

from .base import BaseValidator
from ..schema import InferredField, ValidatorTypes


class Model(BaseModel):
    ip: IPv4Address


class Validator(BaseValidator):
    validator_type = ValidatorTypes.STRING

    @classmethod
    def validate(cls, data: ndarray) -> Optional[InferredField]:
        for value in data:
            try:
                Model(ip=value)
            except ValueError:
                return None
        return InferredField(
            inferred_type=str,
            inferred_virtual_type=IPv4Address
        )
