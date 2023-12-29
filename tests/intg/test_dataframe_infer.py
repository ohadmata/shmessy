import pandas as pd

from shmessy import Shmessy
from numpy import dtypes


def test_data_1_types_infer():
    df = pd.read_csv("tests/data/data_1.csv")
    fixed_df = Shmessy().fix_schema(df)

    assert isinstance(df["created_at"].dtype, dtypes.DateTime64DType)
    assert isinstance(df["modified_at"].dtype, dtypes.DateTime64DType)
    assert isinstance(df["deleted_at"].dtype, dtypes.DateTime64DType)
    assert isinstance(df["celebrated_at"].dtype, dtypes.DateTime64DType)
    assert isinstance(df["joined_at"].dtype, dtypes.DateTime64DType)
    assert isinstance(df["laughed_at"].dtype, dtypes.DateTime64DType)
    assert isinstance(df["loled_at"].dtype, dtypes.DateTime64DType)
    assert isinstance(df["fooled_at"].dtype, dtypes.DateTime64DType)
    assert isinstance(df["emerged_at"].dtype, dtypes.DateTime64DType)
    assert isinstance(df["processed_at"].dtype, dtypes.DateTime64DType)
    assert isinstance(df["isolated_at"].dtype, dtypes.DateTime64DType)
    assert isinstance(df["scheduled_at"].dtype, dtypes.DateTime64DType)
    assert isinstance(df["unixed_at"].dtype, dtypes.DateTime64DType)
