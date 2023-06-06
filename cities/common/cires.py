import numpy as np

from pandas import DataFrame
from common.globals import Data
from common.stats import score

CIRES_DISTRIBUTION = [-0.005, -0.0015, 0.0015, 0.005]

'''
Separate file for processing CIRES like statistics in order to keep main milbert file readable
'''


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
        frame['cires_rate'] = frame.apply(lambda row: score(row['gmean'], CIRES_DISTRIBUTION), axis=1)
        frame['cires_period'] = frame.apply(lambda row: score(row['c_rate'], CIRES_DISTRIBUTION), axis=1)
        df.update(frame)

    # score has to be mapped manually
    df = df.astype(Data.TYPES)
    df = df.astype({'cires_rate': 'Int64'})
    df = df.astype({'cires_period': 'Int64'})

    return df
