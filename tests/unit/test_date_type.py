from datetime import datetime

import numpy as np
import pandas as pd
from parametrization import Parametrization
from shmessy.types.date import DateType

from shmessy import Shmessy


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Base case (%m/%d/%Y)",
    df_data={
        "test_column": ["12/21/2022", "03/11/2022", "08/24/2022"]
    },
    expected_pattern="%m/%d/%Y",
    expected_result=[
        datetime(2022, 12, 21),
        datetime(2022, 3, 11),
        datetime(2022, 8, 24)
    ],
    expected_shmessy_type="Date",
    expected_numpy_type=np.dtype("datetime64")
)
@Parametrization.case(
    name="Base case (%d-%m-%Y)",
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
    name="Base case (%Y-%m-%d)",
    df_data={
        "test_column": ["2020-04-11", "2021-05-23", "2022-11-22"]
    },
    expected_pattern="%Y-%m-%d",
    expected_result=[
        datetime(2020, 4, 11),
        datetime(2021, 5, 23),
        datetime(2022, 11, 22)
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
@Parametrization.case(
    name="Date without leading zeros in the day part and month part (%m/%d/%Y)",
    df_data={
        "test_column": ["7/25/2022", "8/24/2023", "9/23/2024", "10/22/2025", "11/21/2026"]
    },
    expected_pattern="%m/%d/%Y",
    expected_result=[
        datetime(2022, 7, 25),
        datetime(2023, 8, 24),
        datetime(2024, 9, 23),
        datetime(2025, 10, 22),
        datetime(2026, 11, 21)
    ],
    expected_shmessy_type="Date",
    expected_numpy_type=np.dtype("datetime64")
)
@Parametrization.case(
    name="Date without without day (%Y-%m)",
    df_data={
        "test_column": ["2022-02", "2019-01", "2011-02", "2020-12", "2004-06"]
    },
    expected_pattern="%Y-%m",
    expected_result=[
        datetime(2022, 2, 1),
        datetime(2019, 1, 1),
        datetime(2011, 2, 1),
        datetime(2020, 12, 1),
        datetime(2004, 6, 1)
    ],
    expected_shmessy_type="Date",
    expected_numpy_type=np.dtype("datetime64")
)
@Parametrization.case(
    name="Date dot delimiter without leading zero (%d.%m.%Y)",
    df_data={
        "test_column": ["14.11.2022", "11.11.2022", "29.6.2022", "13.9.2022", "26.7.2022"]
    },
    expected_pattern="%d.%m.%Y",
    expected_result=[
        datetime(2022, 11, 14),
        datetime(2022, 11, 11),
        datetime(2022, 6, 29),
        datetime(2022, 9, 13),
        datetime(2022, 7, 26)
    ],
    expected_shmessy_type="Date",
    expected_numpy_type=np.dtype("datetime64")
)
@Parametrization.case(
    name="New date format (%d %b %Y)",
    df_data={
        "test_column": ["13 Jan 2023", "1 Jan 2024", "17 Jan 2025", "16 Mar 2020"]
    },
    expected_pattern="%d %b %Y",
    expected_result=[
        datetime(2023, 1, 13),
        datetime(2024, 1, 1),
        datetime(2025, 1, 17),
        datetime(2020, 3, 16)
    ],
    expected_shmessy_type="Date",
    expected_numpy_type=np.dtype("datetime64")
)
@Parametrization.case(
    name="New date format (%m.%d.%y)",
    df_data={
        "test_column": ["11.24.22", "01.22.21", "12.20.11", "02.12.23"]
    },
    expected_pattern="%m.%d.%y",
    expected_result=[
        datetime(2022, 11, 24),
        datetime(2021, 1, 22),
        datetime(2011, 12, 20),
        datetime(2023, 2, 12)
    ],
    expected_shmessy_type="Date",
    expected_numpy_type=np.dtype("datetime64")
)
@Parametrization.case(
    name="New date format (%d.%m.%y)",
    df_data={
        "test_column": ["24.11.22", "22.01.21", "20.12.11", "12.02.23"]
    },
    expected_pattern="%d.%m.%y",
    expected_result=[
        datetime(2022, 11, 24),
        datetime(2021, 1, 22),
        datetime(2011, 12, 20),
        datetime(2023, 2, 12)
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


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Cannot cast bad value to date - fallback to null",
    df_data={
        "test_column": ["10-12-1991", "23-11-2006", "27-01-2002", "bad_value", "09-05-2022"]
    },
    expected_result=[
        datetime(1991, 12, 10),
        datetime(2006, 11, 23),
        datetime(2002, 1, 27),
        pd.NaT,
        datetime(2022, 5, 9)
    ],
    expected_shmessy_type="Date",
    expected_numpy_type=np.dtype("datetime64")
)
def test_date_fallback_to_null_turn_on(df_data, expected_shmessy_type, expected_numpy_type, expected_result):
    shmessy = Shmessy(use_random_sample=False, sample_size=2, fallback_to_null=True)
    df = pd.DataFrame(df_data)
    fixed_df = shmessy.fix_schema(df)
    result = shmessy.get_inferred_schema()

    assert result.columns[0].inferred_type == expected_shmessy_type
    assert fixed_df["test_column"].dtype.type == expected_numpy_type.type
    assert [x for x in df["test_column"]] == [x for x in expected_result]


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="test %m %d %y",
    date=["%m", "%d", "%Y"],
    delimiters={"/", ".", "-", " "},
)
@Parametrization.case(
    name="test %Y %m",
    date=["%Y", "%m"],
    delimiters={"/", ".", "-", " "},
)
def test_dynamic_patterns(date: list[str], delimiters: set[str]):
    date_type = DateType()
    patterns = date_type.get_patterns()

    for delimiter in delimiters:
        assert delimiter.join(date) in patterns


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="test %B %d, %Y",
    date="%B %d, %Y",
)
def test_static_patterns(date: str):
    date_type = DateType()
    assert date in date_type.get_patterns()


def test_get_patterns_with_date_only():
    date_only_patterns: list[str] = [
        "%Y-%m", "%Y %m", "%Y/%b", "%b %y", "%b.%Y", "%b-%y", "%m/%y"
    ]
    date_type = DateType()
    result_all_patterns = date_type.get_patterns()
    result_date_only_patterns = date_type.get_patterns(include_date_only_patterns=False)

    for p in date_only_patterns:
        assert p in result_all_patterns
        assert p not in result_date_only_patterns


def test_include_date_static_patterns():
    input_static_patterns: list[str] = ["%B %d, %Y"]
    date_type = DateType()
    result_all_patterns = date_type.get_patterns()
    result_without_static_patterns = date_type.get_patterns(include_static_date_patterns=False)

    for p in input_static_patterns:
        assert p in result_all_patterns
        assert p not in result_without_static_patterns
