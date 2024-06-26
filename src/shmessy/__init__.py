import locale
import logging
import time
from typing import BinaryIO, List, Optional, TextIO, Union

import pandas as pd
from pandas import DataFrame

from .exceptions import exception_router
from .schema import ShmessySchema
from .types_handler import TypesHandler
from .utils import (
    _check_number_of_columns,
    _fix_column_names,
    _fix_column_names_in_df,
    _fix_column_names_in_shmessy_schema,
    _get_dialect,
    _get_sampled_df,
)

logger = logging.getLogger(__name__)


class Shmessy:
    def __init__(
        self,
        sample_size: Optional[int] = 1000,
        reader_encoding: Optional[str] = "UTF-8",
        locale_formatter: Optional[str] = "en_US",
        use_random_sample: Optional[bool] = True,
        types_to_ignore: Optional[List[str]] = None,
        max_columns_num: Optional[int] = 500,
        fallback_to_string: Optional[bool] = False,
        fallback_to_null: Optional[bool] = False,
        use_csv_sniffer: Optional[bool] = True,
        fix_column_names: Optional[bool] = False,
    ) -> None:
        self.__types_handler = TypesHandler(types_to_ignore=types_to_ignore)
        self.__sample_size = sample_size
        self.__reader_encoding = reader_encoding
        self.__locale_formatter = locale_formatter
        self.__use_random_sample = use_random_sample
        self.__max_columns_num = max_columns_num
        self.__fallback_to_string = fallback_to_string
        self.__fallback_to_null = fallback_to_null
        self.__use_csv_sniffer = use_csv_sniffer
        self.__fix_column_names = fix_column_names

        self.__inferred_schema: Optional[ShmessySchema] = None

        locale.setlocale(
            locale.LC_ALL, f"{self.__locale_formatter}.{self.__reader_encoding}"
        )

    def get_inferred_schema(self) -> ShmessySchema:
        return self.__inferred_schema

    def infer_schema(self, df: DataFrame) -> ShmessySchema:
        _check_number_of_columns(df=df, max_columns_num=self.__max_columns_num)
        start_time = time.time()
        df = _get_sampled_df(
            df=df,
            sample_size=self.__sample_size,
            random_sample=self.__use_random_sample,
        )
        columns = [
            self.__types_handler.infer_field(field_name=column, data=df[column].values)
            for column in df
        ]
        infer_duration_ms = int((time.time() - start_time) * 1000)
        inferred_schema = ShmessySchema(
            columns=columns, infer_duration_ms=infer_duration_ms
        )
        self.__inferred_schema = inferred_schema
        return inferred_schema

    def fix_schema(self, df: DataFrame) -> DataFrame:
        try:
            _check_number_of_columns(df=df, max_columns_num=self.__max_columns_num)
            fixed_schema = self.infer_schema(df)

            for column in fixed_schema.columns:
                df[column.field_name] = self.__types_handler.fix_field(
                    column=df[column.field_name],
                    inferred_field=column,
                    fallback_to_string=self.__fallback_to_string,
                    fallback_to_null=self.__fallback_to_null,
                )

            if self.__fix_column_names:
                mapping = _fix_column_names(df)
                df = _fix_column_names_in_df(input_df=df, mapping=mapping)
                fixed_schema = _fix_column_names_in_shmessy_schema(
                    input_schema=fixed_schema, mapping=mapping
                )

            self.__inferred_schema = fixed_schema
            return df
        except Exception as e:
            exception_router(e)

    def read_csv(self, filepath_or_buffer: Union[str, TextIO, BinaryIO]) -> DataFrame:
        try:
            dialect = (
                _get_dialect(
                    filepath_or_buffer=filepath_or_buffer,
                    sample_size=self.__sample_size,
                    reader_encoding=self.__reader_encoding,
                )
                if self.__use_csv_sniffer
                else None
            )

            df = pd.read_csv(
                index_col=False,
                filepath_or_buffer=filepath_or_buffer,
                dialect=dialect() if dialect else None,  # noqa
                encoding=self.__reader_encoding,
            )

            return self.fix_schema(df=df)

        except Exception as e:
            exception_router(e)
