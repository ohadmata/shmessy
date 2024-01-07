import logging
import os
from importlib import import_module
from types import ModuleType
from typing import Any, List, Optional

from numpy import ndarray

from .schema import Field
from .types.base import BaseType

logger = logging.getLogger(__name__)


class TypesHandler:
    PACKAGE_NAME: str = "shmessy"
    TYPES_DIR: str = "types"

    def __init__(self):
        self.__types = self._discover_types()

    @classmethod
    def _discover_types(cls) -> List[BaseType]:
        types: List[BaseType] = []
        root_directory = os.path.join(os.path.dirname(__file__))
        types_directory = os.path.join(root_directory, cls.TYPES_DIR)

        for filename in os.listdir(types_directory):
            try:
                types.append(cls._load_type(filename).get_type())
            except AttributeError:
                pass  # ignore types without factory (Such as base types)
        return types

    @classmethod
    def _load_type(cls, type_filename: str) -> Optional[ModuleType]:
        module = (
            f"{cls.PACKAGE_NAME}.{cls.TYPES_DIR}.{type_filename.replace('.py', '')}"
        )
        try:
            return import_module(module)
        except (ImportError, ValueError, AttributeError) as e:
            logger.error(f"Couldn't import {module}: {e}")

    def fix_field(self, column: Any, sample_size: Optional[int] = 1000) -> Any:
        for type_ in self.__types:
            try:
                fixed_field = type_.fix(column=column, sample_size=sample_size)
                if fixed_field is not None:
                    return fixed_field
            except NotImplementedError:
                pass

        return column

    def infer_field(self, field_name: str, data: ndarray) -> Field:

        for type_ in self.__types:
            inferred = type_.validate(data)
            if inferred:
                return Field(
                    field_name=field_name,
                    source_type=str(data.dtype.type),
                    inferred_type=inferred.inferred_type,
                    inferred_pattern=inferred.inferred_pattern,
                )

        return Field(field_name=field_name, source_type=str(data.dtype.type))
