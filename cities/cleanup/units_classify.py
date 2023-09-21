import common.etl as etl

from pandas import DataFrame
from common.globals import Units, Unify, UnitsData
from common.data_frame import unit_name


'''
Enrich units with teryt_id and divide them to 2 separate files
- [full] all municipalities: level 6 and kind 1, 2 or 3
- [basic] city municipalities: level 6 and kind 1 or 3
- [city] only cities: level 6 and kind 1 or 4

Based on taken approach we may have different results for quantile distribution
'''


def transform(df: DataFrame) -> DataFrame:
    df['teryt_id'] = df['unit_id'].str[2:4] + df['unit_id'].str[7:12]
    df['name'] = df.apply(lambda row: unit_name(row['name']), axis=1)

    unify_df = etl.extract(Unify.DATA, Unify.HEADER, Unify.TYPES)
    delete_list = unify_df['from'].loc[unify_df['mode'] == 9].values.tolist()
    df = df.loc[~df['unit_id'].isin(delete_list)]

    return df

def load(df: DataFrame, path: str, level: int, kind: list[int]):
    df = df.loc[(df['level'] == level) & (df['kind'].isin(kind))]
    df = df[Units.HEADER]

    etl.load(df, path)
  
def main():
    # extract
    df = etl.extract(UnitsData.DATA, UnitsData.HEADER, UnitsData.TYPES)

    # transform
    df = transform(df)

    # load
    # load(df, Units.COMMUNE_DATA, 6, [1, 2, 3])
    # load(df, Units.BASIC_DATA, 6, [1, 3])
    # load(df, Units.CITY_DATA, 6, [1, 4])
    load(df, Units.COMPLETE_DATA, 6, [1, 2, 3, 4, 5])
