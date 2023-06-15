import pandas as pd
import numpy as np
import common.etl as etl

from pandas import DataFrame
from common.globals import Data, Units, Unify, OwnRevenue
from common.data_frame import filter_by_var, filter_by_id, unify
from common.stats import basic_stats, quantile_score, adjust_score
from common.utils import timeit, rename
from common.data_frame import change_types


'''
Durchschnittliche jährliche Entwicklung des Gewerbesteuergrundaufkommens je Einwohner 
von 2012/13 bis 2017/18 in %

We load own revenue data, and we count the change between each year. 
Own revenue data are very similar to population and working age. It should be quite easy to process them.
We have various possible municipality revenue parameters. Own revenue and total revenue. 
In 1st iteration we take an own revenue and we could go with total revenue to see if there are any big differences.

We process the average for 5 years period, which will be used for identifing shrinking cities. 
We process parameters with Milbert methodology where we assign points based on quantiles. 
In contrary to Milbert approach we don't smooth the data with 2 years average, but we take values year by year.

However some data may contain value gaps. We don't know why they exist. 
Either they were intentional and cities had no budget or there was a problem with db.
Also data are given in float but we convert them directly to int and we ommit fraction part.

Preprocessing
- filter data based on variable
- unify data valuse based on configuration

For own revenue score adjustment point is 3rd quantile, which means every value above 0 gets 2 score points.
'''


@timeit
@rename('own_revenue_prep')
def prep():
    pre_loaded = False

    # init
    basic_df = etl.extract(Units.BASIC_DATA, Units.HEADER, Units.TYPES)
    conf_df = etl.extract(Unify.DATA, Unify.HEADER, Unify.TYPES)

    if pre_loaded:
        # direct reading from own_revenue_raw
        data_df = etl.extract(OwnRevenue.FIGURES + '/own_revenue_raw.csv', Data.HEADER, Data.TYPES)

    else:
        # read from main source
        data_df = etl.extract(OwnRevenue.DATA, Data.HEADER, Data.TYPES)

        # filtered out data based on variable, save for reference
        data_df = filter_by_var(data_df, OwnRevenue.VAR_ID)
        etl.load(data_df, OwnRevenue.FIGURES + '/own_revenue_raw.csv')

    # unify data: replace, merge, remove
    data_df = unify(data_df, conf_df)
    etl.load(data_df, OwnRevenue.FIGURES + '/own_revenue_unify.csv')

    # leave only units from specific data source, in our case crosscheck with basic_df
    id_list = basic_df['unit_id'].values.tolist()
    data_df = filter_by_id(data_df, id_list)
    etl.load(data_df, OwnRevenue.FIGURES + '/own_revenue_basic.csv')

@timeit
@rename('own_revenue_stats')
def stats():
    pass

    # # init
    # data_df = etl.extract(WorkingAge.FIGURES + '/working_age_basic.csv', Data.HEADER, Data.TYPES)
    
    # # Milbert - working_age score
    # stats_df = basic_stats(data_df)
    # stats_df = change_types(stats_df, WorkingAge.TYPES)
    # etl.load(stats_df, WorkingAge.FIGURES + '/working_age_stats.csv', ff='%.16f')
    
    # quantile_df = quantile_score(stats_df, 'gmean')
    # quantile_df = adjust_score(quantile_df, 'gmean', 0)
    # quantile_df = change_types(quantile_df, WorkingAge.TYPES)
    # etl.load(quantile_df, WorkingAge.FIGURES + '/working_age_score.csv', ff='%.16f')
