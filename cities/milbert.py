import pandas as pd

from common.utils import timeit
import milbert.population as population
import milbert.working_age as working_age
import milbert.own_revenue as own_revenue
import milbert.employment as employment
import milbert.migration as migration
import milbert.unemployed as unemployed
import milbert.summary as summary
import milbert.city as city

import common.etl as etl
from common.globals import Population, Data


'''
Main app script which reads data and processes them according to Milbert algorithm.
We collect data statistics for 6 parameters: 
- population
- migration
- working age
- employment rate
- unemployed
- own revenue
'''

'''
TODO Configuration
- If we have preprocessed data - to save time, but if we divide files by variable we should have no problems with time
- Which model we would like to run: FULL, BASIC, CITY, COMPLETE in reality we switch between BASIC and COMPLETE, 
as we only focus on municipality data.
- How long is the period (5, 6 years etc.)
- Specific algorithms in case we would like to implemnt them and try different things
- Configuration for the diagrams to generate 
- If we store data files in github what about qgis data which may be also large files? 
They are large files above hundeds of MB, need to save them on Google Drive or some other storage provider
- which modules to recalculate, but some of them may impact anothers and would be important to redo all of the necessary? 
or maybe just implement apache flow for etl? but on another hand we don't deliver data on regular basis, 
that should be theoretically one time approach
'''
def main():
    pd.set_option('display.max_rows', 40)

    # # Population
    # population.prep()
    # population.stats()

    # # Migration
    # migration.prep()
    # migration.stats()

    # # Working Age
    # working_age.prep()
    # working_age.stats()

    # # Employment Rate
    # employment.prep()
    # employment.stats()

    # # Unemployed
    # unemployed.prep()
    # unemployed.stats_distribution()
    
    # # Own Revenue
    # own_revenue.prep()
    # own_revenue.stats()

    # # Summary
    # city.size()
    # summary.default()
    
    # # Various
    # city.qgis()
    city.trend()
    # unemployed.hist()


if __name__ == '__main__':
    main()