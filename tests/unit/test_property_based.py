import string

import hypothesis as hp
import pandas as pd
from hypothesis import strategies as st
from hypothesis.extra.pandas import data_frames, columns, range_indexes, series

from shmessy import Shmessy

from shmessy.types.boolean import BooleanType
from shmessy.types.date import DateType
from shmessy.types.datetime_ import DatetimeType


@st.composite
def dtypes_st(draw) -> pd.Series:
    dtypes = st.sampled_from([
        int,
        float,
        bool,
        str,
        "datetime64[ns]",
        # "timedelta64[ns]", todo define shmessy behavior for timedelta

    ])
    return draw(dtypes)


@st.composite
def df_st(draw) -> pd.DataFrame:
    col_names = draw(st.sets(st.text(min_size=1, max_size=10), min_size=2, max_size=5))
    dfs_st = data_frames(
        columns=columns(
            list(col_names),
            dtype=draw(dtypes_st()),
        ),
        index=range_indexes(min_size=2, max_size=5, ),

    )
    df = draw(dfs_st)
    return df


@st.composite
def shmessy_bool_st(draw) -> pd.Series:
    pattern = draw(st.sampled_from(BooleanType().patterns))
    return draw(
        series(
            elements=st.sampled_from(pattern),
            dtype=str,
            index=range_indexes(min_size=2, max_size=10)

        )
    )


@st.composite
def dt_st(draw, patterns) -> pd.Series:
    pattern = draw(st.sampled_from(patterns))
    hp.assume('Y' in pattern)  # format y instead of Y probably have pandas bug with .dt.strftime(pattern)
    pd_series = draw(
        series(
            dtype="datetime64[ns]",
            index=range_indexes(min_size=2, max_size=10),

        )
    )
    return pd_series.dt.strftime(pattern)


@hp.given(
    df=df_st(),
    fix_column_names=st.booleans(),
    fallback_to_string=st.booleans(),
)
def test_fix_schema_cols_hp(df, fix_column_names, fallback_to_string):
    df_fixed = Shmessy().fix_schema(
        df=df,
        fix_column_names=fix_column_names,
        fallback_to_string=fallback_to_string,
    )
    assert set(list(df_fixed)) == set(list(df)) if not fix_column_names else True
    allowed_chars = set(string.ascii_lowercase).union(set(string.ascii_uppercase)).union(set(string.digits))
    allowed_chars.add("_")
    all_cols_name_chars = {char for col in list(df_fixed) for char in col}
    assert all_cols_name_chars.issubset(allowed_chars) if fix_column_names else True


@hp.given(pd_series=shmessy_bool_st(), )
@hp.settings(suppress_health_check=[hp.HealthCheck.function_scoped_fixture], )
def test_schema_infer_booleans_hp(pd_series, type_handler):
    field = type_handler.infer_field(field_name="field_name", data=pd_series)
    hp.assume(len(pd_series.unique()) > 1)
    assert field.inferred_type == "Boolean"


@hp.given(pd_series=dt_st(patterns=DateType().patterns), )
@hp.settings(suppress_health_check=[hp.HealthCheck.function_scoped_fixture], )
def test_schema_infer_date_hp(pd_series, type_handler):
    field = type_handler.infer_field(field_name="field_name", data=pd_series)
    assert field.inferred_type == "Date"


@hp.given(pd_series=dt_st(patterns=DatetimeType().patterns), )
@hp.settings(suppress_health_check=[hp.HealthCheck.function_scoped_fixture], )
def test_schema_infer_datetime_hp(pd_series, type_handler):
    field = type_handler.infer_field(field_name="field_name", data=pd_series)
    assert field.inferred_type == "Datetime"
