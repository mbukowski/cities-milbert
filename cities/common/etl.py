import pandas as pd
import numpy as np

from scipy.interpolate import interp1d
from pandas import DataFrame
from pathlib import Path

'''
Loads a dataframe from the csv file.
'''
def extract(path: str, header: list[str], types: dict[str, str]) -> DataFrame:
    return pd.read_csv(path, sep=',', header=0, names=header, dtype=types)

'''
Saves a dataframe back to a csv file.
'''
def load(df: DataFrame, path: str, ff='%.2f'):
    # creates a parent folder if that doesn't exist
    Path(Path(path).parent).mkdir(parents=True, exist_ok=True)
    df.to_csv(path, float_format=ff, index=False)

'''
Fills NaN gaps in the dataframe for specific column. 
First grouping it by specific another column. 
- col_group: column to group by values, typically unit_id 
- col_val:   column with missing entries which we intend to interpolate (y-axis)
'''
def interpolate(df: DataFrame, col_group: str, col_val: str) -> DataFrame:
    by_col = df.groupby(col_group)
    for unit_id, frame in by_col:
        if frame[col_val].isnull().values.any():
            frame[col_val] = frame[col_val].interpolate(method='linear', limit_direction='both')

            df.update(frame)
        
    return df
