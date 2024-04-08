import numpy as np
import pandas as pd
from parametrization import Parametrization

from shmessy import Shmessy


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Base case",
    df_data={
        "test_column": ["ohad@gmail.com", "hello@microsoft.com", "world@nana.co.il"]
    },
    expected_shmessy_type="Email",
    expected_numpy_type=np.dtype('O')
)
def test_email_type(df_data, expected_shmessy_type, expected_numpy_type):
    shmessy = Shmessy()
    df = pd.DataFrame(df_data)
    inferred_schema = shmessy.infer_schema(df=df)
    fixed_df = shmessy.fix_schema(df)

    assert inferred_schema.columns[0].inferred_type == expected_shmessy_type
    assert fixed_df["test_column"].dtype.type == expected_numpy_type.type


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Base case",
    df_data={
        "test_column": ["ohad@gmail.com", "hello@microsoft.com", "world@nana.co.il"]
    },
    expected_shmessy_type="String",
    expected_numpy_type=np.dtype('O')
)
def test_email_type_turn_off_email_types(df_data, expected_shmessy_type, expected_numpy_type):
    shmessy = Shmessy(types_to_ignore=["email"])
    df = pd.DataFrame(df_data)
    inferred_schema = shmessy.infer_schema(df=df)
    fixed_df = shmessy.fix_schema(df)

    assert inferred_schema.columns[0].inferred_type == expected_shmessy_type
    assert fixed_df["test_column"].dtype.type == expected_numpy_type.type