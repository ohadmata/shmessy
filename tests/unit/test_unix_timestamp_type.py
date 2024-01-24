import numpy as np
import pandas as pd
from parametrization import Parametrization

from shmessy import Shmessy


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Only nan value should be recognized as float",
    df_data={
        "test_column": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan")]
    },
    expected_shmessy_type="Float",
    expected_numpy_type=np.dtype("float64")
)
@Parametrization.case(
    name="UnixTimestamp seconds",
    df_data={
        "test_column": [1706024027, 1706024052, 1706021052, 1704024052]
    },
    expected_shmessy_type="UnixTimestamp",
    expected_numpy_type=np.dtype("datetime64")
)
@Parametrization.case(
    name="UnixTimestamp milliseconds",
    df_data={
        "test_column": [1706024027000, 1706024052000, 1706021052000, 1704024052000]
    },
    expected_shmessy_type="UnixTimestamp",
    expected_numpy_type=np.dtype("datetime64")
)
def test_datetime_type(df_data, expected_shmessy_type, expected_numpy_type):
    shmessy = Shmessy()
    df = pd.DataFrame(df_data)
    fixed_df = shmessy.fix_schema(df)
    inferred_schema = shmessy.get_inferred_schema()

    assert inferred_schema.columns[0].inferred_type == expected_shmessy_type
    assert fixed_df["test_column"].dtype.type == expected_numpy_type.type
