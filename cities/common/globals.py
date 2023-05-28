class DataScheme:
    HEADER = ['unit_id', 'var_id', 'year', 'val']
    TYPES = {
        'unit_id': str,
        'var_id': 'Int64',
        'year': 'Int64',
        'val': 'Int64'
    }
    POPULATION_PATH = './data/bdl/data_unit_population.csv'

class UnitsScheme:
    HEADER = ['id', 'parent_id', 'teryt_id', 'name', 'level', 'kind']    
    DATA_HEADER = ['id', 'parent_id', 'name', 'level', 'kind', 'has_description', 'description', 'years']
    TYPES = {
        'id': str,
        'parent_id': str,
        'teryt_id': str,
        'name': str,
        'level': 'Int64',
        'kind': 'Int64',
        'has_description': bool,
        'description': str,
        'years': str
    }
    PATH = './data/dict/units.csv'
    BASIC_PATH = './figures/units/units_basic.csv'
    CITY_PATH = './figures/units/units_city.csv'
    FULL_PATH = './figures/units/units_full.csv'

class UnifyConfScheme:
    HEADER = ['from', 'to', 'mode', 'name', 'description']
    TYPES = {
        'from': str,
        'to': str,
        'mode': 'Int64',
        'name': str,
        'description': str
    }
    PATH = './data/conf/unify.csv'
