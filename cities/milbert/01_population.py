import pandas as pd
import numpy as np

from pandas import DataFrame

data_header = ['unit_id', 'unit_name', 'aggregate_id', 'var_id', 'measure_unit_id', 'last_update', 'year', 'val', 'attr_id']
units_header = []
conf_header = []

column_types = {
    'unit_id': str,
}

# we extract population data, units dict and conf
def extract(path: list[str], headers: list[list[str]], columns:list[dict(str)]) -> list[DataFrame]:
    for p in path:
    df = pd.read_csv(path, sep=',', header=0, names=input_header, dtype=column_types)

def extract(path: str, header: list[str], columns: dict[str, str]) -> DataFrame:
    df = pd.read_csv(path, sep=',', header=0, names=input_header, dtype=column_types)


def transform(df: DataFrame) -> DataFrame:
    
    return

def load(df: DataFrame, path: str):

    return


#     # saves data to the output dataset
# def load(df: DataFrame, path: str):
#     check_dir(path)
#     df.to_csv(path, float_format='%.2f', index=False)

# prepare population data, filter out unnecessary variables, shrink data table and unify ids in case of admin changes
def main():
    input_path = './data/stats/data_unit_population.csv'

    df = extract(input_path)
    df = transform(df)
    # load(df, output_path)

if __name__ == '__main__':
    main()