import re
from typing import BinaryIO, Dict, Optional, TextIO, Union

from pandas import DataFrame

from .schema import ShmessySchema


def _get_sampled_df(df: DataFrame, sample_size: int, random_sample: bool) -> DataFrame:
    number_of_rows: int = len(df)
    if number_of_rows < sample_size:
        sample_size = number_of_rows
    if random_sample:
        return df.sample(sample_size)
    return df.head(sample_size)


def _fix_column_names(df: DataFrame) -> Dict[str, str]:
    fixed_column_names = {}
    for column in df.columns:
        fixed_column_names[column] = re.sub("[^0-9a-zA-Z]+", "_", str(column))
    return fixed_column_names


def _fix_column_names_in_df(input_df: DataFrame, mapping: Dict[str, str]) -> DataFrame:
    return input_df.rename(columns=mapping)


def _fix_column_names_in_shmessy_schema(
    input_schema: ShmessySchema, mapping: Dict[str, str]
) -> ShmessySchema:
    for column in input_schema.columns:
        if mapping[column.field_name]:
            column.field_name = mapping[column.field_name]
    return input_schema


def _get_sample_from_csv(
    filepath_or_buffer: Union[str, TextIO, BinaryIO],
    sample_size: int,
    encoding: Optional[str] = "UTF-8",
) -> str:
    if isinstance(filepath_or_buffer, str):
        with open(file=filepath_or_buffer, mode="rt", encoding=encoding) as input_file:
            return "".join(input_file.readlines(sample_size))

    # sample = "".join(filepath_or_buffer.readlines(sample_size))
    # There is an issue with readlines(x) that reads the whole data instead of X first rows

    sample = ""
    for idx, line in enumerate(filepath_or_buffer):
        if idx > sample_size:
            break
        if not isinstance(line, str):
            line = line.decode(encoding)  # noqa
        sample += line

    filepath_or_buffer.seek(0)
    return sample
