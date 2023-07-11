import pandas as pd
import numpy as np
import common.etl as etl

from pandas import DataFrame
from common.globals import Data, Units, Unify, WorkingAge
from common.data_frame import filter_by_var, filter_by_id, unify
from common.stats import basic_stats, quantile_score, adjust_score
from common.utils import timeit, rename
from common.data_frame import change_types


'''
Durchschnittliche jährliche Entwicklung der nach Alter Erwerbsfähigen (20 bis 64 Jahre) 
2013 bis 2018 in %

We load working age data, and we count the change between each year. 
Working age data are very similar to population. And it should be quite easy to process them. 

We process the average for 5 years period, which will be used for identifing shrinking cities: 
- aligned with Milbert methodology where we assign points based on quantiles

Preprocessing
- filter data based on variable
- unify data valuse based on configuration

Like with population a border for adjusted score is 4th quantile, which means every value above 0 gets 3 score points.
'''


@timeit
@rename('working_age_prep')
def prep():
    pre_loaded = False

    # init
    # basic_df = etl.extract(Units.BASIC_DATA, Units.HEADER, Units.TYPES)
    full_df = etl.extract(Units.FULL_DATA, Units.HEADER, Units.TYPES)
    conf_df = etl.extract(Unify.DATA, Unify.HEADER, Unify.TYPES)

    if pre_loaded:
        # direct reading from working_age_raw
        data_df = etl.extract(WorkingAge.FIGURES + '/working_age_raw.csv', Data.HEADER, Data.TYPES)
        data_df['val'] = data_df['val'].astype(np.int64)

    else:
        # read from main source
        data_df = etl.extract(WorkingAge.DATA, Data.HEADER, Data.TYPES)
        data_df['val'] = data_df['val'].astype(np.int64)

        # filtered out data based on variable, save for reference
        data_df = filter_by_var(data_df, WorkingAge.VAR_ID)
        etl.load(data_df, WorkingAge.FIGURES + '/working_age_raw.csv')

    # unify data: replace, merge, remove
    data_df = unify(data_df, conf_df)
    etl.load(data_df, WorkingAge.FIGURES + '/working_age_unify.csv')

    # leave only units from specific data source, in our case crosscheck with basic_df
    id_list = full_df['unit_id'].values.tolist()
    data_df = filter_by_id(data_df, id_list)
    etl.load(data_df, WorkingAge.FIGURES + '/working_age_full.csv')

@timeit
@rename('working_age_stats')
def stats():
    # init
    data_df = etl.extract(WorkingAge.FIGURES + '/working_age_full.csv', Data.HEADER, Data.TYPES)
    
    # Milbert - working_age score
    stats_df = basic_stats(data_df)
    stats_df = change_types(stats_df, WorkingAge.TYPES)
    etl.load(stats_df, WorkingAge.FIGURES + '/working_age_stats.csv', ff='%.16f')
    
    quantile_df = quantile_score(stats_df, 'gmean')
    quantile_df = adjust_score(quantile_df, 'gmean', 3, 0)
    quantile_df = change_types(quantile_df, WorkingAge.TYPES)
    etl.load(quantile_df, WorkingAge.FIGURES + '/working_age_score.csv', ff='%.16f')
