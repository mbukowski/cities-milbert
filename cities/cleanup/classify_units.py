import pandas as pd
import re
import common

from pandas import DataFrame

'''
Enrich units with teryt_id and divide them to 2 separate files
- [full] all municipalities: level 6 and kind 1, 2 or 3
- [basic] city municipalities: level 6 and kind 1 or 3
- [city] only cities: level 6 and kind 1 or 4

Based on taken approach we may have different results for quantile distribution
'''

input_header = ['id', 'parent_id', 'name', 'level', 'kind', 'has_description', 'description', 'years']
input_types = { 'id': str, 'parent_id': str, 'level': 'Int64', 'kind': 'Int64' }
unify_header = ['from', 'to', 'mode', 'name', 'description']
unify_types = { 'from': str, 'to': str }
output_header = ['id', 'parent_id', 'teryt_id', 'name', 'level', 'kind']

input_path = './data/dict/units.csv'
output_folder = './figures/units'


def extract(path: str) -> DataFrame:
    df = common.extract(path, input_header, input_types)

    return df

def transform(df: DataFrame) -> DataFrame:
    df['teryt_id'] = df['id'].str[2:4] + df['id'].str[7:12]
    df['name'] = df.apply(lambda row: unit_name(row['name']), axis=1)

    df1 = common.extract('./data/conf/unify.csv', unify_header, unify_types)
    delete_list = df1['from'].loc[df1['mode'] == 9].values.tolist()
    df = df.loc[~df['id'].isin(delete_list)]

    return df

def unit_name(name: str) -> str:
    res = name
    res = re.sub(' - miasto.*', '', res)
    res = re.sub(' od.*', '', res)
    res = re.sub(' do.*', '', res)

    return res

def load(df: DataFrame, path: str):
    load_category(df, path, 'full', 6, [1, 2, 3])
    load_category(df, path, 'basic', 6, [1, 3])
    load_category(df, path, 'city', 6, [1, 4])

def load_category(df: DataFrame, path: str, name: str, level: int, kind: list[int]):
    output_path = f'{path}/units_{name}.csv'

    df = df.loc[(df['level'] == level) & (df['kind'].isin(kind))]
    df = df[output_header]
    common.load(df, output_path)
  
def main():
    df = extract(input_path)
    df = transform(df)
    load(df, output_folder)
