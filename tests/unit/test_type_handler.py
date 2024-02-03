import hypothesis as hp
import pandas as pd
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


def test_handler_type_dict():
    types_handler = TypesHandler()
    types_as_dict = types_handler._TypesHandler__types_as_dict
    values = types_as_dict.values()
    values_base_types = {v.__class__.__bases__[0] for v in values}
    assert {BaseType} == values_base_types


@hp.given(
    pd_series=series_st(),
    field_name=st.text(min_size=1, max_size=10),
    fallback_to_string=st.booleans(),
)
def test_type_handler(pd_series, field_name, fallback_to_string):
    type_handler = TypesHandler()
    copied_series = pd_series.copy()
    field = type_handler.infer_field(field_name=field_name, data=pd_series.values)
    fixed_series = type_handler.fix_field(
        column=pd_series,
        inferred_field=field,
        fallback_to_string=fallback_to_string,
    ).copy()
    assert copied_series.equals(pd_series)
    new_fixed_series = type_handler.fix_field(
        column=fixed_series,
        inferred_field=field,
        fallback_to_string=fallback_to_string,
    )
    assert new_fixed_series.equals(fixed_series)
    field_from_object = type_handler.infer_field(field_name=field_name, data=pd_series.astype(object).values)
    fixed_from_object = type_handler.fix_field(column=pd_series.astype(object), inferred_field=field_from_object)
    assert fixed_from_object.equals(fixed_series)
    # todo shmessy dealing with object type
