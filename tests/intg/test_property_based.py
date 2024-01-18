import string

import hypothesis as hp
import hypothesis.strategies as st

from shmessy import Shmessy
from tests.intg.conftest import df_st, df_bool_st

max_examples = 20


@hp.given(df=df_st(), fix_column_names=st.booleans())
@hp.settings(max_examples=max_examples)
def test_fix_schema_cols_hp(df, fix_column_names):
    df_fixed = Shmessy().fix_schema(df=df, fix_column_names=fix_column_names)
    assert set(list(df_fixed)) == set(list(df)) if not fix_column_names else True
    hp.assume(fix_column_names)
    allowed_chars = set(string.ascii_lowercase).union(set(string.ascii_uppercase)).union(set(string.digits))
    allowed_chars.add("_")
    all_cols_name_chars = {char for col in list(df_fixed) for char in col}
    assert all_cols_name_chars.issubset(allowed_chars)


@hp.given(df_bool=df_bool_st(), )
@hp.settings(max_examples=max_examples)
def test_schema_infer_booleans_hp(df_bool, ):
    shmessy_scheme = Shmessy().infer_schema(df=df_bool.copy())
    for col in shmessy_scheme.columns:
        one_unique = len(df_bool[col.field_name].unique()) == 1
        assert col.inferred_type != "Boolean" if one_unique else col.inferred_type == "Boolean"
