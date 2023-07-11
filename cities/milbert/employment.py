import pandas as pd
import numpy as np
import common.etl as etl

from pandas import DataFrame
from common.globals import Data, Units, Unify, Employment
from common.data_frame import filter_by_var, filter_by_id, unify
from common.stats import basic_stats, quantile_score, adjust_score
from common.utils import timeit, rename
from common.data_frame import change_types


'''
Durchschnittliche jährliche Entwicklung der nach Alter Erwerbsfähigen (20 bis 64 Jahre) 
2013 bis 2018 in %

We load employment data, and we count the change between each year. 
Employment data are very similar to population. And it should be quite easy to process them. 

We process the average for 5 years period, which will be used for identifing shrinking cities: 
- aligned with Milbert methodology where we assign points based on quantiles

Preprocessing
- filter data based on variable
- unify data valuse based on configuration

For employment data we identified more possible gaps, which will be interpolated.
042214213013 - Czarna Woda ~3.1k
042214213013,54821,2020,0

042214213093 - Skarszewy ~14.9k
042214213093,54821,2020,0

042815617043 - Pasym ~5.2k
042815617043,54821,2019,0
042815617043,54821,2020,0
042815617043,54821,2021,0

042815617083 - Wielbark ~6.4k
042815617083,54821,2015,0
042815617083,54821,2016,0
042815617083,54821,2017,0
042815617083,54821,2018,0
042815617083,54821,2019,0
042815617083,54821,2020,0
042815617083,54821,2021,0

052615309033 - Klimontów ~7.8k
052615309033,54821,2021,0

052615309093 - Zawichost ~4.2k
052615309093,54821,2021,0

060611020043 - Krasnobród ~6.9k
060611020043,54821,2021,0

060611020153 - Zwierzyniec ~7.7k
060611020153,54821,2021,0

062013805011 - Hajnówka ~24.2k
062013805011,54821,2015,0

062013813011 - Wysokie Mazowieckie ~9.3k
062013813011,54821,2015,0

071422611011 - Maków Mazowiecki ~10.5k
071422611011,54821,2019,0

Only one city - Hajnowka can be seriously affected. But we can take this approximation as good enough.

Like with own revenue and mignration a border for adjusted score is 3rd quantile, 
which means every value above 0 gets adjeusted 2 score points.
'''


@timeit
@rename('employment_prep')
def prep():
    pre_loaded = False

    # init
    # basic_df = etl.extract(Units.BASIC_DATA, Units.HEADER, Units.TYPES)
    full_df = etl.extract(Units.FULL_DATA, Units.HEADER, Units.TYPES)
    conf_df = etl.extract(Unify.DATA, Unify.HEADER, Unify.TYPES)

    if pre_loaded:
        # direct reading from working_age_raw
        data_df = etl.extract(Employment.FIGURES + '/employment_raw.csv', Data.HEADER, Data.TYPES)
        data_df['val'] = data_df['val'].astype(np.int64)

    else:
        # read from main source
        data_df = etl.extract(Employment.DATA, Data.HEADER, Data.TYPES)
        data_df['val'] = data_df['val'].astype(np.int64)

        # filtered out data based on variable, save for reference
        data_df = filter_by_var(data_df, Employment.VAR_ID)
        etl.load(data_df, Employment.FIGURES + '/employment_raw.csv')

    # unify data: replace, merge, remove
    data_df = unify(data_df, conf_df)
    etl.load(data_df, Employment.FIGURES + '/employment_unify.csv')

    # leave only units from specific data source, in our case crosscheck with full_df
    id_list = full_df['unit_id'].values.tolist()
    data_df = filter_by_id(data_df, id_list)
    # etl.load(data_df, Employment.FIGURES + '/employment_basic.csv')

    # interpolate missing values, first we need to convert all 0s to np.NaN
    data_df['intrpl'] = data_df['val'].replace(0, np.nan)
    data_df = etl.interpolate(data_df, 'unit_id', 'intrpl')
    data_df = change_types(data_df, Employment.TYPES)
    etl.load(data_df, Employment.FIGURES + '/employment_intrpl.csv')

    data_df['val'] = data_df['intrpl']
    data_df.drop(['intrpl'], inplace=True, axis=1)
    # etl.load(data_df, Employment.FIGURES + '/employment_basic.csv')
    etl.load(data_df, Employment.FIGURES + '/employment_full.csv')


@timeit
@rename('employment_stats')
def stats():
    # init
    data_df = etl.extract(Employment.FIGURES + '/employment_full.csv', Data.HEADER, Data.TYPES)
    
    # Milbert - employment score
    stats_df = basic_stats(data_df)
    stats_df = change_types(stats_df, Employment.TYPES)
    etl.load(stats_df, Employment.FIGURES + '/employment_stats.csv', ff='%.16f')
    
    quantile_df = quantile_score(stats_df, 'gmean')
    quantile_df = adjust_score(quantile_df, 'gmean', 2, 0)
    quantile_df = change_types(quantile_df, Employment.TYPES)
    etl.load(quantile_df, Employment.FIGURES + '/employment_score.csv', ff='%.16f')

