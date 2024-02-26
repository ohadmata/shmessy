import numpy as np

from shmessy import Shmessy


def test_read_csv(files_folder):
    df = Shmessy().read_csv(files_folder.as_posix() + "/data_1.csv")

    assert df["created_at"].dtype == np.dtype("datetime64[ns]")
    assert df["modified_at"].dtype == np.dtype("datetime64[ns]")
    assert df["deleted_at"].dtype == np.dtype("datetime64[ns]")
    assert df["celebrated_at"].dtype == np.dtype("datetime64[ns]")
    assert df["joined_at"].dtype == np.dtype("datetime64[ns]")
    assert df["laughed_at"].dtype == np.dtype("datetime64[ns]")
    assert df["loled_at"].dtype == np.dtype("datetime64[ns]")
    assert df["fooled_at"].dtype == np.dtype("datetime64[ns]")
    assert df["emerged_at"].dtype == np.dtype("datetime64[ns]")
    assert df["processed_at"].dtype == np.dtype("datetime64[ns]")
    assert df["isolated_at"].dtype == np.dtype("datetime64[ns]")
    assert df["scheduled_at"].dtype == np.dtype("datetime64[ns]")
    assert df["unixed_at"].dtype == np.dtype("datetime64[ns]")


def test_read_csv_colon_as_delimiter(files_folder):
    df = Shmessy().read_csv(files_folder.as_posix() + "/data_3.csv")
    assert df["id"].dtype == np.dtype("int64")
    assert df["name"].dtype == np.dtype("O")
    assert df["value"].dtype == np.dtype("int64")


def test_read_csv_semicolon_as_delimiter(files_folder):
    df = Shmessy().read_csv(files_folder.as_posix() + "/data_4.csv")
    assert df["id"].dtype == np.dtype("int64")
    assert df["name"].dtype == np.dtype("O")
    assert df["value"].dtype == np.dtype("int64")


def test_buffer_as_read_csv_input(files_folder):
    path = files_folder.as_posix() + "/data_4.csv"
    with open(path, mode="rt") as file_input:
        df = Shmessy().read_csv(file_input)

    assert df["id"].dtype == np.dtype("int64")
    assert df["name"].dtype == np.dtype("O")
    assert df["value"].dtype == np.dtype("int64")


def test_read_csv_file_with_single_column(files_folder):
    path = files_folder.as_posix() + "/data_7.csv"
    with open(path, mode="r") as file_input:
        df = Shmessy().read_csv(file_input)
    assert df["header_name"].dtype == np.dtype("O")


def test_read_csv_with_text_data(files_folder):
    path = files_folder.as_posix() + "/data_8.csv"
    with open(path, mode="rt") as file_input:
        Shmessy(use_random_sample=False).read_csv(file_input, fallback_to_string=True)
        assert True


def test_empty_column_should_identified_as_string(files_folder):
    path = files_folder.as_posix() + "/data_10.csv"
    shmessy = Shmessy()
    with open(path, mode="rt") as file_input:
        df = shmessy.read_csv(file_input)
        schema = shmessy.get_inferred_schema()

    assert df["col_1"].dtype == np.dtype("O")
    assert df["col_2"].dtype == np.dtype("O")
    assert schema.columns[0].inferred_type == "String"
    assert schema.columns[1].inferred_type == "String"
