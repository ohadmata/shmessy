import pandas as pd

from src.shmessy import Shmessy

if __name__ == "__main__":
    input_df = pd.read_csv('../tests/data/data_1.csv')
    schema = Shmessy().infer_schema(input_df)
    print(schema.dict())
