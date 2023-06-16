import pandas as pd

from common.utils import timeit
import milbert.population as population
import milbert.working_age as working_age
import milbert.own_revenue as own_revenue

import common.etl as etl
from common.globals import Population, Data


'''
Main app script which reads data and processes them according to Milbert algorithm.
We collect data statistics for 6 parameters: 
- population
- working age
- own revenue
- migration
- employment
- unemployment rate
- ...
'''


def main():
    pd.set_option('display.max_rows', 40)

    # # Population
    # population.prep()
    # population.stats()

    # # Working Age
    # working_age.prep()
    # working_age.stats()

    # Own Revenue
    own_revenue.prep()
    own_revenue.stats()


if __name__ == '__main__':
    main()