import pandas as pd
import numpy as np
import common.etl as etl
import common.globals as g

from pandas import DataFrame
from common.utils import timeit, rename
from common.data_frame import change_types, city_type, city_status, growth_type


'''
Basic transformations for cities
'''

'''
Retrieve commune population
- in case urban 6,1 return val
- in case rural 6,2 return val
- in case urban-rural 6,3 return a city size in this commune
- in case 6,4 or 6,5 skip 
'''
@timeit
@rename('city_size')
def size():
    complete_df = etl.extract(g.Units.COMPLETE_DATA, g.Units.HEADER, g.Units.TYPES)
    population_df = pd.read_csv(g.Population.FIGURES + '/population_unify.csv', sep=',', header=0, dtype={'unit_id': str})

    df = pd.merge(complete_df, population_df[['unit_id', 'year', 'val']], on=['unit_id'])
    etl.load(df, g.City.FIGURES + '/units_population.csv')

    city_df = df.loc[(df['level'] == 6) & (df['kind'] == 4)]
    df = df.loc[(df['level'] == 6) & (df['kind'].isin([1, 2, 3]))]

    df = pd.merge(df, city_df[['parent_id', 'year', 'val']], 
                  how='left', left_on=['unit_id', 'year'], right_on=['parent_id', 'year'], 
                  suffixes=('', '_city')).fillna(0)
    df = df.astype({'val_city': int})
    etl.load(df, g.City.FIGURES + '/mapping_population.csv')

    df.loc[(df['level'] == 6) & (df['kind'] == 3), 'val'] = 0
    df['val'] = df['val'] + df['val_city']
    df.drop(columns=['val_city', 'parent_id_city'], axis=1, inplace=True)
    etl.load(df, g.City.FIGURES + '/city_population.csv')


'''
Converts data to qgis input
'''
@timeit
@rename('gqis_input')
def qgis():
    df = pd.read_csv(g.Stats.FIGURES + '/summary.csv', sep=',', header=0, dtype={'unit_id': str, 'teryt_id': str})
    df = df[g.City.QGIS_HEADER]
    print(df.dtypes)
    etl.load(df, g.City.FIGURES + '/qgis_data.csv')


def get_last_type(group):
    last_index = group['period_end'].idxmax()
    return group.loc[last_index, 'type']


'''
Finds the trend of the growt / shrinkage
'''
@timeit
@rename('cities_trend')
def trend():
    df = pd.read_csv(g.Stats.FIGURES + '/summary.csv', sep=',', header=0, dtype={'unit_id': str, 'teryt_id': str})
    df = df.loc[df['period_start'].isin([2006, 2011, 2016])]
    df = df.loc[df['population_start'] > 0]

    # when we group here we can add type but we won't be able to get last possible type
    # TODO that should be cleaned up later once we have a better method and some code refactored
    # for a moment that's a manual job to clean up
    df = df.groupby(['unit_id', 'teryt_id', 'name', 'level', 'kind']).agg({'status': ''.join}).reset_index()

    df = df.loc[(df['level'] == 6) & (df['kind'].isin([1, 3]))]
    df['strong_growth'] = df.apply(lambda row: growth_type(row['status'], g.GrowthStrategy.STRONG_TREND), axis=1)
    df['normal_growth'] = df.apply(lambda row: growth_type(row['status'], g.GrowthStrategy.NORMAL_TREND), axis=1)
    df['weak_growth'] = df.apply(lambda row: growth_type(row['status'], g.GrowthStrategy.WEAK_TREND), axis=1)

    df = df.loc[df['weak_growth'] != '']

    etl.load(df, g.City.FIGURES + '/cities_trend.csv')
