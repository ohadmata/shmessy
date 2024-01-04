from src.shmessy import Shmessy
from utils import pretty_print_df


if __name__ == "__main__":
    pretty_print_df(Shmessy().read_csv('../tests/data/data_4.csv'))
