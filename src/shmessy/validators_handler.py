import logging
import os
from importlib import import_module
from types import ModuleType
from .validators.base import BaseValidator
from typing import List, Optional

from numpy import ndarray, issubdtype, number, object_, str_

from .schema import ValidatorTypes, Field

logger = logging.getLogger(__name__)


class ValidatorsHandler:
    PACKAGE_NAME: str = "shmessy"
    VALIDATORS_DIR: str = "validators"

    def __init__(self):
        self.__validators = self._discover_validators()

    @classmethod
    def _discover_validators(cls) -> List[BaseValidator]:
        validators: List[BaseValidator] = list()
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

    def infer_field(self, field_name: str, data: ndarray) -> Field:

        for validator in self.__validators:
            if validator.validator_type == ValidatorTypes.NUMERIC and issubdtype(data.dtype, number):
                inferred = validator.validate(data)
                if inferred:
                    return Field(
                        field_name=field_name,
                        source_type=data.dtype.type,
                        inferred_type=inferred.inferred_type,
                        inferred_virtual_type=inferred.inferred_virtual_type,
                        inferred_pattern=inferred.inferred_pattern,
                    )

            if (validator.validator_type == ValidatorTypes.STRING and
                    (issubdtype(data.dtype, object_) or issubdtype(data.dtype, str_))):
                inferred = validator.validate(data)
                if inferred:
                    return Field(
                        field_name=field_name,
                        source_type=data.dtype.type,
                        inferred_type=inferred.inferred_type,
                        inferred_virtual_type=inferred.inferred_virtual_type,
                        inferred_pattern=inferred.inferred_pattern,
                    )

        return Field(
            field_name=field_name,
            source_type=data.dtype.type
        )
