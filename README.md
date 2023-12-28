# Shmessy
[![PyPI version](https://badge.fury.io/py/shmessy.svg)](https://badge.fury.io/py/shmessy)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/shmessy)](https://pypi.org/project/shmessy/)
[![License](https://img.shields.io/:license-MIT-blue.svg)](https://opensource.org/license/mit/)
![Coverage report](./coverage.svg)
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
    "infer_duration_ms": 91,
    "columns": [
        {
            "field_name": "first_name",
            "source_type": "<class 'numpy.object_'>",
            "inferred_type": "None"
        },
        {
            "field_name": "email",
            "source_type": "<class 'numpy.object_'>",
            "inferred_type": "<class 'str'>",
            "inferred_virtual_type": "<class 'pydantic.networks.EmailStr'>"
        },
        {
            "field_name": "ip_address",
            "source_type": "<class 'numpy.object_'>",
            "inferred_type": "<class 'str'>",
            "inferred_virtual_type": "<class 'ipaddress.IPv4Address'>"
        },
        {
            "field_name": "created_at",
            "source_type": "<class 'numpy.object_'>",
            "inferred_type": "<class 'datetime.date'>",
            "inferred_pattern": "%m/%d/%Y"
        },
        {
            "field_name": "modified_at",
            "source_type": "<class 'numpy.object_'>",
            "inferred_type": "<class 'datetime.datetime'>",
            "inferred_pattern": "%Y-%m-%d %H:%M:%S"
        },
        {
            "field_name": "unixed_at",
            "source_type": "<class 'numpy.float64'>",
            "inferred_type": "<class 'datetime.datetime'>",
            "inferred_pattern": "ms"
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
