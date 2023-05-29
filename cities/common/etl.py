import pandas as pd

from pandas import DataFrame
from pathlib import Path

def extract(path: str, header: list[str], types: dict[str, str]) -> DataFrame:
    return pd.read_csv(path, sep=',', header=0, names=header, dtype=types)

def load(df: DataFrame, path: str, ff='%.2f'):
    # creates a parent folder if that doesn't exist
    Path(Path(path).parent).mkdir(parents=True, exist_ok=True)
    df.to_csv(path, float_format=ff, index=False)

