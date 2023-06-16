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
    DATA = ''
    FIGURES = ''
    SUBJECT_ID = ''
    VAR_ID = 1365234

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
    DATA = ''
    FIGURES = ''
    SUBJECT_ID = ''
    VAR_ID = 54821

class Unemployed:
    DATA = ''
    FIGURES = ''
    SUBJECT_ID = ''
    VAR_ID = 10514

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
        'diff': 'Int64',
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
    


