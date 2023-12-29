import os

import pandas as pd
from parametrization import Parametrization

from shmessy import Shmessy
import sys


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="Test demo data 1",
    file_path="data/data_1.csv",
)
@Parametrization.case(
    name="Test demo data 2",
    file_path="data/data_2.csv",
)
def test_duration_for_sample_file_should_be_less_than_300_ms(file_path, request):
    print("fff")
    print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    tests_root = os.path.join(request.config.rootdir, "..")
    df = pd.read_csv(os.path.join(tests_root, file_path))
    result = Shmessy().infer_schema(df)
    assert result.infer_duration_ms < 300

