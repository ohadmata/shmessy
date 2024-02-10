import os
import random
from datetime import datetime
from uuid import uuid4

import pandas as pd
import pytest
from parametrization import Parametrization
from shmessy import Shmessy


@pytest.fixture
def create_large_file(tmp_files_folder) -> str:
    file_path = tmp_files_folder / "large_csv_file.csv"
    outsize = 1024 * 1024 * 128  # 100MB
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, "w") as csvfile:
        size = 0
        while size < outsize:
            text = f"{uuid4()},{datetime.now()},{datetime.now().strftime('%d/%m/%Y')},{random.randrange(1000)}\n"
            size += len(text)
            csvfile.write(text)
    return file_path.as_posix()


def test_large_file_infer_should_be_less_than_3000_ms(create_large_file):
    df = pd.read_csv(create_large_file)
    result = Shmessy().infer_schema(df)
    assert result.infer_duration_ms < 3000


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Test demo data 1",
    file_path="data_1.csv",
)
@Parametrization.case(
    name="Test demo data 2",
    file_path="data_2.csv",
)
def test_duration_for_sample_file_should_be_less_than_3000_ms(file_path,files_folder):
    path = files_folder.as_posix() + f"/{file_path}"
    df = pd.read_csv(path)
    result = Shmessy().infer_schema(df)
    assert result.infer_duration_ms < 3000

