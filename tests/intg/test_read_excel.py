import numpy as np
import pandas

from shmessy import Shmessy


def test_read_excel_with_numeric_headers(files_folder):
    df = pandas.read_excel(files_folder.as_posix() + "/data_9.xlsx")
    df = Shmessy().fix_schema(df)

    assert df[0].dtype == np.dtype("int64")
    assert df["First Name"].dtype == np.dtype("O")
    assert df["Date"].dtype == np.dtype("datetime64[ns]")
    assert df["Id"].dtype == np.dtype("int64")