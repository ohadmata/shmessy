import pandas as pd

from src.shmessy import Shmessy
from utils import pretty_print_df

if __name__ == "__main__":
    df = pd.read_csv('../tests/data/data_1.csv')

    print("Original dataframe:")
    pretty_print_df(df)

    print("Fixed dataframe:")
    shmessy = Shmessy()
    df = shmessy.fix_schema(df)
    inferred_schema = shmessy.get_inferred_schema()
    pretty_print_df(
        df=df,
        inferred_schema=inferred_schema
    )
