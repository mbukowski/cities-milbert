class Data:
    HEADER = ['unit_id', 'var_id', 'year', 'val']
    TYPES = {
        'unit_id': str,
        'var_id': 'Int64',
        'year': 'Int64',
        'val': 'Int64'
    }

class Population:
    DATA = './data/bdl/data_unit_population.csv'
    FIGURES = './figures/population'
    SUBJECT_ID = 'P2137'
    VAR_ID = 72305
    TYPES = {
        'unit_id': str,
        'var_id': 'Int64',
        'year': 'Int64',
        'val': 'Int64',
        'diff': 'Int64',
        'rate': 'Float64',
        'mean': 'Float64',
        'gmean': 'Float64',
        'score': 'Int64',
        'adj_score': 'Int64'
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
        'var_id': 'Int64',
        'year': 'Int64',
        'val': 'Int64',
        'diff': 'Int64',
        'rate': 'Float64',
        'mean': 'Float64',
        'gmean': 'Float64',
        'score': 'Int64',
        'adj_score': 'Int64'
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

class OwnRevenue:
    DATA = ''
    FIGURES = ''
    SUBJECT_ID = ''
    VAR_ID = 76070

class Units:
    HEADER = ['unit_id', 'parent_id', 'teryt_id', 'name', 'level', 'kind']    
    DATA_HEADER = ['unit_id', 'parent_id', 'name', 'level', 'kind', 'has_description', 'description', 'years']
    TYPES = {
        'unit_id': str,
        'parent_id': str,
        'teryt_id': str,
        'name': str,
        'level': 'Int64',
        'kind': 'Int64',
        'has_description': bool,
        'description': str,
        'years': str
    }
    DATA = './data/dict/units.csv'
    FIGURES = './figures/units'
    BASIC_DATA = FIGURES + '/units_basic.csv'
    CITY_DATA = FIGURES + '/units_city.csv'
    FULL_DATA = FIGURES + '/units_full.csv'

class Unify:
    HEADER = ['from', 'to', 'mode', 'name', 'description']
    TYPES = {
        'from': str,
        'to': str,
        'mode': 'Int64',
        'name': str,
        'description': str
    }
    DATA = './data/conf/unify.csv'


