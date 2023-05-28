from common.globals import DataScheme as DS
from common.globals import UnitsScheme as US
from common.globals import UnifyConfScheme as UCS

import pandas as pd
import numpy as np
import common.etl as etl

from pandas import DataFrame


'''
We load data 
'''


# # we extract population data, units dict and conf
# def extract(path: list[str], headers: list[list[str]], columns:list[dict(str)]) -> list[DataFrame]:
#     for p in path:
#     df = pd.read_csv(path, sep=',', header=0, names=input_header, dtype=column_types)

# def extract(path: str, header: list[str], columns: dict[str, str]) -> DataFrame:
#     df = pd.read_csv(path, sep=',', header=0, names=input_header, dtype=column_types)


# def transform(df: DataFrame) -> DataFrame:
    
#     return

# def load(df: DataFrame, path: str):

#     return


#     # saves data to the output dataset
# def load(df: DataFrame, path: str):
#     check_dir(path)
#     df.to_csv(path, float_format='%.2f', index=False)

# prepare population data, filter out unnecessary variables, shrink data table and unify ids in case of admin changes
def main():
    # extract
    population_df = etl.extract(DS.POPULATION_PATH, DS.HEADER, DS.TYPES)
    basic_df = etl.extract(US.BASIC_PATH, US.HEADER, US.TYPES)
    conf_df = etl.extract(UCS.PATH, UCS.HEADER, UCS.TYPES)

    print(basic_df.head())
    print(basic_df.dtypes)

    # transform


    # load
