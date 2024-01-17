import pandas as pd
from numpy.core._multiarray_umath import dtype
from parametrization import Parametrization

from shmessy import Shmessy


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Base case",
    df_data={
        "test_column": [15, 1230, 1, 154, 330, 1, 53451, 344, 166, 123]
    },
    expected_shmessy_type="Integer",
    expected_numpy_type=dtype('int64')
)
@Parametrization.case(
    name="Input as strings",
    df_data={
        "test_column": ["15", "1230", "1"]
    },
    expected_shmessy_type="Integer",
    expected_numpy_type=dtype('int64')
)
@Parametrization.case(
    name="Input as strings with commas",
    df_data={
        "test_column": ["15,322", "1,230", "1"]
    },
    expected_shmessy_type="Integer",
    expected_numpy_type=dtype('int64')
)
@Parametrization.case(
    name="Input as strings with comma and decimal point",
    df_data={
        "test_column": ["15,322.1", "1,230", "1"]
    },
    expected_shmessy_type="Float",
    expected_numpy_type=dtype('float64')
)
@Parametrization.case(
    name="Base case - Input as strings with comma and decimal point",
    df_data={
        "test_column": ["15322.1", "123.10", "1"]
    },
    expected_shmessy_type="Float",
    expected_numpy_type=dtype('float64')
)
def test_numeric_type(df_data, expected_shmessy_type, expected_numpy_type):
    shmessy = Shmessy()
    df = pd.DataFrame(df_data)
    result = shmessy.infer_schema(df=df)
    assert result.columns[0].inferred_type == expected_shmessy_type

    fixed_df = shmessy.fix_schema(df)
    assert fixed_df["test_column"].dtype == expected_numpy_type



