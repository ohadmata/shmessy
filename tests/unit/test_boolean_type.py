import pandas as pd
from parametrization import Parametrization

from shmessy import Shmessy
import numpy as np
import pytest


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Base case - 1 / 0",
    df_data={
        "test_column": [1, 0, 1, 1, 0, 1, 1, 0, 1, 0]
    },
    expected_result=[True, False, True, True, False, True, True, False, True, False],
    expected_shmessy_type="Boolean",
    expected_numpy_type=np.dtype("bool")
)
@Parametrization.case(
    name="Base case - 1 / 0",
    df_data={
        "test_column": ["1", "0", "1", "1", "0", "1", "1", "0", "1", "0"]
    },
    expected_result=[True, False, True, True, False, True, True, False, True, False],
    expected_shmessy_type="Boolean",
    expected_numpy_type=np.dtype("bool")
)
@Parametrization.case(
    name="Base case - Yes / No",
    df_data={
        "test_column": ["yes", "no", "yes", "yes", "no"]
    },
    expected_result=[True, False, True, True, False],
    expected_shmessy_type="Boolean",
    expected_numpy_type=np.dtype("bool")
)
@Parametrization.case(
    name="1 / 0 with bad value",
    df_data={
        "test_column": [1, 0, 1, 1, 4, 1, 1, 0, 1, 0]
    },
    expected_result=[1, 0, 1, 1, 4, 1, 1, 0, 1, 0],
    expected_shmessy_type="Integer",
    expected_numpy_type=np.dtype("int64")
)
@Parametrization.case(
    name="1 / 0 with bad string value",
    df_data={
        "test_column": [1, 0, 1, 1, "hello", 1, 1, 0, 1, 0]
    },
    expected_result=["1", "0", "1", "1", "hello", "1", "1", "0", "1", "0"],
    expected_shmessy_type="String",
    expected_numpy_type=np.dtype("object")
)
@Parametrization.case(
    name="Only 1 should be identify as integer",
    df_data={
        "test_column": [1, 1, 1, 1, 1, 1, 1]
    },
    expected_result=[1, 1, 1, 1, 1, 1, 1],
    expected_shmessy_type="Integer",
    expected_numpy_type=np.dtype("int64")
)
@Parametrization.case(
    name="Only no should be identify as String",
    df_data={
        "test_column": ["no", "no", "no", "no", "no"]
    },
    expected_result=["no", "no", "no", "no", "no"],
    expected_shmessy_type="String",
    expected_numpy_type=np.dtype("object")
)
@Parametrization.case(
    name="Only no with single yes should be identify as bool",
    df_data={
        "test_column": ["no", "no", "no", "no", "no", "yes"]
    },
    expected_result=[False, False, False, False, False, True],
    expected_shmessy_type="Boolean",
    expected_numpy_type=np.dtype("bool")
)
def test_boolean_match_at_least_once_for_each_value(df_data, expected_shmessy_type, expected_numpy_type, expected_result):
    shmessy = Shmessy()
    df = pd.DataFrame(df_data)
    fixed_df = shmessy.fix_schema(df)
    result = shmessy.get_inferred_schema()

    assert result.columns[0].inferred_type == expected_shmessy_type
    assert fixed_df["test_column"].dtype.type == expected_numpy_type.type
    assert [x for x in df["test_column"]] == [x for x in expected_result]


def test_read_bool_from_csv_only_true_values(files_folder):
    df = Shmessy().read_csv(files_folder.as_posix() + "/data_6.csv")
    result = Shmessy().infer_schema(df=df)
    assert result.columns[1].inferred_type == "Boolean"


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Cannot cast bad value to boolean",
    df_data={
        "test_column": ["no", "yes", "no", "no", "bad_value", "yes"]
    },
    expected_result=[False, True, False, False, False, True],
    expected_shmessy_type="Boolean",
    expected_numpy_type=np.dtype("bool")
)
def test_boolean_fallback_to_null_turn_off(df_data, expected_shmessy_type, expected_numpy_type, expected_result):
    shmessy = Shmessy(use_random_sample=False, sample_size=2)
    df = pd.DataFrame(df_data)

    with pytest.raises(Exception) as e:
        shmessy.fix_schema(df)
    assert f"Couldn\\\'t cast value \"bad_value\" to type Boolean" in str(e)


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Cannot cast bad value to boolean - fallback to null",
    df_data={
        "test_column": ["no", "yes", "no", "no", "bad_value", "yes"]
    },
    expected_result=[False, True, False, False, np.nan, True],
    expected_shmessy_type="Boolean",
    expected_numpy_type=np.dtype("O")
)
def test_boolean_fallback_to_null_turn_on(df_data, expected_shmessy_type, expected_numpy_type, expected_result):
    shmessy = Shmessy(use_random_sample=False, sample_size=2, fallback_to_null=True)
    df = pd.DataFrame(df_data)
    fixed_df = shmessy.fix_schema(df)
    result = shmessy.get_inferred_schema()

    assert result.columns[0].inferred_type == expected_shmessy_type
    assert fixed_df["test_column"].dtype.type == expected_numpy_type.type
    assert [x for x in df["test_column"]] == [x for x in expected_result]
