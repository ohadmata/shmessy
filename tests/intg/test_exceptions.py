import pytest
from shmessy import Shmessy
import pandas as pd


def test_too_many_columns_exception():
    df_data = {
        "col_1": ["data_1"],
        "col_2": ["data_1"],
        "col_3": ["data_1"],
        "col_4": ["data_1"],
    }

    df = pd.DataFrame(df_data)
    shmessy = Shmessy(max_columns_num=2)
    with pytest.raises(Exception) as e:
        shmessy.fix_schema(df)
    assert "The input table contains 4 columns. The maximum number of columns we support is 2" in str(e)