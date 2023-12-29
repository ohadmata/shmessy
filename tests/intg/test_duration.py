import pandas as pd
from parametrization import Parametrization

from shmessy import Shmessy


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Test demo data 1",
    file_path="tests/data/data_1.csv",
)
@Parametrization.case(
    name="Test demo data 2",
    file_path="tests/data/data_2.csv",
)
def test_duration_for_sample_file_should_be_less_than_350_ms(file_path):
    df = pd.read_csv(file_path)
    result = Shmessy().infer_schema(df)
    assert result.infer_duration_ms < 350

