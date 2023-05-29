import pandas as pd
import numpy as np
import common.etl as etl

from pandas import DataFrame
from common.globals import Data, Units, Unify, Population
from common.data_frame import filter_by_var, filter_by_level, filter_by_level_kind, filter_by_id, unify
from common.utils import timeit, rename


'''
We load population data, we count the change between each year. 
We process the average for 5 years period, which will be used for identifing shrinking cities: 
- according to classic definition CIRES - in this definition we could work with units_city dataset
- aligned with Milbert methodology where de assign points based on quantiles

Preprocessing
- filter data based on variable
- unify data valuse based on configuration
'''


@timeit
@rename('population_prep')
def prep():
    pre_loaded = True

    # init
    basic_df = etl.extract(Units.BASIC_DATA, Units.HEADER, Units.TYPES)
    conf_df = etl.extract(Unify.DATA, Unify.HEADER, Unify.TYPES)

    if pre_loaded:
        # direct reading from population_raw
        data_df = etl.extract(Population.FIGURES + '/population_raw.csv', Data.HEADER, Data.TYPES)

    else:
        data_df = etl.extract(Population.DATA, Data.HEADER, Data.TYPES)

        # filtered out data based on variable
        data_df = filter_by_var(data_df, Population.VAR_ID)
        etl.load(data_df, Population.FIGURES + '/population_raw.csv')

    # unify data: replace, merge, remove
    data_df = unify(data_df, conf_df)
    etl.load(data_df, Population.FIGURES + '/populuation_unify.csv')

    # leave only units from specific data source, in our case crosscheck with basic_df
    id_list = basic_df['unit_id'].values.tolist()
    data_df = filter_by_id(data_df, id_list)
    etl.load(data_df, Population.FIGURES + '/populuation_prep.csv')


@timeit
@rename('population_stats')
def stats():


#     step_df = pd.merge(step_df, population_df[['id', 'year', 'population']], on=['id', 'year'])
# step_df[param_pp] = step_df['own_revenue'] / step_df['population']

# step_df['diff'], step_df['rate'], step_df['mean'] = np.NaN, np.NaN, np.NaN
# by_id = step_df.groupby('id')
# for id, frame in by_id:
#     frame['diff'] = frame['own_revenue_pp'].diff()
#     frame['rate'] = frame['diff'] / (frame[param_pp] - frame['diff'])
#     frame['mean'] = frame['rate'].rolling(window=5).mean()
#     step_df.update(frame)

# stats_df = init_stats_df(step_df, [param, param_pp, ratio, 'parentId', 'population', 'diff', 'rate'])
# stats_quantile_score(stats_df, score)


    # avg from last 2 years + group by
    # quantile division

    # need to generate 3 files
    # stats
    # cires 
    # milbert

    pass
    # print(conf_df.head())
    # print()

    # print(basic_df.head())
    # print()

    # print(population_df.head(100))
    # print()

