class Data:
    HEADER = ['unit_id', 'var_id', 'year', 'val']
    TYPES = {
        'unit_id': str,
        'var_id': int,
        'year': int,
        'val': float
    }

class Population:
    DATA = './data/bdl/data_unit_population.csv'
    FIGURES = './figures/population'
    SUBJECT_ID = 'P2137'
    VAR_ID = 72305
    TYPES = {
        'unit_id': str,
        'var_id': int,
        'year': int,
        'val': int,
        'diff': 'Int64',
        'rate': float,
        'mean': float,
        'gmean': float,
        'score': int,
        'adj_score': int
    }

class Migration:
    DATA = './data/bdl/data_unit_migration.csv'
    FIGURES = './figures/migration'
    SUBJECT_ID = 'P1350'
    VAR_ID = 1365234
    TYPES = {
        'unit_id': str,
        'var_id': int,
        'year': int,
        'val': int,
        'population': int,
        'rate': float,
        'sum': float,
        'score': int,
        'adj_score': int
    }

class WorkingAge:
    DATA = './data/bdl/data_unit_working_age.csv'
    FIGURES = './figures/working_age'
    SUBJECT_ID = 'P1342'
    VAR_ID = 152
    TYPES = {
        'unit_id': str,
        'var_id': int,
        'year': int,
        'val': int,
        'diff': 'Int64',
        'rate': float,
        'mean': float,
        'gmean': float,
        'score': int,
        'adj_score': int
    }

class Employment:
    DATA = './data/bdl/data_unit_employment.csv'
    FIGURES = './figures/employment'
    SUBJECT_ID = 'P2172'
    VAR_ID = 54821
    TYPES = {
        'unit_id': str,
        'var_id': int,
        'year': int,
        'val': int,
        'intrpl': int,
        'diff': 'Int64',
        'rate': float,
        'mean': float,
        'gmean': float,
        'score': int,
        'adj_score': int
    }

class Unemployed:
    DATA = './data/bdl/data_unit_unemployed.csv'
    FIGURES = './figures/unemployed'
    SUBJECT_ID = 'P1944'
    VAR_ID = 10514
    TYPES = {
        'unit_id': str,
        'var_id': int,
        'year': int,
        'val': int,
        'population': int,
        'rate': float,
        'group': str,
        'group_start': str,
        'diff': float,
        'mean': float,
        'gmean': float,
        'score': int,
        'adj_score': int
    }
    RATE = [(0.015, 'A'), (0.085, 'B'), (1.00, 'C')]
    DISTRIBUTION = [0.2, 0.8]

'''
Total: P2621 -> 76037
Own:   P2622 -> 76070
'''
class OwnRevenue:
    DATA = './data/bdl/data_unit_own_revenue.csv'
    FIGURES = './figures/own_revenue'
    SUBJECT_ID = 'P2622'
    VAR_ID = 76070
    TYPES = {
        'unit_id': str,
        'var_id': int,
        'year': int,
        'val': int,
        'intrpl': int,
        'diff': 'Float64',
        'rate': float,
        'mean': float,
        'gmean': float,
        'score': int,
        'adj_score': int
    }

class Stats:
    FIGURES = './figures/stats'
    # HEADER = ['unit_id', 'teryt_id', 'name', 'period_start', 'period_end', 'population_start', 'population_end', 'type', 
    #           'pop', 'migr', 'age', 'empl', 'unempl', 'revenue', 'score', 'status']
    HEADER = ['unit_id', 'teryt_id', 'name', 'level', 'kind',
              'period_start', 'period_end', 'population_start', 'population_end', 'type',
              'pop_rate', 'pop_points', 'migr_rate', 'migr_points', 'age_rate', 'age_points', 
              'empl_rate', 'empl_points', 'unempl_rate', 'unempl_points', 'revenue_rate', 'revenue_points', 
              'score', 'status']
    # TYPES = {
    #     'unit_id': str,
    #     'var_id': int,
    #     'year': int,
    #     'val': int,
    #     'intrpl': int,
    #     'diff': 'Float64',
    #     'rate': float,
    #     'mean': float,
    #     'gmean': float,
    #     'score': int,
    #     'adj_score': int
    # }
    


class Units:
    FIGURES = './figures/units'
    DATA = FIGURES + '/units.csv'
    BASIC_DATA = FIGURES + '/units_basic.csv'
    CITY_DATA = FIGURES + '/units_city.csv'
    COMMUNE_DATA = FIGURES + '/units_commune.csv'
    COMPLETE_DATA = FIGURES + '/units_complete.csv'
    HEADER = ['unit_id', 'parent_id', 'teryt_id', 'name', 'level', 'kind']
    TYPES = {
        'unit_id': str,
        'parent_id': str,
        'teryt_id': str,
        'name': str,
        'level': int,
        'kind': int,
    }


class UnitsData:
    DATA = './data/dict/units.csv'
    HEADER = ['unit_id', 'parent_id', 'name', 'level', 'kind', 'has_description', 'description', 'years']
    TYPES = {
        'unit_id': str,
        'parent_id': str,
        'name': str,
        'level': int,
        'kind': int,
        'has_description': bool,
        'description': str,
        'years': str
    }


class Unify:
    DATA = './data/conf/unify.csv'
    HEADER = ['from', 'to', 'mode', 'name', 'description', 'start_year', 'end_year']
    TYPES = {
        'from': str,
        'to': str,
        'mode': int,
        'name': str,
        'description': str,
        'start_year': 'Int64',
        'end_year': 'Int64'
    }

class City:
    FIGURES = './figures/city'
    POPULATION_DATA = FIGURES + '/city_population.csv'
    RURAL = { 'id': 'R', 'name': 'rural' }
    SMALL = { 'id': 'S', 'name': 'small', 'min_size': 0, 'max_size': 20000 }
    MEDIUM = { 'id': 'M', 'name': 'medium', 'min_size': 20000, 'max_size': 100000 }
    LARGE = { 'id': 'L', 'name': 'large', 'min_size': 100000, 'max_size': 100000000 }
    SIZE_MARGIN = 0.00
    QGIS_HEADER = ['teryt_id', 'name', 'level', 'kind', 
                   'period_start', 'period_end', 'population_start', 'population_end', 
                   'type', 'score', 'status']

class GrowthStrategy:
    STRONG_TREND = { 
        'AAA': 'AA', 'EEE': 'EE', 'CCC': 'CC',
        'AAD': 'AE', 'AAE': 'AE',
        'EEA': 'EA', 'EEB': 'EA' 
    }
    NORMAL_TREND = { 
        'AAA': 'AA', 'EEE': 'EE', 'CCC': 'CC',
        'AAD': 'AE', 'AAE': 'AE', 
        'BAE': 'AE', 'ABE': 'AE', 'BBE': 'AE',
        'EEA': 'EA', 'EEB': 'EA', 
        'EDA': 'EA', 'DEA': 'EA', 'DDA': 'EA'
    }
    WEAK_TREND = {
        'AAA': 'AA', 'EEE': 'EE', 'CCC': 'CC',
        'AAD': 'AE', 'AAE': 'AE', 
        'BAE': 'AE', 'ABE': 'AE', 'BBE': 'AE', 
        'BAD': 'AE', 'ABD': 'AE', 'BBD': 'AE',
        'EEA': 'EA', 'EEB': 'EA', 
        'EDA': 'EA', 'DEA': 'EA', 'DDA': 'EA', 
        'EDB': 'EA', 'DEB': 'EA', 'DDB': 'EA'
    }
