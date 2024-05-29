import time

from src.shmessy import Shmessy
from utils import pretty_print_df, init_logger

if __name__ == "__main__":
    init_logger()
    shmessy = Shmessy()
    start_time = time.time()
    df = shmessy.read_csv('../tests/data/data_1.csv')
    inferred_schema = shmessy.get_inferred_schema()
    pretty_print_df(df=df, inferred_schema=inferred_schema)
    print(f"Duration: {int((time.time() - start_time) * 1000)}")
