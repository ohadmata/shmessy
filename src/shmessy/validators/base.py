from abc import ABC, abstractmethod
from typing import Optional, Type

from numpy import issubdtype, ndarray, number, object_, str_
from pandas import Series

from ..schema import InferredField, ValidatorTypes


class BaseValidator(ABC):
    validator_type: ValidatorTypes

    @abstractmethod
    def validate(self, data: ndarray) -> Optional[InferredField]:
        pass

    @abstractmethod
    def fix(self, column: Series, sample_size: int) -> Series:
        pass

    def is_validator_type_valid(self, dtype: Type) -> bool:
        if self.validator_type == ValidatorTypes.NUMERIC and not issubdtype(
            dtype, number
        ):
            return False

        if self.validator_type == ValidatorTypes.STRING and not (
            issubdtype(dtype, object_) or issubdtype(dtype, str_)
        ):
            return False
        return True
