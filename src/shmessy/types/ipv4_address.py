import logging
from typing import Any, Optional

from numpy import ndarray
from pydantic import BaseModel
from pydantic.networks import IPv4Address  # noqa

from ..schema import InferredField
from .base import BaseType

logger = logging.getLogger(__name__)


class Model(BaseModel):
    ip: IPv4Address


class IPv4Type(BaseType):
    weight = 6

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for value in data:
            try:
                if not isinstance(value, str):
                    logger.debug(
                        f"Value '{value}' is not string, cannot cast to {self.name}"
                    )
                    return None
                Model(ip=value)
            except ValueError:
                logger.debug(f"Cannot cast the value '{value}' to {self.name}")
                return None
        return InferredField(inferred_type=self.name)

    def cast(self, value: Any, pattern: Optional[Any] = None) -> Optional[Any]:
        return str(value)


def get_type() -> IPv4Type:
    return IPv4Type()
