import logging
import os
from importlib import import_module
from types import ModuleType
from typing import Any, List, Optional

from numpy import ndarray

from .schema import Field
from .validators.base import BaseValidator

logger = logging.getLogger(__name__)


class ValidatorsHandler:
    PACKAGE_NAME: str = "shmessy"
    VALIDATORS_DIR: str = "validators"

    def __init__(self):
        self.__validators = self._discover_validators()

    @classmethod
    def _discover_validators(cls) -> List[BaseValidator]:
        validators: List[BaseValidator] = []
        root_directory = os.path.join(os.path.dirname(__file__))
        validators_directory = os.path.join(root_directory, cls.VALIDATORS_DIR)

        for filename in os.listdir(validators_directory):
            if cls._is_validator(filename):
                validators.append(cls._load_validator(filename).Validator())
        return validators

    @classmethod
    def _load_validator(cls, validator_filename: str) -> Optional[ModuleType]:
        module = f"{cls.PACKAGE_NAME}.{cls.VALIDATORS_DIR}.{validator_filename.replace('.py', '')}"
        try:
            return import_module(module)
        except (ImportError, ValueError, AttributeError) as e:
            logger.error(f"Couldn't import {module}, error is: {e}")

    @staticmethod
    def _is_validator(filename: str) -> bool:
        if "__" in filename or "base" in filename:
            return False
        return True

    def fix_field(self, column: Any, sample_size: int) -> Any:
        for validator in self.__validators:
            fixed_field = validator.fix(column=column, sample_size=sample_size)
            if fixed_field is not None:
                return fixed_field

        return column

    def infer_field(self, field_name: str, data: ndarray) -> Field:

        for validator in self.__validators:
            inferred = validator.validate(data)
            if inferred:
                return Field(
                    field_name=field_name,
                    source_type=data.dtype.type,
                    inferred_type=inferred.inferred_type,
                    inferred_virtual_type=inferred.inferred_virtual_type,
                    inferred_pattern=inferred.inferred_pattern,
                )

        return Field(field_name=field_name, source_type=data.dtype.type)
