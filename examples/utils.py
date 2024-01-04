from pandas import DataFrame
from tabulate import tabulate
from typing import Optional


def add_data_types_to_column_names(df: DataFrame) -> dict:
    names = dict()
    for column in df.columns:
        name = column + " [" + str(df[column].dtype.type) + "]"
        name = name.replace("<class 'numpy.", "")
        name = name.replace("'>", "")
        names[column] = name
    return names


def pretty_print_df(
        df: DataFrame,
        *,
        sample_size: Optional[int] = 10,
        sort_key: Optional[str] = "id"
) -> None:
    df = df[:sample_size]
    df = df.sort_values(by=[sort_key])
    df = df.rename(columns=add_data_types_to_column_names(df))
    print(tabulate(df, headers="keys", tablefmt="rounded_outline", showindex=False))
