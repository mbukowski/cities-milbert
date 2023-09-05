# necessary imports
import os
import sys
import json
import pandas as pd

# small changes

# # set up system paths
# qspath = './config/qgis_sys_paths.csv'

# # provide the path where you saved this file.
# paths = pd.read_csv(qspath).paths.tolist()
# sys.path += paths

# set up environment variables
qepath = './config/qgis_env.json'
js = json.loads(open(qepath, 'r').read())
for k, v in js.items():
    os.environ[k] = v

# In special cases, we might also need to map the PROJ_LIB to handle the projections
# for mac OS
os.environ['PROJ_LIB'] = '/Applications/Qgis.app/Contents/Resources/proj'

import PyQt5.QtCore
import qgis

# import gdal
import qgis.PyQt.QtCore
from qgis.core import (QgsApplication,
                       QgsProcessingFeedback,
                       QgsProcessingRegistry)
from qgis.analysis import QgsNativeAlgorithms

def main():
    
    feedback = QgsProcessingFeedback()

    # initializing processing module
    # maybe we don't need to set prefix path as it's already included in variables
    qgis.QgsApplication.setPrefixPath(js['HOME'], True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    qgs.exitQgis()



if __name__ == '__main__':
    main()