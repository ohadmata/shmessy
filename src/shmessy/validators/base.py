from abc import ABC, abstractmethod
from typing import Optional

from numpy import ndarray

from ..schema import InferredField, ValidatorTypes


class BaseValidator(ABC):
    validator_type: ValidatorTypes

    @classmethod
    @abstractmethod
    def validate(cls, data: ndarray) -> Optional[InferredField]:
        pass
