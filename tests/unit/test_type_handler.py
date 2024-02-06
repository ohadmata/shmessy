import hypothesis as hp
import pandas as pd
import pytest
from hypothesis import strategies as st
from hypothesis.extra.pandas import range_indexes, series

from shmessy import TypesHandler
from shmessy.types.base import BaseType
from tests.unit.test_property_based import dtypes_st


@st.composite
def series_st(draw) -> pd.Series:
    s = series(
        dtype=draw(dtypes_st()),
        index=range_indexes(min_size=2, max_size=5, ),
    )
    return draw(s)


@pytest.fixture(scope="module")
def types_handler():
    return TypesHandler()


def test_handler_type_dict(types_handler):
    types_as_dict = types_handler._TypesHandler__types_as_dict
    values = types_as_dict.values()
    values_base_types = {v.__class__.__bases__[0] for v in values}
    assert {BaseType} == values_base_types


@hp.given(
    pd_series=series_st(),
    field_name=st.text(min_size=1, max_size=10),
    fallback_to_string=st.booleans(),
)
def test_th_preserve_original_series(
        pd_series,
        field_name,
        fallback_to_string,
        types_handler,

):
    copied_series = pd_series.copy()
    field = types_handler.infer_field(field_name=field_name, data=pd_series.values)
    _ = types_handler.fix_field(
        column=pd_series,
        inferred_field=field,
        fallback_to_string=fallback_to_string,
    )
    assert copied_series.equals(pd_series)


@hp.given(
    pd_series=series_st(),
    field_name=st.text(min_size=1, max_size=10),
    fallback_to_string=st.booleans(),
)
def test_th_double_fixing_yield_same_results(
        pd_series,
        field_name,
        fallback_to_string,
        types_handler,

):
    fixed_series = types_handler.fix_field(
        column=pd_series,
        inferred_field=types_handler.infer_field(field_name=field_name, data=pd_series.values),
        fallback_to_string=fallback_to_string,
    )
    new_fixed_series = types_handler.fix_field(
        column=fixed_series,
        inferred_field=types_handler.infer_field(field_name=field_name, data=fixed_series.values),
        fallback_to_string=fallback_to_string,
    )
    assert new_fixed_series.equals(fixed_series)


@hp.given(
    pd_series=series_st(),
    field_name=st.text(min_size=1, max_size=10),
    object_type=st.sampled_from([
        str,  # fails with AssertionError: assert 'Datetime' == 'Date'
        object,  # fails with TypeError: int() argument must be a string, a bytes-like object or a real number
    ]),
)
@pytest.mark.xfail(reason="todo define shmessy consistency rules")
def test_th_field_infer_consistency(
        pd_series,
        field_name,
        object_type,
        types_handler,

):
    hp.assume(pd_series.dtype != bool)
    field = types_handler.infer_field(data=pd_series.values, field_name=field_name, )
    field_from_object = types_handler.infer_field(data=pd_series.astype(object_type).values, field_name=field_name, )
    assert field.inferred_type == field_from_object.inferred_type
