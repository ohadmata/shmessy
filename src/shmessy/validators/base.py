from abc import ABC, abstractmethod
from typing import Optional, Type, Any
from pandas import Series
from numpy import ndarray, issubdtype, number, object_, str_

from ..schema import InferredField, ValidatorTypes


class BaseValidator(ABC):
    validator_type: ValidatorTypes

    @abstractmethod
    def validate(self, data: ndarray) -> Optional[InferredField]:
        pass

    @abstractmethod
    def fix(self, column: Series, sample_size: int) -> Series:
        pass

    def check_validation_type(self, dtype: Type) -> None:
        if self.validator_type == ValidatorTypes.NUMERIC and not issubdtype(dtype, number):
            raise ValueError(f"NUMERIC validation is not supported for {dtype}")

        if (self.validator_type == ValidatorTypes.STRING and
                not (issubdtype(dtype, object_) or issubdtype(dtype, str_))):
            raise ValueError(f"STRING validation is not supported for {dtype}")
