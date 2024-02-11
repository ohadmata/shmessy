import logging
import os
from importlib import import_module
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

from numpy import ndarray
from numpy.dtypes import (
    BoolDType,
    DateTime64DType,
    Float16DType,
    Float32DType,
    Float64DType,
    Int8DType,
    Int16DType,
    Int32DType,
    Int64DType,
    IntDType,
    ObjectDType,
    StrDType,
)
from pandas import Series

from shmessy.exceptions import FieldCastingException

from .schema import Field, InferredField
from .types.base import BaseType
from .types.boolean import BooleanType
from .types.datetime_ import DatetimeType
from .types.float import FloatType
from .types.integer import IntegerType
from .types.string import StringType

logger = logging.getLogger(__name__)


class TypesHandler:
    PACKAGE_NAME: str = "shmessy"
    TYPES_DIR: str = "types"

    def __init__(self):
        self.__types = self._discover_types()
        self.__types_as_dict: Dict[str, BaseType] = self._types_as_dict(self.__types)

    @classmethod
    def _types_as_dict(cls, __types: List[BaseType]) -> Dict[str, BaseType]:
        res = {}
        for type_ in __types:
            res[type_.name] = type_
        return res

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

    @staticmethod
    def _extract_bad_value(column: Series, func: Callable) -> Tuple[int, Any]:
        for idx, row in enumerate(column):
            try:
                func(row)  # noqa
            except Exception:  # noqa
                return idx + 2, row

        # If we reached this piece of code - The dtype is probably an object - do nothing!
        raise NotImplementedError()

    def _fix_column(
        self, column: Series, inferred_field: InferredField, type_: BaseType
    ) -> Series:
        try:
            if column.dtype.type in type_.ignore_cast_for_types():
                return column
            return column.apply(
                lambda x: type_.cast(x, inferred_field.inferred_pattern)
            )
        except Exception as e:
            logger.debug(f"Couldn't cast column to type {type_.name}: {e}")
            line_number, bad_value = self._extract_bad_value(
                column=column,
                func=lambda x: type_.cast(
                    value=x, pattern=inferred_field.inferred_pattern
                ),
            )
            raise FieldCastingException(
                type_=type_.name,
                line_number=line_number,
                bad_value=bad_value,
                column_name=str(column.name),
                pattern=inferred_field.inferred_pattern,
            )

    def fix_field(
        self, column: Series, inferred_field: Field, fallback_to_string: bool
    ) -> Any:
        try:
            fixed_field = self._fix_column(
                column=column,
                inferred_field=inferred_field,
                type_=self.__types_as_dict[inferred_field.inferred_type],
            )
            if fixed_field is not None:
                return fixed_field
        except FieldCastingException as e:
            if not fallback_to_string:
                raise e
            logger.debug("Could not cast the field - Apply fallback to string")
            self._fix_column(
                column=column, inferred_field=inferred_field, type_=StringType()
            )
        return column

    def infer_field(self, field_name: str, data: ndarray) -> Field:
        sorted_types = sorted(self.__types, key=lambda x: x.weight)
        for type_ in sorted_types:
            logger.debug(f"Trying to match column {field_name} to type {type_.name}")
            inferred = type_.validate(data)
            if inferred:
                return Field(
                    field_name=field_name,
                    source_type=_numpy_type_shmessy_type(data.dtype),
                    inferred_type=inferred.inferred_type,
                    inferred_pattern=inferred.inferred_pattern,
                )

        return Field(
            field_name=field_name, source_type=_numpy_type_shmessy_type(data.dtype)
        )


def _numpy_type_shmessy_type(numpy_type: Type) -> str:
    if isinstance(
        numpy_type,
        (
            IntDType,
            Int64DType,
            Int8DType,
            Int16DType,
            Int32DType,
        ),
    ):
        return IntegerType().name
    if isinstance(numpy_type, (ObjectDType, StrDType)):
        return StringType().name
    if isinstance(numpy_type, BoolDType):
        return BooleanType().name
    if isinstance(numpy_type, DateTime64DType):
        return DatetimeType().name
    if isinstance(numpy_type, (Float16DType, Float32DType, Float64DType)):
        return FloatType().name
    return str(numpy_type)
