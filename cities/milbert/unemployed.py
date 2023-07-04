import pandas as pd
import numpy as np
import common.etl as etl

from pandas import DataFrame
from common.globals import Data, Units, Unify, Unemployed, Population
from common.data_frame import filter_by_var, filter_by_id, unify
from common.stats import basic_stats, quantile_score_ext, adjust_score, rate_gmean_stats
from common.utils import timeit, rename
from common.data_frame import change_types, city_type, unemp_rate

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

'''
Durchschnittliche jährliche Veränderung der Arbeitslosenquote 2012/13 bis 2017/18 in %-
Punkten

According to a methodology we should distribute cities to various buckets based on some factor. Most important reason, 
is that we compare %-points and not %-change. Also cities with small unemployment rate would be in disadvantage.
- First one which comes to my mind is simply city size status: large, medium or small. With that we can simply divide 
all cities based on a value and we have constant sets, but actually we should look also on yearly basis. 
- Second approach would be to divide them on initial unemployment ratio. It's much harder to go down from 1%,
 than from 5%. For that we should first observe how does a distribution look like and then us some parameters to divide.
- Third possible could be to divide cities based on a total value of unemployed, 
but that doesn't take under consideration city size, which also is a big factor.

We load umeploymend data, and we count the change between each year in %-points. 
Unemployed data are the most specific ones and require a special attention.

We process the average for 5 years period, which will be used for identifing shrinking cities: 
- aligned with Milbert methodology where we assign points based on quantiles

Preprocessing
- filter data based on variable
- unify data valuse based on configuration
- keep in mind we need to reverse quantile calculation as the lower value of unemployment rate,
 is a better indicator than a higher one

There are no gaps for communes on level 6,1 and 6,3. But when we would like to focus on unemployed data only for cities, 
this becomes more complicated. For 6,1 and 6,4 we have 9566 / 17236 entries with value 0 which makes interpolation 
even more problematic.

Because unemployment ratio is little different and we are having a reveted quantiles here. Every value with positive, 
influx of unemployed people will be 'awarded' with 0 points. 0 is the border of the 1st quantile.
'''


@timeit
@rename('umemployed_prep')
def prep():
    pre_loaded = False

    # init
    basic_df = etl.extract(Units.BASIC_DATA, Units.HEADER, Units.TYPES)
    conf_df = etl.extract(Unify.DATA, Unify.HEADER, Unify.TYPES)

    if pre_loaded:
        # direct reading from working_age_raw
        data_df = etl.extract(Unemployed.FIGURES + '/unemployed_raw.csv', Data.HEADER, Data.TYPES)
        data_df['val'] = data_df['val'].astype(np.int64)

    else:
        # read from main source
        data_df = etl.extract(Unemployed.DATA, Data.HEADER, Data.TYPES)
        data_df['val'] = data_df['val'].astype(np.int64)

        # filtered out data based on variable, save for reference
        data_df = filter_by_var(data_df, Unemployed.VAR_ID)
        etl.load(data_df, Unemployed.FIGURES + '/unemployed_raw.csv')

    # unify data: replace, merge, remove
    data_df = unify(data_df, conf_df)
    etl.load(data_df, Unemployed.FIGURES + '/unemployed_unify.csv')

    # leave only units from specific data source, in our case crosscheck with basic_df
    # here we could compare values for basic and city mapping
    id_list = basic_df['unit_id'].values.tolist()
    data_df = filter_by_id(data_df, id_list)
    etl.load(data_df, Unemployed.FIGURES + '/unemployed_basic.csv')


