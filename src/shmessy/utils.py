import codecs
import re
from io import TextIOWrapper
from typing import BinaryIO, Optional, TextIO, Union

from pandas import DataFrame


def _get_sampled_df(df: DataFrame, sample_size: int) -> DataFrame:
    number_of_rows: int = len(df)
    if number_of_rows < sample_size:
        sample_size = number_of_rows
    return df.sample(n=sample_size)


def _fix_column_names(df: DataFrame) -> DataFrame:
    fixed_column_names = {}
    for column in df.columns:
        fixed_column_names[column] = re.sub("[^0-9a-zA-Z]+", "_", column)
    return df.rename(columns=fixed_column_names)


def _get_sample_from_csv(
    filepath_or_buffer: Union[str, TextIO, BinaryIO],
    sample_size: int,
    encoding: Optional[str] = "UTF-8",
) -> str:
    if isinstance(filepath_or_buffer, str):
        with open(file=filepath_or_buffer, mode="rt", encoding=encoding) as input_file:
            return "".join(input_file.readlines(sample_size))

    elif isinstance(filepath_or_buffer, (TextIO, TextIOWrapper)):
        text_stream = filepath_or_buffer

    else:
        text_stream = codecs.getreader(encoding)(filepath_or_buffer)

    sample = "".join(text_stream.readlines(sample_size))
    filepath_or_buffer.seek(0)
    return sample
