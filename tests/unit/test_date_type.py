from datetime import datetime

import numpy as np
import pandas as pd
from parametrization import Parametrization

from shmessy import Shmessy


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Base case",
    df_data={
        "test_column": ["23-11-2023", "21-04-2022", "11-08-2021"]
    },
    expected_pattern="%d-%m-%Y",
    expected_result=[
        datetime(2023, 11, 23),
        datetime(2022, 4, 21),
        datetime(2021, 8, 11)
    ],
    expected_shmessy_type="Date",
    expected_numpy_type=np.dtype("datetime64")
)
@Parametrization.case(
    name="Date without leading zeros in the day part",
    df_data={
        "test_column": ["1-11-2023", "9-04-2022", "11-12-2021", "2-01-2020", "23-04-2019"]
    },
    expected_pattern="%d-%m-%Y",
    expected_result=[
        datetime(2023, 11, 1),
        datetime(2022, 4, 9),
        datetime(2021, 12, 11),
        datetime(2020, 1, 2),
        datetime(2019, 4, 23)
    ],
    expected_shmessy_type="Date",
    expected_numpy_type=np.dtype("datetime64")
)
def test_date_type(df_data, expected_shmessy_type, expected_numpy_type, expected_result, expected_pattern):
    shmessy = Shmessy()
    df = pd.DataFrame(df_data)
    fixed_df = shmessy.fix_schema(df)
    inferred_schema = shmessy.get_inferred_schema()

    assert inferred_schema.columns[0].inferred_pattern == expected_pattern
    assert inferred_schema.columns[0].inferred_type == expected_shmessy_type
    assert fixed_df["test_column"].dtype.type == expected_numpy_type.type
    assert [x for x in df["test_column"]] == [x for x in expected_result]
