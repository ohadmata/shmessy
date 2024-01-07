from pandas import DataFrame
from tabulate import tabulate
from typing import Optional, Dict
from shmessy.schema import ShmessySchema


def add_data_types_to_column_names(df: DataFrame, inferred_schema: Optional[ShmessySchema] = None) -> dict:
    names = dict()
    if inferred_schema:
        for column in inferred_schema.columns:
            names[column.field_name] = f"{column.field_name} [{column.inferred_type}]"
        return names

    for column in df.columns:
        name = f"{column} [{df[column].dtype.type}]"
        name = name.replace("<class 'numpy.", "")
        name = name.replace("'>", "")
        names[column] = name
    return names


def pretty_print_df(
        df: DataFrame,
        *,
        sample_size: Optional[int] = 10,
        sort_key: Optional[str] = "id",
        inferred_schema: Optional[ShmessySchema] = None
) -> None:
    df = df[:sample_size]
    df = df.sort_values(by=[sort_key])
    df = df.rename(columns=add_data_types_to_column_names(df, inferred_schema))
    print(tabulate(df, headers="keys", tablefmt="rounded_outline", showindex=False))
