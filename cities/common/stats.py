import numpy as np

from pandas import DataFrame
from scipy.stats import gmean
from common.globals import Data, Population

QUANTILE_DISTRIBUTION = [0.2, 0.4, 0.6, 0.8]

'''
Calculate basic stats with basic scenario for parameters:
- population
- working_age
- employment
- own_revenue

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
Calculate stats with predefined rate, scenario for parameters:
- migration

In contrary to basic stats we simply sum up provided rates in given window.
'''
def rate_sum_stats(df: DataFrame, win_len=5) -> DataFrame:
    df['sum'] = np.NaN

    by_id = df.groupby('unit_id')
    for unit_id, frame in by_id:
        window = frame['rate'].rolling(window=win_len)
        frame['sum'] = window.sum()

        df.update(frame)

    return df


'''
Calculate stats with predefined rate, scenario for parameters:
- unemployed

In this case we follow regular gmean method like with most of the parameters.
This is little more complicated than originally but we only need to calculate it for unemployed rate. 
Order of the columns is little different here. Rate means unpemployment rate, 
which we substract from each other year by year.
'''
def rate_gmean_stats(df: DataFrame, win_len=5) -> DataFrame:
    df['diff'], df['mean'], df['gmean'] = np.NaN, np.NaN, np.NaN

    by_id = df.groupby('unit_id')
    for unit_id, frame in by_id:
        frame['diff'] = frame['rate'].diff()

        window = frame['diff'].rolling(window=win_len)
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
        quantiles = frame[param].quantile(QUANTILE_DISTRIBUTION).values.tolist()
        frame['score'] = frame.apply(lambda row: score(row[param], quantiles, reversed=reversed), axis=1)
        df.update(frame)

    return df


'''
Adds quantile score to our data  based on valuse of a specific column, filtered by defined columns
'''
def quantile_score_ext(df: DataFrame, param: str, col_a: str, col_b: str, reversed=False) -> DataFrame:
    # we need to drop all rows where we don't have NaN values in mean, 
    # otherwise we can't calculate quantiles
    df = df.dropna().copy()
    df.reset_index(drop=True, inplace=True)

    # only then we add a new column otherwise we would have whole df empty
    df['score'] = np.NaN

    by_cols = df.groupby([col_a, col_b])
    for frame_id, frame in by_cols:
        quantiles = frame[param].quantile(QUANTILE_DISTRIBUTION).values.tolist()
        frame['score'] = frame.apply(lambda row: score(row[param], quantiles, reversed=reversed), axis=1)
        df.update(frame)

    return df

'''
Groups values for a given parameter according to a given distribution 
and save the value in a new column with given name.
'''
def distribution_group(df: DataFrame, param: str, col: str, group_name: str, distribution:list[float]) -> DataFrame:
    # we need to drop all rows where we don't have NaN values in param, 
    # otherwise we can't calculate distribution
    df = df.dropna().copy()
    df.reset_index(drop=True, inplace=True)

    # only then we add a new column otherwise we would have whole df empty
    df[group_name] = np.NaN

    by_col = df.groupby(col)
    for year, frame in by_col:
        quantiles = frame[param].quantile(distribution).values.tolist()
        frame[group_name] = frame.apply(lambda row: group(row[param], quantiles, reversed=reversed), axis=1)
        df.update(frame)

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
Very similar as above but we return char 'groups' which indicate bucket according to the distribution
'''
def group(v: float, q: list[float], reversed=False) -> str:
    res = len(q)

    for i in range(len(q)):
        if v < q[i]:
            res = i
            break

    if reversed:
        res = len(q) - res

    val = ord('A') + res
    return chr(val)


'''
For most of the parameters we additionally adjust calculated scored based on specific threshold value.
For example:
    For population parameter the rate value 0 is used as imit determined for the 4th quintile. 
    Positive developments always fall at the very least 4th quintile and are therefore rated with at least 3 points.

We have a special case for unemployed, but looks like that with a small adjustment, 
a regular function can make a work done.


| parameter | threshold | minimum score |
| --------- | --------- | ------------- |
| population |        0 |             3 |
| working_age |       0 |             3 |
| own_revenue |       0 |             2 |
| employment |        0 |             2 |
| migration |         0 |             2 |
| unemployed |        0 |             0 |
'''
def adjust_score(df: DataFrame, param: str, min_score: int, threshold: int, reversed=False) -> DataFrame:
    df['adj_score'] = np.NaN

    # unemployeb
    if reversed:
        df['adj_score'] = df.apply(lambda row: min(min_score, row['score']) if(row[param] > threshold) else row['score'], axis=1)
    # eveerything else
    else:
        df['adj_score'] = df.apply(lambda row: max(min_score, row['score']) if(row[param] > threshold) else row['score'], axis=1)

    return df
