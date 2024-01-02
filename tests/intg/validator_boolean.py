import pandas as pd
from parametrization import Parametrization

from shmessy import Shmessy
from numpy.dtypes import StrDType, BoolDType


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Do nothing - Bad value",
    df_data={
        "name": ["true", "false", "true", "true", "bad value"],
    },
    expected_result=["true", "false", "true", "true", "bad value"],
    expected_dtype=StrDType
)
@Parametrization.case(
    name="Recognize true/false",
    df_data={
        "name": ["true", "false", "true", "true"],
    },
    expected_result=[True, False, True, True],
    expected_dtype=BoolDType()
)
@Parametrization.case(
    name="Recognize True/False",
    df_data={
        "name": ["True", "True", "False", "False"],
    },
    expected_result=[True, True, False, False],
    expected_dtype=BoolDType()
)
@Parametrization.case(
    name="Recognize yes/no",
    df_data={
        "name": ["yes", "yes", "no", "no"],
    },
    expected_result=[True, True, False, False],
    expected_dtype=BoolDType()
)
@Parametrization.case(
    name="Recognize Y/N",
    df_data={
        "name": ["Y", "Y", "N", "N"],
    },
    expected_result=[True, True, False, False],
    expected_dtype=BoolDType()
)
@Parametrization.case(
    name="Recognize T/F",
    df_data={
        "name": ["F", "T", "T", "F"],
    },
    expected_result=[False, True, True, False],
    expected_dtype=BoolDType()
)
@Parametrization.case(
    name="Recognize 1/0",
    df_data={
        "name": [1, 0, 0, 1, 0],
    },
    expected_result=[True, False, False, True, False],
    expected_dtype=BoolDType()
)
def test_validator_boolean(df_data, expected_result, expected_dtype):
    df = pd.DataFrame(df_data)
    df = Shmessy().fix_schema(df=df)

    assert [x for x in df["name"]] == [x for x in expected_result]
    assert df["name"].dtype == expected_dtype
