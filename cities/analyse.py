import pandas as pd

from pathlib import Path

from common.data_frame import city_type

CLC_YEARS = [2006, 2012, 2018]

'''
a script to combine both compactness and shrinking data
'''
def main():
    path = Path('./data/processed/analyse', 'analyse.csv')

    header_types = {
        'unit_id': str,
        'teryt_id': str,
        'period_start': int, 
        'period_end': int,
        'population_start': int,
        'population_end': int,
        'score': int
        # 'period_start': 'Int64', 
        # 'period_end': 'Int64',
        # 'population_start': 'Int64',
        # 'population_end': 'Int64',
        # 'score': 'Int64'
    }

    output_header = ['unit_id', 'teryt_id', 'name', 
                     'period_start', 'period_end', 'population_start', 'population_end', 'score', 'status', 
                     'year', 'population', 'type', 'group', 'base_area', 'density', 'schwartzberg', 'polsby_popper', 'reock', 'box', 'rectangle', 'convex_hull', 
                     ]

    df = pd.read_csv('./data/processed/qgis/compactness.csv', sep=',', decimal='.', dtype=header_types)

    df1 = pd.read_csv('./data/processed/parameters/population/population_full.csv', sep=',', decimal='.', dtype=header_types)
    df = pd.merge(df, df1[['unit_id', 'year', 'val']], how='left', left_on=['unit_id', 'year'], right_on=['unit_id', 'year'])
    df = df.dropna()
    df.rename(columns={'val': 'population'}, inplace=True)
    # df = df.astype({'population': 'Int64'})
    df = df.astype({'population': int})

    df['type'] = df.apply(lambda row: city_type(row['population'], row['unit_id']), axis=1)
    df['density'] = df['population'] / df['base_area'] * 1000000

    df2 = pd.read_csv('./data/processed/stats/summary.csv', sep=',', decimal='.', dtype=header_types)
    # df2 = df2.loc[df2['period_start'].isin([2006, 2011, 2016])]
    # df2.reset_index(inplace=True)
    df2['year'] = df2.apply(lambda row: map_period_to_year(row['period_start']), axis=1)

    df = pd.merge(df, df2[['unit_id', 'year', 'period_start', 'period_end', 'population_start', 'population_end', 'score', 'status']], how='left', left_on=['unit_id', 'year'], right_on=['unit_id', 'year'])
    # df = df.fillna(0)
    df = df.dropna()

    df.sort_values(['unit_id', 'group', 'year'], inplace=True)
    df = df[output_header]
    print(df.dtypes)

    # TODO - Wiskitki stay with no values for all periods, something didn't properly calculated in city.size()

    df.to_csv(path.resolve(), float_format='%.6f', index=False)

'''
simple function to map year to the perod
'''
def map_period_to_year(period_start: int) -> int:
    for year in CLC_YEARS:
        if period_start <= year: return year

    return 0

if __name__ == '__main__':
    main()


