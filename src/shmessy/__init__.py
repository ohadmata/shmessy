import logging
import time
from typing import Optional

from pandas import DataFrame

from .schema import ShmessySchema
from .validators_handler import ValidatorsHandler

logger = logging.getLogger(__name__)


class Shmessy:
    def __init__(self, sample_size: Optional[int] = 1000) -> None:
        self.__validators_handler = ValidatorsHandler()
        self.__sample_size = sample_size

    def _get_sampled_df(self, df: DataFrame) -> DataFrame:
        number_of_rows: int = len(df)
        if number_of_rows < self.__sample_size:
            self.__sample_size = number_of_rows
        return df.sample(n=self.__sample_size)

    def infer_schema(self, df: DataFrame) -> ShmessySchema:
        start_time = time.time()
        df = self._get_sampled_df(df)
        columns = [
            self.__validators_handler.infer_field(
                field_name=column, data=df[column].values
            )
            for column in df
        ]
        infer_duration_ms = int((time.time() - start_time) * 1000)

        return ShmessySchema(columns=columns, infer_duration_ms=infer_duration_ms)

    def fix_schema(self, df: DataFrame) -> DataFrame:
        for column in df:
            df[column] = self.__validators_handler.fix_field(
                column=df[column], sample_size=self.__sample_size
            )

        return df
