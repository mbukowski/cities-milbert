import pandas as pd
import sys
import json
import os
import re

qgs_sys_conf = './config/qgis_win_sys_paths.csv'
qgs_env_conf = './config/qgis_win_env.json'
layers_folder = 'C:/Users/mbukowski/dev/qgis/shrinking-cities/layers'

paths = pd.read_csv(qgs_sys_conf).paths.tolist()
sys.path += paths

with open(qgs_env_conf, 'r') as f:
    js = json.loads(f.read())
    for k, v in js.items():
        os.environ[k] = v

from qgis.core import *
from qgis.analysis import *
from PyQt5.QtCore import *

feedback = QgsProcessingFeedback()
QgsApplication.setPrefixPath(js['HOME'], True)
qgs = QgsApplication([], False)
qgs.initQgis()

from processing.core.Processing import *
