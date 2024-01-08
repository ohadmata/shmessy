from src.shmessy import Shmessy
from utils import pretty_print_df


if __name__ == "__main__":
    df, inferred_schema = Shmessy().read_csv('../tests/data/data_4.csv')
    pretty_print_df(df=df, inferred_schema=inferred_schema)
