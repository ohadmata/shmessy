# Shmessy
[![PyPI version](https://badge.fury.io/py/shmessy.svg)](https://badge.fury.io/py/shmessy)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/shmessy)](https://pypi.org/project/shmessy/)
[![License](https://img.shields.io/:license-MIT-blue.svg)](https://opensource.org/license/mit/)
![Coverage report](https://raw.githubusercontent.com/ohadmata/shmessy/main/coverage.svg)
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

### Original Dataframe
╭──────────────┬────────────────────────┬────────────────────────┬───────────────────────────┬───────────────────────────╮
│   id [int64] │ birth_date [object_]   │ churn_date [object_]   │ register_date [object_]   │   timestamp_epoch [int64] │
├──────────────┼────────────────────────┼────────────────────────┼───────────────────────────┼───────────────────────────┤
│            0 │ 6-12-2002              │ 2008/9/3               │ 18.2.2011                 │                1608242400 │
│            1 │ 11-21-2013             │ 2030/6/7               │ 1.8.2008                  │                1111528800 │
│            2 │ 3-15-2005              │ 2014/5/17              │ 17.6.2008                 │                1673733600 │
│            3 │ 10-28-2014             │ 2008/3/2               │ 5.4.2021                  │                 968360400 │
│            4 │ 3-5-2019               │ 2018/12/11             │ 31.8.2019                 │                1901653200 │
│            5 │ 6-23-2020              │ 2013/10/15             │ 5.3.2015                  │                1589576400 │
│            6 │ 10-26-2025             │ 2017/4/8               │ 17.4.2028                 │                1896040800 │
│            7 │ 12-8-2016              │ 2006/2/26              │ 11.8.2016                 │                1159477200 │
│            8 │ 3-18-2028              │ 2023/9/20              │ 18.5.2027                 │                1434488400 │
│            9 │ 7-30-2009              │ 2030/3/29              │ 15.12.2010                │                1685653200 │
╰──────────────┴────────────────────────┴────────────────────────┴───────────────────────────┴───────────────────────────╯

### After fix
╭──────────────┬───────────────────────────┬───────────────────────────┬──────────────────────────────┬────────────────────────────────╮
│   id [int64] │ birth_date [datetime64]   │ churn_date [datetime64]   │ register_date [datetime64]   │ timestamp_epoch [datetime64]   │
├──────────────┼───────────────────────────┼───────────────────────────┼──────────────────────────────┼────────────────────────────────┤
│            0 │ 2002-06-12 00:00:00       │ 2008-09-03 00:00:00       │ 2011-02-18 00:00:00          │ 2020-12-17 22:00:00            │
│            1 │ 2013-11-21 00:00:00       │ 2030-06-07 00:00:00       │ 2008-08-01 00:00:00          │ 2005-03-22 22:00:00            │
│            2 │ 2005-03-15 00:00:00       │ 2014-05-17 00:00:00       │ 2008-06-17 00:00:00          │ 2023-01-14 22:00:00            │
│            3 │ 2014-10-28 00:00:00       │ 2008-03-02 00:00:00       │ 2021-04-05 00:00:00          │ 2000-09-07 21:00:00            │
│            4 │ 2019-03-05 00:00:00       │ 2018-12-11 00:00:00       │ 2019-08-31 00:00:00          │ 2030-04-05 21:00:00            │
│            5 │ 2020-06-23 00:00:00       │ 2013-10-15 00:00:00       │ 2015-03-05 00:00:00          │ 2020-05-15 21:00:00            │
│            6 │ 2025-10-26 00:00:00       │ 2017-04-08 00:00:00       │ 2028-04-17 00:00:00          │ 2030-01-30 22:00:00            │
│            7 │ 2016-12-08 00:00:00       │ 2006-02-26 00:00:00       │ 2016-08-11 00:00:00          │ 2006-09-28 21:00:00            │
│            8 │ 2028-03-18 00:00:00       │ 2023-09-20 00:00:00       │ 2027-05-18 00:00:00          │ 2015-06-16 21:00:00            │
│            9 │ 2009-07-30 00:00:00       │ 2030-03-29 00:00:00       │ 2010-12-15 00:00:00          │ 2023-06-01 21:00:00            │
╰──────────────┴───────────────────────────┴───────────────────────────┴──────────────────────────────┴────────────────────────────────╯