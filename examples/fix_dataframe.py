import pandas as pd
from pandas import DataFrame
from tabulate import tabulate

from src.shmessy import Shmessy


def add_data_types_to_column_names(df: DataFrame) -> dict:
    names = dict()
    for column in df.columns:
        name = column + " [" + str(df[column].dtype.type) + "]"
        name = name.replace("<class 'numpy.", "")
        name = name.replace("'>", "")
        names[column] = name
    return names


def print_original_df(df: DataFrame) -> None:
    df = df[:10]
    df = df.sort_values(by=['id'])
    df = df.rename(columns=add_data_types_to_column_names(df))
    print(tabulate(df, headers="keys", tablefmt="rounded_outline", showindex=False))


def print_fixed_df(df: DataFrame) -> None:
    df = Shmessy().fix_schema(df)
    df = df[:10]
    df = df.sort_values(by=['id'])
    df = df.rename(columns=add_data_types_to_column_names(df))
    print(tabulate(df, headers="keys", tablefmt="rounded_outline", showindex=False))


if __name__ == "__main__":
    input_df = pd.read_csv('../tests/data/data_1.csv')
    print_original_df(input_df)
    print_fixed_df(input_df)
