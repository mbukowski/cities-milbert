import pandas as pd
import numpy as np
import common.etl as etl

from pandas import DataFrame
from common.globals import Data, Units, Unify, Population
from common.data_frame import filter_by_var, filter_by_id, unify
from common.stats import simple_stats, quantile_stats, period_stats, cires_stats
from common.utils import timeit, rename


'''
We load population data, we count the change between each year. 
We process the average for 5 years period, which will be used for identifing shrinking cities: 
- according to classic definition CIRES - in this definition we could work with units_city dataset
- aligned with Milbert methodology where de assign points based on quantiles

Preprocessing
- filter data based on variable
- unify data valuse based on configuration

After calculation we don't have full details for following municipalities. 
- 012414513031 - Radzionków
- 012414915021 - Radlin

Both of them were created after 1995, thus 5-years periods starts counting from later period. 
It doesn't affect our further experiments.
'''


@timeit
@rename('population_prep')
def prep():
    pre_loaded = False

    # init
    basic_df = etl.extract(Units.BASIC_DATA, Units.HEADER, Units.TYPES)
    conf_df = etl.extract(Unify.DATA, Unify.HEADER, Unify.TYPES)

    if pre_loaded:
        # direct reading from population_raw
        data_df = etl.extract(Population.FIGURES + '/population_raw.csv', Data.HEADER, Data.TYPES)

    else:
        # read from main source
        data_df = etl.extract(Population.DATA, Data.HEADER, Data.TYPES)

        # filtered out data based on variable, save for reference
        data_df = filter_by_var(data_df, Population.VAR_ID)
        etl.load(data_df, Population.FIGURES + '/population_raw.csv')

    # unify data: replace, merge, remove
    data_df = unify(data_df, conf_df)
    etl.load(data_df, Population.FIGURES + '/population_unify.csv')

    # leave only units from specific data source, in our case crosscheck with basic_df
    id_list = basic_df['unit_id'].values.tolist()
    data_df = filter_by_id(data_df, id_list)
    etl.load(data_df, Population.FIGURES + '/population_prep.csv')


@timeit
@rename('population_stats')
def stats():
    # init
    data_df = etl.extract(Population.FIGURES + '/population_prep.csv', Data.HEADER, Data.TYPES)
    basic_df = etl.extract(Units.BASIC_DATA, Units.HEADER, Units.TYPES)

    # Milbert Parameter - population score
    stats_df = simple_stats(data_df)
    etl.load(stats_df, Population.FIGURES + '/population_stats.csv', ff='%.16f')
    
    quantile_df = quantile_stats(stats_df)
    etl.load(quantile_df, Population.FIGURES + '/population_score.csv', ff='%.16f')

    # CIRES Parameter - special case only for population distribution
    cires_df = period_stats(stats_df)
    etl.load(cires_df, Population.FIGURES + '/population_cires_stats.csv', ff='%.16f')

    cires_df = cires_stats(cires_df)
    etl.load(cires_df, Population.FIGURES + '/population_cires_score.csv', ff='%.16f')

