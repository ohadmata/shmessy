from src.shmessy import Shmessy
from utils import pretty_print_df, init_logger


if __name__ == "__main__":
    init_logger()
    shmessy = Shmessy(types_to_ignore=["unixTimestamp"])
    df = shmessy.read_csv('../tests/data/test_timestamp.csv')
    inferred_schema = shmessy.get_inferred_schema()
    pretty_print_df(df=df, inferred_schema=inferred_schema)
