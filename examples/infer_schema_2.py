import pandas as pd
import json

from src.shmessy import Shmessy

if __name__ == "__main__":
    input_df = pd.read_csv('../tests/data/data_5.csv')
    schema = Shmessy().infer_schema(input_df)
    print(json.dumps(schema.dict(), indent=4))
