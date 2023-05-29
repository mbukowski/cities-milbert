import numpy as np

from pandas import DataFrame
from common.globals import Data

QUANTILE_DISTRIBUTION = [0.2, 0.4, 0.6, 0.8]
CIRES_DISTRIBUTION = [-0.005, -0.0015, 0.0015, 0.005]

'''
Calculate simple stats with basic scenario for parameters:
- population
- ...
'''
def simple_stats(df: DataFrame, win_len=5) -> DataFrame:
    df['diff'], df['rate'], df['mean'] = np.NaN, np.NaN, np.NaN

    by_id = df.groupby('unit_id')
    for unit_id, frame in by_id:
        frame['diff'] = frame['val'].diff()
        frame['rate'] = frame['diff'] / (frame['val'] - frame['diff'])
        frame['mean'] = frame['rate'].rolling(window=win_len).mean()
        df.update(frame)

    df = df.astype(Data.TYPES)

    return df

'''
Adds quantile score to our data
'''
def quantile_stats(df, reversed=False) -> DataFrame:
    # we need to drop all rows where we don't have NaN values in mean, 
    # otherwise we can't calculate quantiles
    df = df.dropna().copy()
    df.reset_index(drop=True, inplace=True)

    # only then we add a new column otherwise we would have whole df empty
    df['score'] = np.NaN

    by_year = df.groupby('year')
    for year, frame in by_year:
        quantiles = frame['mean'].quantile(QUANTILE_DISTRIBUTION).values.tolist()
        frame['score'] = frame.apply(lambda row: score(row['mean'], quantiles, reversed=reversed), axis=1)
        df.update(frame)

    # score has to be mapped manually
    df = df.astype(Data.TYPES)
    df = df.astype({'score': 'Int64'})

    return df

'''
In period stats we compare values over longer period of time, ie. we don't compare to previous year but according to window length.
Mostly used for cires stats, thus we don't require a ratio calculated
'''
def period_stats(df, win_len=5) -> DataFrame:
    df['c_diff'], df['c_rate'] = np.NaN, np.NaN

    by_id = df.groupby('unit_id')
    for unit_id, frame in by_id:
        frame['c_diff'] = frame['val'].diff(win_len)
        frame['c_rate'] = frame['c_diff'] / (frame['val'] - frame['c_diff'])
        df.update(frame)

    # specific columns mapped separately
    df = df.astype(Data.TYPES)
    df = df.astype({'c_diff': 'Int64', 'c_rate': 'Float64'})

    return df

'''
Processing cires parameter for mean and c_rate columns. 
Mean sounds to be much more correct - much more polished, 
but for the sake of experiment we also take under consideration we take also begin and the end of the period.
'''
def cires_stats(df) -> DataFrame:
    # first we drop all rows where we don't have NaN values
    df = df.dropna().copy()
    df.reset_index(drop=True, inplace=True)

    # we add two columns, one for avarege rate and another one for simple period
    df['cires_rate'], df['cires_period'] = np.NaN, np.NaN

    by_year = df.groupby('year')
    for year, frame in by_year:
        frame['cires_rate'] = frame.apply(lambda row: score(row['mean'], CIRES_DISTRIBUTION), axis=1)
        frame['cires_period'] = frame.apply(lambda row: score(row['c_rate'], CIRES_DISTRIBUTION), axis=1)
        df.update(frame)

    # score has to be mapped manually
    df = df.astype(Data.TYPES)
    df = df.astype({'cires_rate': 'Int64'})
    df = df.astype({'cires_period': 'Int64'})

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
