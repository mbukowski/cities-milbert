import pandas as pd

from common.utils import timeit
import milbert.population as population


'''
Main app script which reads data and processes them according to Milbert algorithm.
We collect data statistics for 6 parameters: 
- population
- unemployment rate
- ...
'''


def main():
    pd.set_option('display.max_rows', 40)

    population.prep()
    population.stats()

    pass

if __name__ == '__main__':
    main()