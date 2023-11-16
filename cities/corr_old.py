import pandas as pd
import sys
import json
import os
import re
import csv
import math

# simple correlation check for parameters 
def main():
    qgis_output = './data/processed/qgis'

    header_types = {
        'teryt_id': str
    }

    input_files = []
    for f in os.listdir(qgis_output):
        if re.search(r'^compactness.*\.csv', f):
            input_files.append(f'{os.path.abspath(qgis_output)}/{f}')

    df1 = pd.read_csv('./data/processed/units/units_commune.csv', sep=',', decimal='.', dtype=header_types)
    df2 = pd.concat((pd.read_csv(f, sep=',', decimal='.', dtype=header_types) for f in input_files), ignore_index=True)
    df = pd.merge(df1[['teryt_id', 'name']], df2, how='right', left_on=['teryt_id'], right_on=['teryt_id'])
    df.to_csv(f'{qgis_output}/compactness.csv', float_format='%.6f', index=False)

    # correlations
    # stats df -> teryt_id, period_end [year, year + 5] -> [2006, 2011] type (SMLR) -> (SML) -> (M), score

    # compactness
    # compact df teryt_id year group schwartzberg,polsby_popper,reock,box,rectangle,convex_hull
    




if __name__ == '__main__':
    main()