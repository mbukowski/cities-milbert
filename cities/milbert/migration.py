import pandas as pd
import numpy as np
import common.etl as etl

from pandas import DataFrame
from common.globals import Data, Units, Unify, Migration, Population
from common.data_frame import filter_by_var, filter_by_id, unify
from common.stats import rate_sum_stats, quantile_score, adjust_score
from common.utils import timeit, rename
from common.data_frame import change_types


'''
Durchschnittliches jährliches Gesamtwanderungssaldo 2014 bis 2018 je 1000 Einwohner

For migration we process a saldo per 1000 inhabitants. This suggests that we have to combine it with population data, 
for specific year. After that in the 5-year period we sum this migration saldo. 

We process the sum for 5 years period, which will be used for identifing shrinking cities: 
- aligned with Milbert methodology where we assign points based on quantiles

Preprocessing
- filter data based on variable
- unify data valuse based on configuration

Like with own revenue and employment rate a border for adjusted score is 3rd quantile, 
which means every value above 0 gets at least 2 score points.
'''


@timeit
@rename('migration_prep')
def prep():
    pre_loaded = False

    # init
    basic_df = etl.extract(Units.BASIC_DATA, Units.HEADER, Units.TYPES)
    conf_df = etl.extract(Unify.DATA, Unify.HEADER, Unify.TYPES)
    
    if pre_loaded:
        # direct reading from migration_raw
        data_df = etl.extract(Migration.FIGURES + '/migration_raw.csv', Data.HEADER, Data.TYPES)
        data_df['val'] = data_df['val'].astype(np.int64)

    else:
        # read from main source
        data_df = etl.extract(Migration.DATA, Data.HEADER, Data.TYPES)
        data_df['val'] = data_df['val'].astype(np.int64)

        # filtered out data based on variable, save for reference
        data_df = filter_by_var(data_df, Migration.VAR_ID)
        etl.load(data_df, Migration.FIGURES + '/migration_raw.csv')

    # unify data: replace, merge, remove
    data_df = unify(data_df, conf_df)
    etl.load(data_df, Migration.FIGURES + '/migration_unify.csv')

    # leave only units from specific data source, in our case crosscheck with basic_df
    id_list = basic_df['unit_id'].values.tolist()
    data_df = filter_by_id(data_df, id_list)
    etl.load(data_df, Migration.FIGURES + '/migration_basic.csv')


@timeit
@rename('migraton_stats')
def stats():
    # init
    data_df = etl.extract(Migration.FIGURES + '/migration_basic.csv', Data.HEADER, Data.TYPES)
    population_df = etl.extract(Population.FIGURES + '/population_raw.csv', Data.HEADER, Data.TYPES)

    # merge migration with population
    data_df = pd.merge(data_df, population_df[['unit_id', 'year', 'val']], on=['unit_id', 'year'], suffixes=('', '_population'))
    data_df.rename(columns={'val_population': 'population'}, inplace=True)
    data_df['rate'] = data_df['val'] / (0.001 * data_df['population'])
    data_df = change_types(data_df, Migration.TYPES)
    etl.load(data_df, Migration.FIGURES + '/migration_saldo.csv')

    # Milbert - migrtion score
    stats_df = rate_sum_stats(data_df)
    stats_df = change_types(stats_df, Migration.TYPES)
    etl.load(stats_df, Migration.FIGURES + '/migration_stats.csv', ff='%.16f')
    
    quantile_df = quantile_score(stats_df, 'sum')
    quantile_df = adjust_score(quantile_df, 'sum', 2, 0)
    quantile_df = change_types(quantile_df, Migration.TYPES)
    etl.load(quantile_df, Migration.FIGURES + '/migration_score.csv', ff='%.16f')
