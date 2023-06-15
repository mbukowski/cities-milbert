import numpy as np

from pandas import DataFrame
from scipy.stats import gmean
from common.globals import Data, Population

QUANTILE_DISTRIBUTION = [0.2, 0.4, 0.6, 0.8]

'''
Calculate simple stats with basic scenario for parameters:
- population
- working_age

We calculate both mean and gmean even though we need only gmean.
For geometric average, we add and substruct 1 as gmean function works only on positive values.
'''
def basic_stats(df: DataFrame, win_len=5) -> DataFrame:
    df['diff'], df['rate'], df['mean'], df['gmean'] = np.NaN, np.NaN, np.NaN, np.NaN

    by_id = df.groupby('unit_id')
    for unit_id, frame in by_id:
        frame['diff'] = frame['val'].diff()
        frame['rate'] = frame['diff'] / (frame['val'] - frame['diff'])

        window = frame['rate'].rolling(window=win_len)
        frame['mean'] = window.mean()
        frame['gmean'] = window.apply(lambda row: gmean(row + 1) - 1)

        df.update(frame)

    return df

'''
Adds quantile score to our data  based on valuse of a specific column
'''
def quantile_score(df, param: str, reversed=False) -> DataFrame:
    # we need to drop all rows where we don't have NaN values in mean, 
    # otherwise we can't calculate quantiles
    df = df.dropna().copy()
    df.reset_index(drop=True, inplace=True)

    # only then we add a new column otherwise we would have whole df empty
    df['score'] = np.NaN

    by_year = df.groupby('year')
    for year, frame in by_year:
        quantiles = frame['mean'].quantile(QUANTILE_DISTRIBUTION).values.tolist()
        frame['score'] = frame.apply(lambda row: score(row[param], quantiles, reversed=reversed), axis=1)
        df.update(frame)

    # score has to be mapped manually
    # df = df.astype(Data.TYPES)
    # df = df.astype({'score': 'Int64'})
    # df = change_types(df, Data.TYPES)
    # df = change_types(df, Population.TYPES)

    return df

'''
Finds out in which basket our value should belong to.
Function can be used for calculating quantiles as well as other distribution.

Calculate a quantile score for given value. We check in which bucket our value would end up
- v is value for which we search a bucket
- q is list of precalculated quantiles
'''
def score(v: float, q: list[float], reversed=False) -> int:
    res = len(q)

    for i in range(len(q)):
        if v < q[i]:
            res = i
            break

    if reversed:
        res = len(q) - res

    return res

'''
For most of the parameters we additionally adjust calculated scored based on specific threshold value.
For example:
    For population parameter the rate value 0 is used as imit determined for the 4th quintile. 
    Positive developments always fall at the very least 4th quintile and are therefore rated with at least 3 points.


| parameter | threshold | minimum score |
| --------- | --------- | ------------- |
| population |        0 |             3 |
| working_age |       0 |             3 |
'''
def adjust_score(df: DataFrame, param: str, value: int) -> DataFrame:
    df['adj_score'] = np.NaN
    df['adj_score'] = df.apply(lambda row: max(3, row['score']) if(row[param] > value) else row['score'] , axis=1)

    return df
