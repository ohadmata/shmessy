from typing import Optional

from numpy import ndarray
from pandas import Series
from pydantic import BaseModel
from pydantic.networks import IPv4Address  # noqa

from ..schema import CastingTypes, InferredField
from .base import BaseType


class Model(BaseModel):
    ip: IPv4Address


class IPv4Type(BaseType):
    weight = 6
    casting_types = (CastingTypes.STRING,)

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for value in data:
            try:
                Model(ip=value)
            except ValueError:
                return None
        return InferredField(inferred_type=self.name)

    def fix(self, column: Series, inferred_field: InferredField) -> Series:
        # IP defined as a virtual data-type. Fix is not relevant.
        raise NotImplementedError()


def get_type() -> IPv4Type:
    return IPv4Type()
