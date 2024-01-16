import pandas as pd
from parametrization import Parametrization

from shmessy import Shmessy


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Base case - 1 / 0",
    df_data={
        "test_column": [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]
    },
    expected_result="Boolean"
)
@Parametrization.case(
    name="Base case - Yes / No",
    df_data={
        "test_column": ["yes", "no", "yes", "yes", "no"]
    },
    expected_result="Boolean"
)
@Parametrization.case(
    name="1 / 0 with bad value",
    df_data={
        "test_column": [1, 0, 1, 1, 4, 1, 1, 0, 1, 0]
    },
    expected_result="Integer"
)
@Parametrization.case(
    name="1 / 0 with bad string value",
    df_data={
        "test_column": [1, 0, 1, 1, "hello", 1, 1, 0, 1, 0]
    },
    expected_result="String"
)
@Parametrization.case(
    name="Only 1 should be identify as integer",
    df_data={
        "test_column": [1, 1, 1, 1, 1, 1, 1]
    },
    expected_result="Integer"
)
@Parametrization.case(
    name="Only no should be identify as String",
    df_data={
        "test_column": ["no", "no", "no", "no", "no"]
    },
    expected_result="String"
)
@Parametrization.case(
    name="Only no with single yes should be identify as bool",
    df_data={
        "test_column": ["no", "no", "no", "no", "no", "yes"]
    },
    expected_result="Boolean"
)
def test_boolean_match_at_least_once_for_each_value(df_data, expected_result):
    df = pd.DataFrame(df_data)
    result = Shmessy().infer_schema(df=df)
    assert result.columns[0].inferred_type == expected_result


def test_read_bool_from_csv_only_true_values():
    df = Shmessy().read_csv("tests/data/data_6.csv")
    result = Shmessy().infer_schema(df=df)
    assert result.columns[1].inferred_type == "Boolean"


