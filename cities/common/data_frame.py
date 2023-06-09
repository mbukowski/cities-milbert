import re
import pandas as pd

from pandas import DataFrame
from common.globals import City, Unemployed

def unit_name(name: str) -> str:
    res = name
    res = re.sub(' - miasto.*', '', res)
    res = re.sub(' od.*', '', res)
    res = re.sub(' do.*', '', res)

    return res

'''
Identifies a city type based on a population size
'''
def city_type(size: int, unit_id: str) -> str:
    # TODO this should come from parameter 'kind' but we don't have this information in dataframe with compiled data
    if unit_id.endswith('2'): return City.RURAL['id']

    medium_min = City.MEDIUM['min_size'] * (1 - City.SIZE_MARGIN)
    medium_max = City.MEDIUM['max_size'] * (1 + City.SIZE_MARGIN)

    if size < medium_min: return City.SMALL['id']
    if size > medium_max: return City.LARGE['id']

    return City.MEDIUM['id']


# @obsolete
# '''
# Calculates a city size for a city within an urban-rural commune for given year
# '''
# def city_size(df: DataFrame, unit_id: str, year: int) -> int:
#     print(f'{unit_id} -> {year}')
#     # default - no matching row
#     v = -1

#     v_series = df.loc[(df['parent_id'] == unit_id) & (df['year'] == year) & (df['kind'] == 4)]['val']
    
#     if not v_series.empty:
#         v = v_series.values[0]
#         if pd.isnull(v):
#             v = 0

#     print(v)

#     return v


'''
Returns a city status based on collected score for Milbert methodology
- significantly shrinking
- shrinking
- stabilization
- growin
- significantly growing
'''
def city_status(score: int) -> str:
    if score <= 6: return 'E'
    elif score <= 10: return 'D'
    elif score <= 13: return 'C'
    elif score <= 18: return 'B'
    elif score <= 24: return 'A'
    else: return 'Z'


'''
Returns a growth type based on 3 periods.
- all A or 2xA and 1xB strong growth -> AA
- all E or 2xE and 1xD strong shrinkage -> EE
- all C or 2xC and 1xB or 1xD strong stable -> CC
- from E to A or B, positive change -> EA
- from A to E or D, negative change -> AE
'''
def growth_type(status: str, strategy) -> str:
    if status in strategy:
        return strategy[status]

    return ''
    # match status:
    #     # case 'AAA' | 'BAA' | 'ABA' | 'AAB':
    #     case 'AAA':
    #         return 'AA'
    #     # case 'EEE' | 'DEE' | 'EDE' | 'EED':
    #     case 'EEE':
    #         return 'EE'
    #     # case 'CCC' | 'BCC' | 'CBC' | 'CCB' | 'DCC' | 'CDC' | 'CCD':
    #     case 'CCC':
    #         return 'CC'
    #     case 'EEA' | 'EEB':
    #     # case 'EEA' | 'EEB' | 'EDA' | 'DEA' | 'DDA':
    #     # case 'EEA' | 'EEB' | 'EDA' | 'DEA' | 'DDA' | 'EDB' | 'DEB' | 'DDB':
    #         return 'EA'
    #     case 'AAD' | 'AAE':
    #     # case 'AAD' | 'AAE' | 'BAE' | 'ABE' | 'BBE':
    #     # case 'AAD' | 'AAE' | 'BAE' | 'ABE' | 'BBE' | 'BAD' | 'ABD' | 'BBD':
    #         return 'AE'
    #     case _:
    #         return ''

'''
Identifies a group to which unemployment rate should belong. 
Don't know if we still use this probably not. Verify before removing.
'''
def unemp_rate(rate: float) -> str:
    for r in Unemployed.RATE:
        if rate <= r[0]: return r[1]
    
    return 'Z'


'''
Filters all data based on a given variable id, specific to our research
'''
def filter_by_var(data_df: DataFrame, var_id: int) -> DataFrame:
    df = data_df[data_df['var_id'] == var_id].copy()
    df.reset_index(drop=True, inplace=True)

    return df

'''
Filters all data based on a given level
'''
def filter_by_level(data_df: DataFrame, units_df: DataFrame, level: int) -> DataFrame:
    df = units_df.loc[units_df['level'] == level]
    id_list = df['unit_id'].values.tolist()

    df = filter_by_id(data_df, id_list)

    return df

'''
Filters all data based on a given level and kind list
'''
def filter_by_level_kind(data_df: DataFrame, units_df: DataFrame, level: int, kind:list[int]) -> DataFrame:
    df = units_df.loc[(units_df['level'] == level) & (units_df['kind'].isin(kind))]
    id_list = df['unit_id'].values.tolist()
    
    df = filter_by_id(data_df, id_list)

    return df

'''
Filters all data by unit_ids
'''
def filter_by_id(data_df: DataFrame, id_list: list[str]) -> DataFrame:
    df = data_df.loc[data_df['unit_id'].isin(id_list)].copy()
    
    return df

'''
Change column types based on a given dict
Cast a pandas object to a specified dtype
'''
def change_types(df: DataFrame, types: dict[str, str]) -> DataFrame:
    for col in df.columns:
        df = df.astype({col: types[col]})

    return df

'''
1 - replace
2 - merge
9 - delete
'''
def unify(data_df: DataFrame, conf_df: DataFrame) -> DataFrame:
    # replace - narrow a df to a smaller piece and operate on it
    id_list = conf_df.loc[conf_df['mode'] == 1]['from'].values.tolist()
    df = filter_by_id(data_df, id_list)

    # replace 
    df['unit_id'] = df.apply(lambda row: replace(row['unit_id'], conf_df), axis=1)
    data_df.loc[df.index, 'unit_id'] = df['unit_id']
    data_df.reset_index(drop=True, inplace=True)

    # merge - narrow a df to a smaller piece starting based on to
    id_list = conf_df.loc[conf_df['mode'] == 2]['to'].values.tolist()
    df = filter_by_id(data_df, id_list)
    
    # merge
    df['val'] = df.apply(lambda row: merge(row['unit_id'], row['year'], data_df, conf_df), axis=1)
    data_df.loc[df.index, 'val'] = df['val']
    data_df.reset_index(drop=True, inplace=True)

    # # remove
    id_list = conf_df.loc[conf_df['mode'] == 9]['from'].values.tolist()    
    data_df = data_df.loc[~data_df['unit_id'].isin(id_list)].copy()

    data_df.sort_values(['unit_id', 'year'], inplace=True)
    data_df.reset_index(drop=True, inplace=True)

    return data_df

# conf_row is never empty because we prefiltered it upfront
def replace(unit_id: str, conf_df: DataFrame) -> str:
    conf_row = conf_df.loc[conf_df['from'] == unit_id]

    return conf_row.iloc[0]['to']

def merge(unit_id: str, year: int, data_df: DataFrame, conf_df: DataFrame) -> int:
    conf_row = conf_df.loc[conf_df['to'] == unit_id]
    from_id = conf_row.iloc[0]['from']

    val = data_df.loc[(data_df['unit_id'] == unit_id) & (data_df['year'] == year)]['val'].iloc[0]
    cell = data_df.loc[(data_df['unit_id'] == from_id) & (data_df['year'] == year)]
    if not cell.empty:
        val_from = cell['val'].iloc[0]
        val += val_from

    return val
