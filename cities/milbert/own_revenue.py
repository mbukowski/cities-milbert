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

Data for revenue in contrary to other parameters (population, working_age) are provided in float format.

Preprocessing
- filter data based on variable
- unify data valuse based on configuration

We identified 4 entries with data gaps:
060611211021,76070,1995,0.00
060611211021,76070,1996,0.00
060611211021,76070,1997,0.00
030210321011,76070,2019,0.00

060611211021 - Stoczek Łukowski
- a new city municipality was craeted from 1998 thus missing data
- current population ~2.5k

030210321011 Boguszów-Gorce
- current population ~15k

Only few points missind and units are outside our analysis interest. 
All missing data will are interporpolated with linear method. Unfortunately using polynomial or cubic / quadratic, 
doesn't yield good results as we are missing more data at the begin - we don't have a starting point in some cases. 
We could have taken care of it if we would have artificially make sure that each period has starting and ending valuues.
In our case it's not that crucial. Linear interpolation would be a good exercise as well as presented municipalities 
don't have a huge impact on the research.


For own revenue score adjustment point is 3rd quantile, which means every value above 0 gets 2 score points.
'''


@timeit
@rename('own_revenue_prep')
def prep():
    pre_loaded = False
    # commune_type = 'full'

    # init
    # basic_df = etl.extract(Units.BASIC_DATA, Units.HEADER, Units.TYPES)
    full_df = etl.extract(Units.FULL_DATA, Units.HEADER, Units.TYPES)
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

    # leave only units from specific data source, in our case crosscheck with full_df
    id_list = full_df['unit_id'].values.tolist()
    data_df = filter_by_id(data_df, id_list)
    # etl.load(data_df, OwnRevenue.FIGURES + '/own_revenue_basic.csv')

    # interpolate missing values, first we need to convert all 0s to np.NaN
    data_df['intrpl'] = data_df['val'].replace(0, np.nan)
    data_df = etl.interpolate(data_df, 'unit_id', 'intrpl')
    data_df = change_types(data_df, OwnRevenue.TYPES)
    etl.load(data_df, OwnRevenue.FIGURES + '/own_revenue_intrpl.csv')

    data_df['val'] = data_df['intrpl']
    data_df.drop(['intrpl'], inplace=True, axis=1)
    # etl.load(data_df, OwnRevenue.FIGURES + '/own_revenue_basic.csv')
    etl.load(data_df, OwnRevenue.FIGURES + '/own_revenue_full.csv')


@timeit
@rename('own_revenue_stats')
def stats():
    # init
    data_df = etl.extract(OwnRevenue.FIGURES + '/own_revenue_full.csv', Data.HEADER, Data.TYPES)
    
    # Milbert - own_revenue score
    stats_df = basic_stats(data_df)
    stats_df = change_types(stats_df, OwnRevenue.TYPES)
    etl.load(stats_df, OwnRevenue.FIGURES + '/own_revenue_stats.csv', ff='%.16f')
    
    quantile_df = quantile_score(stats_df, 'gmean')
    quantile_df = adjust_score(quantile_df, 'gmean', 2, 0)
    quantile_df = change_types(quantile_df, OwnRevenue.TYPES)
    etl.load(quantile_df, OwnRevenue.FIGURES + '/own_revenue_score.csv', ff='%.16f')
