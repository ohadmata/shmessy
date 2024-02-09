import pandas

from src.shmessy import Shmessy
from utils import pretty_print_df, init_logger


if __name__ == "__main__":
    init_logger()
    shmessy = Shmessy()
    df = pandas.read_excel("../tests/data/data_9.xlsx")
    df = shmessy.fix_schema(df)
    inferred_schema = shmessy.get_inferred_schema()
    pretty_print_df(df=df, inferred_schema=inferred_schema)
