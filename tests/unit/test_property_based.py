import string

import hypothesis as hp
import pandas as pd
from hypothesis import strategies as st
from hypothesis.extra.pandas import data_frames, columns, range_indexes

from shmessy import Shmessy


@st.composite
def df_st(draw) -> pd.DataFrame:
    col_names = draw(st.sets(st.text(min_size=1, max_size=10), min_size=2, max_size=5))
    dfs_st = data_frames(
        columns=columns(
            list(col_names),
            dtype=draw(st.sampled_from([
                int,
                float,
                bool,
                str,
                "datetime64[ns]",
                "timedelta64[ns]",
                "period[D]"

            ])),
        ),
        index=range_indexes(min_size=2, max_size=5, ),

    )
    df = draw(dfs_st)
    return df


@st.composite
def df_bool_st(draw) -> pd.DataFrame:
    dfs_st = data_frames(
        columns=columns(
            list(['col1', 'col2']),
            dtype=draw(st.sampled_from([
                bool,
            ])),
        ),
        index=range_indexes(min_size=2, max_size=5, ),

    )
    draw_type = draw(st.sampled_from([
        int,
        str,
        object,
    ]))
    df = draw(dfs_st)
    df = df.astype(draw_type)

    return df


@hp.given(df=df_st(), fix_column_names=st.booleans())
def test_fix_schema_cols_hp(df, fix_column_names):
    df_fixed = Shmessy().fix_schema(df=df, fix_column_names=fix_column_names)
    assert set(list(df_fixed)) == set(list(df)) if not fix_column_names else True
    allowed_chars = set(string.ascii_lowercase).union(set(string.ascii_uppercase)).union(set(string.digits))
    allowed_chars.add("_")
    all_cols_name_chars = {char for col in list(df_fixed) for char in col}
    assert all_cols_name_chars.issubset(allowed_chars) if fix_column_names else True


@hp.given(df_bool=df_bool_st(), )
def test_schema_infer_booleans_hp(df_bool, ):
    shmessy_scheme = Shmessy().infer_schema(df=df_bool.copy())
    for col in shmessy_scheme.columns:
        one_unique = len(df_bool[col.field_name].unique()) == 1
        assert col.inferred_type != "Boolean" if one_unique else col.inferred_type == "Boolean"
