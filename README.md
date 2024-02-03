# Shmessy
[![PyPI version](https://badge.fury.io/py/shmessy.svg)](https://badge.fury.io/py/shmessy)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/shmessy)](https://pypi.org/project/shmessy/)
![Coverage report](https://raw.githubusercontent.com/ohadmata/shmessy/main/assets/coverage.svg)
[![CI](https://github.com/ohadmata/shmessy/actions/workflows/main.yml/badge.svg)](https://github.com/ohadmata/shmessy/actions/workflows/main.yml)
[![License](https://img.shields.io/:license-MIT-blue.svg)](https://opensource.org/license/mit/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/shmessy)](https://pypi.org/project/shmessy/)
![OS](https://img.shields.io/badge/ubuntu-blue?logo=ubuntu)
![OS](https://img.shields.io/badge/mac-blue?logo=apple)
![OS](https://img.shields.io/badge/win-blue?logo=windows)
### If your data is messy - Use Shmessy!

Shmessy designed to deal with messy pandas dataframes.
We all knows the frustrating times when we as analysts or data-engineers should handle messy dataframe and analyze them by ourselves.

The goal of this tiny tool is to identify the physical / logical data type for each Dataframe column.
It based on fast validators that will validate the data (Based on a sample) against regex / pydantic types or any additional validation function that you want to implement.

As you understand, this tool was designed to deal with dirty data, 
ideally developed for Dataframes generated from CSV / Flat files or any source that doesn't contain strict schema.

## Installation
```python
pip install shmessy
```

## Usage

You have two ways to use this tool

### Identify the Dataframe schema
```python
import pandas as pd
from shmessy import Shmessy

df = pd.read_csv('/tmp/file.csv')
inferred_schema = Shmessy().infer_schema(df)
```

Output (inferred_schema dump):
```json
{
    "infer_duration_ms": 12,
    "columns": [
        {
            "field_name": "id",
            "source_type": "Integer",
            "inferred_type": "Integer"
        },
        {
            "field_name": "email_value",
            "source_type": "String",
            "inferred_type": "Email"
        },
        {
            "field_name": "date_value",
            "source_type": "String",
            "inferred_type": "Date",
            "inferred_pattern": "%d-%m-%Y"
        },
        {
            "field_name": "datetime_value",
            "source_type": "String",
            "inferred_type": "Datetime",
            "inferred_pattern": "%Y/%m/%d %H:%M:%S"
        },
        {
            "field_name": "yes_no_data",
            "source_type": "String",
            "inferred_type": "Boolean",
            "inferred_pattern": [
                "YES",
                "NO"
            ]
        },
        {
            "field_name": "unix_value",
            "source_type": "Integer",
            "inferred_type": "UnixTimestamp",
            "inferred_pattern": "ms"
        },
        {
            "field_name": "ip_value",
            "source_type": "String",
            "inferred_type": "IPv4"
        }
    ]
}
```

### Identify and fix Pandas Dataframe
This piece of code will change the column types of the input Dataframe according to Messy infer.
```python
import pandas as pd
from shmessy import Shmessy

df = pd.read_csv('/tmp/file.csv')
fixed_df = Shmessy().fix_schema(df)
```

#### Original Dataframe
![Original Dataframe](https://raw.githubusercontent.com/ohadmata/shmessy/main/assets/screenshot_1.png)

#### Fixed Dataframe
![After fix](https://raw.githubusercontent.com/ohadmata/shmessy/main/assets/screenshot_2.png)


### Read Messy CSV file
```python
from shmessy import Shmessy
df = Shmessy().read_csv('/tmp/file.csv')
```

#### Original file
![Original Dataframe](https://raw.githubusercontent.com/ohadmata/shmessy/main/assets/screenshot_3.png)

#### Fixed Dataframe
![After fix](https://raw.githubusercontent.com/ohadmata/shmessy/main/assets/screenshot_4.png)


## API

### Constructor
```python
shmessy = Shmessy(
    sample_size: Optional[int] = 1000,
    reader_encoding: Optional[str] = "UTF-8",
    locale_formatter: Optional[str] = "en_US"
)
```

### read_csv
```python
shmessy.read_csv(
    filepath_or_buffer: str | TextIO | BinaryIO,
    use_sniffer: Optional[bool] = True,  # Use python sniffer to identify the dialect (seperator / quote-char / etc...)
    fixed_schema: Optional[ShmessySchema] = None,  # Fix the given CSV according to this schema
    fix_column_names: Optional[bool] = False,  # Replace non-alphabetic/numeric chars with underscore
    fallback_to_string: Optional[bool] = False,  # Fallback to string in case of casting exception
) -> DataFrame
```

### infer_schema
```python
shmessy.infer_schema(
    df: Dataframe  # Input dataframe
) -> ShmessySchema
```

### fix_schema
```python
shmessy.fix_schema(
    df: Dataframe,
    fix_column_names: Optional[bool] = False,  # Replace non-alphabetic/numeric chars with underscore
    fixed_schema: Optional[ShmessySchema] = None,  # Fix the given DF according to this schema
    fallback_to_string: Optional[bool] = False,  # Fallback to string in case of casting exception
) -> DataFrame
```

### get_inferred_schema
```python
shmessy.get_inferred_schema() -> ShmessySchema
```
