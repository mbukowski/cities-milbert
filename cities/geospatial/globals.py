import os

from qgis.core import *
from qgis.analysis import *
from PyQt5.QtCore import *

class Config:
    QGS_SYS_CONF = './config/qgis_win_sys_paths.csv'
    QGS_ENV_CONF = './config/qgis_win_env.json'
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    PCT_THRESHOLD = 2
    START_STEP = 9
    TEST_MODE = False
    TEST_FEATUER_COUNT = 9999
    TEST_CLC_YEAR = '2006'
    TEST_CLC_GROUP = 'urban_fabric'

class CLC:
    CLC_LAYERS = {
        '2006': 'U2012_CLC2006_V2020_20u1',
        '2012': 'U2018_CLC2012_V2020_20u1',
        '2018': 'U2018_CLC2018_V2020_20u1'
    }

    CLC_CODES = {
        'urban_fabric': ['111', '112'],
        'artificial_surfaces': ['111', '112', '121', '122', '123', '124', '131', '132', '133', '141', '142']
    }

class QGS:
    LAYERS_FOLDER = os.getenv('USERPROFILE').replace('\\', '/') + '/dev/qgis/shrinking-cities/layers'
    MEMORY = 'memory:'
    PREFIX = 'ovrl_'

class Attributes:
    FID = QgsField(name='fid', type=QVariant.Int, len=0)
    TERYT_ID = QgsField(name='teryt_id', type=QVariant.String, len=32)
    AREA = QgsField(name='area', type=QVariant.Double, len=0)
    PERIMETER = QgsField(name='perimeter', type=QVariant.Double, len=0)
    PCT = QgsField(name='pct', type=QVariant.Double, len=0)
    OBJECT_ID = QgsField(name='OBJECTID', type=QVariant.Int, len=0)
    CODE = QgsField(name='Code', type=QVariant.String, len=3)
    ID = QgsField(name='ID', type=QVariant.String, len=18)
    REMARK = QgsField(name='Remark', type=QVariant.String, len=20)
    AREA_HA = QgsField(name='Area_Ha', type=QVariant.Double, len=0)


class Geometry:
    BOUNDING_BOX = 0
    MINIMUM_ORIENTED_RECTANGLE = 1
    MINIMUM_ENCLOSING_CIRCLE = 2
    CONVEX_HULL = 3

class FlipMode:
    FLIP_HORIZONTAL = 0
    FLIP_VERTICAL = 1
    ROTATE_180 = 2
    ROTATE_90_CW = 3
    ROTATE_90_CCW = 4
