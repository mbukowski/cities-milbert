import pandas as pd
import common

from pandas import DataFrame

'''
We find out which units have to be transformed in order to fill the gaps

During the lifecycle of the municipality various events might have occured. This information is encompassed in description field.
Idea behind unification is that we keep data accross all periods and we can compare values. If it wac a simple name or type change, 
it should be quite straight forward. Problems may occur with dividing a municipality to urban-rural with two respective parts.
- type change: from rural to urban-rural, ...
- move between counties,
- name change,
- dissolving,
- combining,

Data were collected, processed and stored in data/conf/unify.csv. During the process we identified 3 situations:
1 - replace an old id with a new one,
2 - combine values for both ids in given time gap
9 - remove given entries
'''

header = ['id', 'parent_id', 'name', 'level', 'kind', 'has_description', 'description', 'years']
types = { 'id': str, 'parent_id': str, 'level': 'Int64', 'kind': 'Int64' }

input_path = './data/dict/units.csv'
output_folder = './figures/unify_units_xxx'

def extract(path: str) -> DataFrame:
    df =  common.extract(path, header, types)

    return df

def transform(df: DataFrame) -> DataFrame:
    df = df.loc[df['has_description'] == True].copy()
    df['description'] = df['description'].str.lower()

    return df

def load(df: DataFrame, path: str):
    load_step(df, path, '00')
    
    df = load_step_desc(df, path, 'zmiana rodzaju gminy z wiejskiego na miejsko-wiejski', '01')
    df = load_step_desc(df, path, 'zmiana przynależności gminy z powiatu', '02')
    df = load_step_desc(df, path, 'zmiana nazwy gminy', '03')
    df = load_step_desc(df, path, 'zmiana rodzaju gminy z miejskiego na miejsko-wiejski', '04')
    df = load_step_desc(df, path, 'zmiana granic', '05')
    df = load_step_desc(df, path, 'utworzenie gminy', '06')
    df = load_step_desc(df, path, 'przeniesienie gminy z powiatu', '07')
    df = load_step_desc(df, path, 'zmiana symbolu gminy', '08')
    df = load_step_desc(df, path, 'zniesienie gminy', '09')
    df = load_step_desc(df, path, 'utworzenie dzielnicy', '10')
    
    load_step(df, path, '11')

def load_step_desc(df: DataFrame, path: str, description: str, step: str) -> DataFrame:
    df1 = df.loc[df['description'].str.contains(description)]
    df = df.loc[~df['description'].str.contains(description)]
    load_step(df1, path, step)

    return df

def load_step(df: DataFrame, path: str, step: str):
    output_path = f'{path}/unify_units_{step}.csv'
    
    common.load(df, output_path)
  
def main():
    df = extract(input_path)
    df = transform(df)
    load(df, output_folder)
