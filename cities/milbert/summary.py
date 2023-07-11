import pandas as pd
import numpy as np
import common.etl as etl
import common.globals as g

from pandas import DataFrame
from common.data_frame import filter_by_var, filter_by_id, unify
from common.stats import basic_stats, quantile_score, adjust_score
from common.utils import timeit, rename
from common.data_frame import change_types, city_type, city_status


'''
Collects statistics for milbert methodology, with main sources for 5 parameters and city type as a bucket used for 
unemployed parameter.
'''
@timeit
@rename('summary_default')
def default():
    # init
    df = etl.extract(g.Units.FULL_DATA, g.Units.HEADER, g.Units.TYPES)
    city_population_df = pd.read_csv(g.City.FIGURES + '/city_population.csv', sep=',', header=0, dtype={'unit_id': str})    

    # period start and period end years and values
    df = pd.merge(df, city_population_df[['unit_id', 'year', 'val']], on=['unit_id'])
    df.rename(columns={'year': 'period_end', 'val': 'population_end'}, inplace=True)

    df['period_start'] = df['period_end'] - 5
    # df = df.astype({'period_start': int, 'period_end': int})

    df = pd.merge(df, city_population_df[['unit_id', 'year', 'val']], 
                  how='left', left_on=['unit_id', 'period_start'], right_on=['unit_id', 'year'])
    df.rename(columns={'val': 'population_start'}, inplace=True)

    pop_df = pd.read_csv(g.Population.FIGURES + '/population_score.csv', sep=',', header=0, dtype={'unit_id': str})
    migr_df = pd.read_csv(g.Migration.FIGURES + '/migration_score.csv', sep=',', header=0, dtype={'unit_id': str})
    age_df = pd.read_csv(g.WorkingAge.FIGURES + '/working_age_score.csv', sep=',', header=0, dtype={'unit_id': str})
    empl_df = pd.read_csv(g.Employment.FIGURES + '/employment_score.csv', sep=',', header=0, dtype={'unit_id': str})
    unempl_df = pd.read_csv(g.Unemployed.FIGURES + '/unemployed_distr_score.csv', sep=',', header=0, dtype={'unit_id': str})
    revenue_df = pd.read_csv(g.OwnRevenue.FIGURES + '/own_revenue_score.csv', sep=',', header=0, dtype={'unit_id': str})

    # only for merging
    df['year'] = df['period_end']

    # score and statistics are always calculated for perido end
    # merge with population score
    df = pd.merge(df, pop_df[['unit_id', 'year', 'gmean', 'adj_score']], on=['unit_id', 'year'])
    df.rename(columns={'adj_score': 'pop_points', 'gmean': 'pop_rate'}, inplace=True)

    # merge with migration score
    df = pd.merge(df, migr_df[['unit_id', 'year', 'sum', 'adj_score']], on=['unit_id', 'year'])
    df.rename(columns={'adj_score': 'migr_points', 'sum': 'migr_rate'}, inplace=True)

    # merge with working_age score
    df = pd.merge(df, age_df[['unit_id', 'year', 'gmean', 'adj_score']], on=['unit_id', 'year'])
    df.rename(columns={'adj_score': 'age_points', 'gmean': 'age_rate'}, inplace=True)

    # merge with employment score
    df = pd.merge(df, empl_df[['unit_id', 'year', 'gmean', 'adj_score']], on=['unit_id', 'year'])
    df.rename(columns={'adj_score': 'empl_points', 'gmean': 'empl_rate'}, inplace=True)

    # merge with unemployed score
    df = pd.merge(df, unempl_df[['unit_id', 'year', 'gmean', 'adj_score']], on=['unit_id', 'year'])
    df.rename(columns={'adj_score': 'unempl_points', 'gmean': 'unempl_rate'}, inplace=True)

    # merge with own revenue score
    df = pd.merge(df, revenue_df[['unit_id', 'year', 'gmean', 'adj_score']], on=['unit_id', 'year'])
    df.rename(columns={'adj_score': 'revenue_points', 'gmean': 'revenue_rate'}, inplace=True)

    # add calculated columns to the dataframe
    df['score'] = df.loc[:, df.columns.str.endswith('_points')].sum(axis = 1)
    df['type'] = df.apply(lambda row: city_type(row['population_start'], row['unit_id']), axis=1)
    df['status'] = df.apply(lambda row: city_status(row['score']), axis=1)

    df = df.astype({'population_start': int, 'population_end': int})
    df = df[g.Stats.HEADER]

    # print(df.dtypes)

    # df = change_types(df, g.Stats.TYPES)
    etl.load(df, g.Stats.FIGURES + '/summary.csv', ff='%.4f')
