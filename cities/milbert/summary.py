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
    basic_df = etl.extract(g.Units.BASIC_DATA, g.Units.HEADER, g.Units.TYPES)
    population_df = pd.read_csv(g.Population.FIGURES + '/population_basic.csv', sep=',', header=0, dtype={'unit_id': str})

    pop_df = pd.read_csv(g.Population.FIGURES + '/population_score.csv', sep=',', header=0, dtype={'unit_id': str})
    migr_df = pd.read_csv(g.Migration.FIGURES + '/migration_score.csv', sep=',', header=0, dtype={'unit_id': str})
    age_df = pd.read_csv(g.WorkingAge.FIGURES + '/working_age_score.csv', sep=',', header=0, dtype={'unit_id': str})
    empl_df = pd.read_csv(g.Employment.FIGURES + '/employment_score.csv', sep=',', header=0, dtype={'unit_id': str})
    # unempl_df = pd.read_csv(g.Unemployed.FIGURES + '/unemployed_type_score.csv', sep=',', header=0, dtype={'unit_id': str})
    unempl_df = pd.read_csv(g.Unemployed.FIGURES + '/unemployed_unempl_score.csv', sep=',', header=0, dtype={'unit_id': str})
    revenue_df = pd.read_csv(g.OwnRevenue.FIGURES + '/own_revenue_score.csv', sep=',', header=0, dtype={'unit_id': str})

    # first we set a copy and merge with population data
    df = basic_df.copy()
    df = pd.merge(df, population_df[['unit_id', 'year', 'val']], on=['unit_id'])
    df.rename(columns={'val': 'population'}, inplace=True)

    # merge with population score
    df = pd.merge(df, pop_df[['unit_id', 'year', 'adj_score']], on=['unit_id', 'year'])
    df.rename(columns={'adj_score': 'pop'}, inplace=True)

    # merge with migration score
    df = pd.merge(df, migr_df[['unit_id', 'year', 'adj_score']], on=['unit_id', 'year'])
    df.rename(columns={'adj_score': 'migr'}, inplace=True)

    # merge with working_age score
    df = pd.merge(df, age_df[['unit_id', 'year', 'adj_score']], on=['unit_id', 'year'])
    df.rename(columns={'adj_score': 'age'}, inplace=True)

    # merge with employment score
    df = pd.merge(df, empl_df[['unit_id', 'year', 'adj_score']], on=['unit_id', 'year'])
    df.rename(columns={'adj_score': 'empl'}, inplace=True)

    # merge with unemployed score
    df = pd.merge(df, unempl_df[['unit_id', 'year', 'adj_score']], on=['unit_id', 'year'])
    df.rename(columns={'adj_score': 'unempl'}, inplace=True)

    # merge with own revenue score
    df = pd.merge(df, revenue_df[['unit_id', 'year', 'adj_score']], on=['unit_id', 'year'])
    df.rename(columns={'adj_score': 'revenue'}, inplace=True)

    df.rename(columns={'year': 'period_end'}, inplace=True)
    df['period_start'] = df['period_end'] - 5


    # add calculated columns to the dataframe
    df['score'] = df['pop'] + df['migr'] + df['age'] + df['empl'] + df['unempl'] + df['revenue']
    df['type'] = df.apply(lambda row: city_type(row['population']), axis=1)
    df['status'] = df.apply(lambda row: city_status(row['score']), axis=1)

    df = df[g.Stats.HEADER]
    # df = df[g.Stats.HEADER]

    # print(pop_df.dtypes)
    print(df.dtypes)

    # df = change_types(df, g.Stats.TYPES)
    etl.load(df, g.Stats.FIGURES + '/summary.csv')


    # wielkosc miasta a nie gminy
    # poczatek okresu 
    # bez 5% zakladki