'''
We measure unemployed score based on the dividing stats to a city type bucket:
- large
- medium 
- small 
'''
@timeit
@rename('umemployed_stats_type')
def stats_type():
    # init
    data_df = etl.extract(Unemployed.FIGURES + '/unemployed_basic.csv', Data.HEADER, Data.TYPES)
    population_df = etl.extract(Population.FIGURES + '/population_raw.csv', Data.HEADER, Data.TYPES)

    # merge unemployed with population and set the city type
    data_df = pd.merge(data_df, population_df[['unit_id', 'year', 'val']], on=['unit_id', 'year'], suffixes=('', '_population'))
    data_df.rename(columns={'val_population': 'population'}, inplace=True)
    data_df['type'] = data_df.apply(lambda row: city_type(row['population']), axis=1)
    data_df['rate'] = data_df['val'] / data_df['population']
    data_df = change_types(data_df, Unemployed.TYPES)
    etl.load(data_df, Unemployed.FIGURES + '/unemployed_type_rate.csv', ff='%.16f')
    
    # Milbert - unemployed score
    stats_df = rate_gmean_stats(data_df)
    stats_df = change_types(stats_df, Unemployed.TYPES)
    etl.load(stats_df, Unemployed.FIGURES + '/unemployed_type_stats.csv', ff='%.16f')
    
    quantile_df = quantile_score_ext(stats_df, 'gmean', 'year', 'type', reversed=True)
    quantile_df = adjust_score(quantile_df, 'gmean', 0, 0, reversed=True)
    quantile_df = change_types(quantile_df, Unemployed.TYPES)
    etl.load(quantile_df, Unemployed.FIGURES + '/unemployed_type_score.csv', ff='%.16f')


'''
Almost the same as above with stats_type, only now we calculate a rate based on starting unemployment rate
'''
@timeit
@rename('umemployed_stats_unemp_rate')
def stats_rate():
    # init
    data_df = etl.extract(Unemployed.FIGURES + '/unemployed_basic.csv', Data.HEADER, Data.TYPES)
    population_df = etl.extract(Population.FIGURES + '/population_raw.csv', Data.HEADER, Data.TYPES)

    # merge unemployed with population and set the unemployed rate type
    data_df = pd.merge(data_df, population_df[['unit_id', 'year', 'val']], on=['unit_id', 'year'], suffixes=('', '_population'))
    data_df.rename(columns={'val_population': 'population'}, inplace=True)
    data_df['rate'] = data_df['val'] / data_df['population']
    data_df['type'] = data_df.apply(lambda row: unemp_rate(row['rate']), axis=1)
    data_df = change_types(data_df, Unemployed.TYPES)
    etl.load(data_df, Unemployed.FIGURES + '/unemployed_unempl_rate.csv', ff='%.16f')

    # Milbert - unemployed score
    stats_df = rate_gmean_stats(data_df)
    stats_df = change_types(stats_df, Unemployed.TYPES)
    etl.load(stats_df, Unemployed.FIGURES + '/unemployed_unempl_stats.csv', ff='%.16f')
    
    quantile_df = quantile_score_ext(stats_df, 'gmean', 'year', 'type', reversed=True)
    quantile_df = adjust_score(quantile_df, 'gmean', 0, 0, reversed=True)
    quantile_df = change_types(quantile_df, Unemployed.TYPES)
    etl.load(quantile_df, Unemployed.FIGURES + '/unemployed_unempl_score.csv', ff='%.16f')


@timeit
@rename('umemployed_hist')
def hist():
    df = pd.read_csv(Unemployed.FIGURES + '/unemployed_unempl_rate.csv', sep=',', header=0)

    ax = df.hist(column='rate', bins=50, grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)

    plt.xlabel('Rate')
    plt.ylabel('Frequency')
    plt.title('Histogram of Rate')

    # Display the histogram
    plt.show()

    # ax = ax[0]
    # for x in ax:

    #     # Despine
    #     x.spines['right'].set_visible(False)
    #     x.spines['top'].set_visible(False)
    #     x.spines['left'].set_visible(False)

    #     # Switch off ticks
    #     x.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

    #     # Draw horizontal axis lines
    #     vals = x.get_yticks()
    #     for tick in vals:
    #         x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

    #     # Remove title
    #     x.set_title("")

    #     # Set x-axis label
    #     x.set_xlabel("Session Duration (Seconds)", labelpad=20, weight='bold', size=12)

    #     # Set y-axis label
    #     x.set_ylabel("Sessions", labelpad=20, weight='bold', size=12)

    #     # Format y-axis label
    #     x.yaxis.set_major_formatter(StrMethodFormatter('{x:,g}'))
