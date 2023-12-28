# Shmessy
### Got messy data? Use shmessy to fix it!

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

### Identify and fix Pandas Dataframe
```python
import pandas as pd
from shmessy import Shmessy

df = pd.read_csv('/tmp/file.csv')
fixed_df = Shmessy().fix_schema(df)
```
