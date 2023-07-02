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
        'type': str,
        'rate': float,
        'diff': float,
        'mean': float,
        'gmean': float,
        'score': int,
        'adj_score': int
    }
    RATE = [(0.05, 'A'), (0.10, 'B'), (1.00, 'C')]

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

class Units:
    FIGURES = './figures/units'
    DATA = FIGURES + '/units.csv'
    BASIC_DATA = FIGURES + '/units_basic.csv'
    CITY_DATA = FIGURES + '/units_city.csv'
    FULL_DATA = FIGURES + '/units_full.csv'
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
    HEADER = ['from', 'to', 'mode', 'name', 'description']
    TYPES = {
        'from': str,
        'to': str,
        'mode': int,
        'name': str,
        'description': str
    }

class City:
    SMALL = { 'id': 'S', 'name': 'small', 'min_size': 0, 'max_size': 20000 }
    MEDIUM = { 'id': 'M', 'name': 'medium', 'min_size': 20000, 'max_size': 100000 }
    LARGE = { 'id': 'L', 'name': 'large', 'min_size': 100000, 'max_size': 100000000 }
    SIZE_MARGIN = 0.05
