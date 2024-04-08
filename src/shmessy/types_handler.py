import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

from numpy import nan, ndarray
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
from .types.date import DateType
from .types.datetime_ import DatetimeType
from .types.email import EmailType
from .types.float import FloatType
from .types.integer import IntegerType
from .types.ipv4_address import IPv4Type
from .types.string import StringType
from .types.unix_timestamp import UnixTimestampType

logger = logging.getLogger(__name__)


class TypesHandler:
    PACKAGE_NAME: str = "shmessy"
    TYPES_DIR: str = "types"

    def __init__(self, types_to_ignore: List[str]):
        self.__types = self._discover_types(types_to_ignore=types_to_ignore)
        self.__types_as_dict: Dict[str, BaseType] = self._types_as_dict(self.__types)

    @classmethod
    def _types_as_dict(cls, __types: List[BaseType]) -> Dict[str, BaseType]:
        res = {}
        for type_ in __types:
            res[type_.name] = type_
        return res

    @classmethod
    def _discover_types(cls, types_to_ignore: List[str]) -> List[BaseType]:
        filtered_types = []
        types_to_ignore = (
            [x.lower() for x in types_to_ignore] if types_to_ignore else []
        )
        types = [
            BooleanType(),
            DatetimeType(),
            DateType(),
            FloatType(),
            IntegerType(),
            StringType(),
            UnixTimestampType(),
            IPv4Type(),
            EmailType(),
        ]

        for _type in types:
            if _type.name.lower() not in types_to_ignore:
                filtered_types.append(_type)

        return sorted(filtered_types, key=lambda x: x.weight)

    @staticmethod
    def _extract_bad_value(column: Series, func: Callable) -> Tuple[int, Any]:
        for idx, row in enumerate(column):
            try:
                func(row)  # noqa
            except Exception:  # noqa
                return idx + 2, row

        # If we reached this piece of code - The dtype is probably an object - do nothing!
        raise NotImplementedError()

    @staticmethod
    def _cast_with_fallback_to_null(
        value: Any, inferred_pattern: Any, type_: BaseType
    ) -> Any:
        try:
            return type_.cast_value(value, inferred_pattern)
        except Exception as e:
            logger.debug(e)
            return nan

    def _fix_column(
        self,
        column: Series,
        inferred_field: InferredField,
        type_: BaseType,
        fallback_to_null: Optional[bool] = False,
    ) -> Series:
        try:
            if column.dtype.type in type_.ignore_cast_for_types():
                return column
            if type_.prefer_column_casting:
                try:
                    return type_.cast_column(column, inferred_field)
                except Exception as e:  # noqa
                    logger.debug(f"Cannot cast column to type: {type_}. Error: {e}")

                    if fallback_to_null:
                        logger.debug(
                            f"Trying to cast column to type: {type_} using FallbackToNull"
                        )
                        return column.apply(
                            lambda x: self._cast_with_fallback_to_null(
                                x, inferred_field.inferred_pattern, type_
                            )
                        )

            if fallback_to_null:
                logger.debug(
                    f"Trying to cast column to type: {type_} using FallbackToNull"
                )
                return column.apply(
                    lambda x: self._cast_with_fallback_to_null(
                        x, inferred_field.inferred_pattern, type_
                    )
                )

            return column.apply(
                lambda x: type_.cast_value(x, inferred_field.inferred_pattern)
            )
        except Exception as e:
            logger.debug(f"Couldn't cast column to type {type_.name}: {e}")
            try:
                line_number, bad_value = self._extract_bad_value(
                    column=column,
                    func=lambda x: type_.cast_value(
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
            except NotImplementedError:
                pass

    def fix_field(
        self,
        column: Series,
        inferred_field: Field,
        fallback_to_string: bool,
        fallback_to_null: bool,
    ) -> Any:
        try:
            return self._fix_column(
                column=column,
                inferred_field=inferred_field,
                type_=self.__types_as_dict[inferred_field.inferred_type],
            )

        except FieldCastingException as e:
            logger.debug(e)

            if fallback_to_string:
                logger.debug("Could not cast the field - Apply fallback to string")
                return self._fix_column(
                    column=column, inferred_field=inferred_field, type_=StringType()
                )

            if fallback_to_null:
                return self._fix_column(
                    column=column,
                    inferred_field=inferred_field,
                    type_=self.__types_as_dict[inferred_field.inferred_type],
                    fallback_to_null=True,
                )
            raise e

    def infer_field(self, field_name: str, data: ndarray) -> Field:
        for type_ in self.__types:
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
