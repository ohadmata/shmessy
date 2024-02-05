import logging
from typing import Any, Dict, List, Type

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

from . import types
from .schema import Field
from .types.base import BaseType
from .types.boolean import BooleanType
from .types.datetime_ import DatetimeType
from .types.float import FloatType
from .types.integer import IntegerType
from .types.string import StringType

logger = logging.getLogger(__name__)


class TypesHandler:

    @property
    def __types(self) -> List[BaseType]:
        type_names = types.__all__
        types_objects = [getattr(types, type_)() for type_ in type_names]
        return types_objects

    @property
    def __types_as_dict(self) -> Dict[str, BaseType]:
        return {type_.name: type_ for type_ in self.__types}

    def fix_field(
        self, column: Series, inferred_field: Field, fallback_to_string: bool
    ) -> Any:
        try:
            fixed_field = self.__types_as_dict[inferred_field.inferred_type].fix(
                column=column, inferred_field=inferred_field
            )
            if fixed_field is not None:
                return fixed_field
        except NotImplementedError:
            pass
        except FieldCastingException as e:
            if not fallback_to_string:
                raise e
            logger.debug("Could not cast the field - Apply fallback to string")
            StringType().fix(column=column, inferred_field=inferred_field)
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
