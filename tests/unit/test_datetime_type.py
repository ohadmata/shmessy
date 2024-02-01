from datetime import datetime

import numpy as np
import pandas as pd
from parametrization import Parametrization

from shmessy import Shmessy


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Base case (%Y-%m-%d %H:%M:%S)",
    df_data={
        "test_column": ["2022-04-25 12:18:08", "2022-05-08 21:08:27", "2022-02-03 21:56:00"]
    },
    expected_pattern="%Y-%m-%d %H:%M:%S",
    expected_result=[
        datetime(2022, 4, 25, 12, 18, 8),
        datetime(2022, 5, 8, 21, 8, 27),
        datetime(2022, 2, 3, 21, 56, 0)
    ],
    expected_shmessy_type="Datetime",
    expected_numpy_type=np.dtype("datetime64")
)
def test_datetime_type(df_data, expected_shmessy_type, expected_numpy_type, expected_result, expected_pattern):
    shmessy = Shmessy()
    df = pd.DataFrame(df_data)
    fixed_df = shmessy.fix_schema(df)
    inferred_schema = shmessy.get_inferred_schema()

    assert inferred_schema.columns[0].inferred_pattern == expected_pattern
    assert inferred_schema.columns[0].inferred_type == expected_shmessy_type
    assert fixed_df["test_column"].dtype.type == expected_numpy_type.type
    assert [x for x in df["test_column"]] == [x for x in expected_result]


def test_source_column_already_defines_as_date():
    df = pd.DataFrame(pd.date_range(start='2020-11-03', end='2021-10-01'), columns=['test_column'])
    fixed_df = Shmessy().fix_schema(df)
    assert fixed_df["test_column"].dtype.type == np.dtype("datetime64")
