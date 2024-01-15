from numpy import dtypes

from shmessy import Shmessy


def test_read_csv():
    df = Shmessy().read_csv("tests/data/data_1.csv")

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


def test_read_csv_colon_as_delimiter():
    df = Shmessy().read_csv("tests/data/data_3.csv")

    assert isinstance(df["id"].dtype, dtypes.Int64DType)
    assert isinstance(df["name"].dtype, dtypes.ObjectDType)
    assert isinstance(df["value"].dtype, dtypes.Int64DType)


def test_read_csv_semicolon_as_delimiter():
    df = Shmessy().read_csv("tests/data/data_4.csv")

    assert isinstance(df["id"].dtype, dtypes.Int64DType)
    assert isinstance(df["name"].dtype, dtypes.ObjectDType)
    assert isinstance(df["value"].dtype, dtypes.Int64DType)


def test_buffer_as_read_csv_input():
    with open("tests/data/data_4.csv", mode="rt") as file_input:
        df = Shmessy().read_csv(file_input)

    assert isinstance(df["id"].dtype, dtypes.Int64DType)
    assert isinstance(df["name"].dtype, dtypes.ObjectDType)
    assert isinstance(df["value"].dtype, dtypes.Int64DType)


def test_binary_buffer_as_read_csv_input():
    with open("tests/data/data_4.csv", mode="rb") as file_input:
        df = Shmessy().read_csv(file_input)

    assert isinstance(df["id"].dtype, dtypes.Int64DType)
    assert isinstance(df["name"].dtype, dtypes.ObjectDType)
    assert isinstance(df["value"].dtype, dtypes.Int64DType)


def test_read_csv_wrong_number_of_columns():
    df = Shmessy().read_csv("tests/data/data_6.csv")
