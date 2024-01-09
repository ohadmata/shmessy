from abc import ABC, abstractmethod
from typing import Optional, Tuple, Type

from numpy import issubdtype, ndarray, number, object_, str_
from pandas import Series

from ..schema import CastingTypes, InferredField


class BaseType(ABC):
    weight: int = 0
    casting_types: Tuple[CastingTypes]

    @abstractmethod
    def validate(self, data: ndarray) -> Optional[InferredField]:
        pass

    @abstractmethod
    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        pass

    def is_casting_type_valid(self, dtype: Type) -> bool:
        for possible_casting_type in self.casting_types:
            if self._check_single_validator_type(dtype, possible_casting_type):
                return True
        return False

    @staticmethod
    def _check_single_validator_type(
        dtype: Type, possible_casting_type: CastingTypes
    ) -> bool:
        if possible_casting_type == CastingTypes.NUMERIC and not issubdtype(
            dtype, number
        ):
            return False

        if possible_casting_type == CastingTypes.STRING and not (
            issubdtype(dtype, object_) or issubdtype(dtype, str_)
        ):
            return False
        return True

    @property
    def name(self) -> str:
        return str(self.__class__.__name__.replace("Type", ""))
