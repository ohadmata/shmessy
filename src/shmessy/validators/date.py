from datetime import datetime
from typing import Optional

from numpy import ndarray

from .base import BaseValidator
from ..schema import InferredField, ValidatorTypes


class Validator(BaseValidator):
    validator_type = ValidatorTypes.STRING
    ignore_nan: bool = True
    patterns: list[str] = [
        "%m/%d/%Y", "%m-%d-%Y", "%m.%d.%Y",
        "%m/%d/%y", "%m-%d-%y", "%m.%d.%y",
        "%Y/%m/%d", "%Y-%m-%d", "%Y.%m.%d",
        "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y",
        "%d/%b/%Y", "%d-%b-%Y",
    ]

    def validate(self, data: ndarray) -> Optional[InferredField]:
        for pattern in self.patterns:
            valid: bool = True
            for value in data:
                try:
                    datetime.strptime(value, pattern)
                except ValueError:
                    valid = False
                    break
                except TypeError:
                    if not self.ignore_nan:
                        valid = False
            if valid:
                return InferredField(
                    inferred_type="date",
                    inferred_pattern=pattern
                )
