1. Installation procedure from the repository - qgis 
2. install qgis
3. download files 

## CLC
download each file
modify symbologoy legend 
Code_06 / Code_12 / Code_18 -> Code

##
Fixing geometry in case something is broken


that can be done like this as if every time a new update is released it's propagated down to the respective version
And inside the layer -> script to modify column name

what about converting to other formats?  

we have to 


describe how qgis data have to be prepared, which years taken 2021 - not from WFS, that geometries have to be fixed as well for following features
636: 1425103 Skaryszew
951: 2815042 Łukta
1144: 3012052 Rozdrażew
2351: 1007032 Mniszków
we can try to init and clean all features for clip layers by fix_layer = processing.run("native:fixgeometries", {'INPUT':layer,'OUTPUT':'memory:'})['OUTPUT'] ...
for a moment it's done manually
or we could copy fixed geometry from a new feature layre and copy it to existing one - that could also work 
we can also check geometry with validateGeometry() in QGSGeometry class - that we should do actually every time ;)
How we need to enhance our layers by adding fields, how to cut, how to dissolve etc,



Download paths and system env from qgis

import sys
import pandas as pd
paths = sys.path
df = pd.DataFrame({'paths':paths})
df.to_csv('C:/Users/mbukowski/qgis_sys_paths.csv', index=False)


import os
import json
env = dict(os.environ)
rem = ['SECURITYSESSIONID', 'LaunchInstanceID', 'TMPDIR']
_ = [env.pop(r, None) for r in rem]
with open('C:/Users/mbukowski/qgis_env.json', 'w') as f: 
    json.dump(env, f, ensure_ascii=False, indent=4)

Register algorithm provider for each plugein
C:/Users/mbukowski/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/shapetools

Display algorithms available
for alg in QgsApplication.processingRegistry().algorithms():
    print(f'{alg.id()} -> {alg.displayName()}')
