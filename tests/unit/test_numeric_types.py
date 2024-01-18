import numpy as np
import pandas as pd
from parametrization import Parametrization

from shmessy import Shmessy


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Base case",
    df_data={
        "test_column": [15, 1230, 1, 154, 330, 1, 53451, 344, 166, 123]
    },
    expected_shmessy_type="Integer",
    expected_numpy_type=np.dtype('int64')
)
@Parametrization.case(
    name="Input as strings",
    df_data={
        "test_column": ["15", "1230", "1"]
    },
    expected_shmessy_type="Integer",
    expected_numpy_type=np.dtype('int64')
)
@Parametrization.case(
    name="Input as strings with commas",
    df_data={
        "test_column": ["15,322", "1,230", "1"]
    },
    expected_shmessy_type="Integer",
    expected_numpy_type=np.dtype('int64')
)
@Parametrization.case(
    name="Input as strings with comma and decimal point",
    df_data={
        "test_column": ["15,322.1", "1,230", "1"]
    },
    expected_shmessy_type="Float",
    expected_numpy_type=np.dtype('float64')
)
@Parametrization.case(
    name="Base case - Input as strings with comma and decimal point",
    df_data={
        "test_column": ["15322.1", "123.10", "1"]
    },
    expected_shmessy_type="Float",
    expected_numpy_type=np.dtype('float64')
)
def test_numeric_type(df_data, expected_shmessy_type, expected_numpy_type):
    shmessy = Shmessy()
    df = pd.DataFrame(df_data)
    inferred_schema = shmessy.infer_schema(df=df)
    fixed_df = shmessy.fix_schema(df)

    assert inferred_schema.columns[0].inferred_type == expected_shmessy_type
    assert fixed_df["test_column"].dtype.type == expected_numpy_type.type


