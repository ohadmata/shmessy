import csv
import logging
import time
from typing import BinaryIO, Optional, TextIO, Union

import pandas as pd
from pandas import DataFrame

from .schema import ShmessySchema
from .types_handler import TypesHandler
from .utils import _fix_column_names, _get_sample_from_csv, _get_sampled_df

logger = logging.getLogger(__name__)


class Shmessy:
    def __init__(self, sample_size: Optional[int] = 1000) -> None:
        self.__types_handler = TypesHandler()
        self.__sample_size = sample_size
        self.__csv_reader_encoding: str = "UTF-8"

    def infer_schema(self, df: DataFrame) -> ShmessySchema:
        start_time = time.time()
        df = _get_sampled_df(df=df, sample_size=self.__sample_size)
        columns = [
            self.__types_handler.infer_field(field_name=column, data=df[column].values)
            for column in df
        ]
        infer_duration_ms = int((time.time() - start_time) * 1000)

        return ShmessySchema(columns=columns, infer_duration_ms=infer_duration_ms)

    def fix_schema(
        self,
        df: DataFrame,
        *,
        fix_column_names: Optional[bool] = False,
        fixed_schema: Optional[ShmessySchema] = None
    ) -> (DataFrame, ShmessySchema):
        if fixed_schema is None:
            fixed_schema = self.infer_schema(df)

        for column in fixed_schema.columns:
            df[column.field_name] = self.__types_handler.fix_field(
                column=df[column.field_name], inferred_field=column
            )

        if fix_column_names:
            df = _fix_column_names(df)

        return df, fixed_schema

    def read_csv(
        self,
        filepath_or_buffer: Union[str, TextIO, BinaryIO],
        *,
        use_sniffer: Optional[bool] = True,
        fixed_schema: Optional[ShmessySchema] = None
    ) -> (DataFrame, ShmessySchema):
        if use_sniffer:
            dialect = csv.Sniffer().sniff(
                sample=_get_sample_from_csv(
                    filepath_or_buffer=filepath_or_buffer,
                    sample_size=self.__sample_size,
                    encoding=self.__csv_reader_encoding,
                ),
                delimiters="".join([",", "\t", ";", " ", ":"]),
            )
            df = pd.read_csv(filepath_or_buffer=filepath_or_buffer, dialect=dialect())
        else:
            df = pd.read_csv(filepath_or_buffer=filepath_or_buffer)

        if fixed_schema is None:
            fixed_schema = self.infer_schema(df)

        return self.fix_schema(df=df, fixed_schema=fixed_schema)[0], fixed_schema
