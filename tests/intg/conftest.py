import pandas as pd
from hypothesis import strategies as st
from hypothesis.extra.pandas import data_frames, columns, range_indexes


@st.composite
def df_st(draw) -> st.SearchStrategy[pd.DataFrame]:
    col_names = draw(st.sets(st.text(min_size=1, max_size=10), min_size=2, max_size=5))
    dfs_st = data_frames(
        columns=columns(
            list(col_names),
            dtype=draw(st.sampled_from([
                # int, todo fix shmessy for int type. fails by exception
                # float, todo fix shmessy for float type. fails by exception for nan and inf values
                bool,
                str,
                # object, todo define object strategy for hypothesis

            ])),
        ),
        index=range_indexes(min_size=2, max_size=5, ),

    )
    df = draw(dfs_st)
    return df


@st.composite
def df_bool_st(draw) -> st.SearchStrategy[pd.DataFrame]:
    col_names = ['test_column']
    df = draw(data_frames(
        columns=columns(
            list(col_names),
            dtype=draw(st.sampled_from([
                bool,
            ])),
        ),
        rows=st.tuples(
            *[st.booleans() for _ in col_names]
        ),
        index=range_indexes(min_size=2, max_size=5, ),

    )
    )
    draw_type = draw(st.sampled_from([
        int,
        str,
        object,
    ]))
    df = df.astype(draw_type)
    return df
