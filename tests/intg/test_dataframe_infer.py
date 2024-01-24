import pandas as pd
from numpy import dtypes
from shmessy import Shmessy


def test_data_1_types_infer(files_folder):
    df = pd.read_csv(files_folder.as_posix() + "/data_1.csv")
    df = Shmessy().fix_schema(df)

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
