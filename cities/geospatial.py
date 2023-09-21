import pandas as pd
import sys
import json
import os
import re
import csv
import math

from common.utils import *
from geospatial.common import *
from geospatial.globals import *
from geospatial.methods import *

paths = pd.read_csv(Config.QGS_SYS_CONF).paths.tolist()
sys.path += paths

with open(Config.QGS_ENV_CONF, 'r') as f:
    js = json.loads(f.read())
    for k, v in js.items():
        os.environ[k] = v

from qgis.core import (
    QgsApplication, 
    QgsProcessingFeedback
)
from PyQt5.QtCore import *

feedback = QgsProcessingFeedback()
QgsApplication.setPrefixPath(js['HOME'], True)
qgs = QgsApplication([], False)
qgs.initQgis()

from processing.core.Processing import Processing
Processing.initialize()

# Shape Tools plugin
from shapetools.provider import ShapeToolsProvider
provider = ShapeToolsProvider()
QgsApplication.processingRegistry().addProvider(provider)

def main():
    # administrative_boundaries paths
    adm_boundaries_folder = '/processed/prg/administrative_boundaries'
    adm_boundaries_gpkg = build_gpkg(QGS.LAYERS_FOLDER, adm_boundaries_folder, 'administrative_boundaries.gpkg')
    adm_country_layer = build_layer(adm_boundaries_gpkg, 'country')
    adm_commune_layer = build_layer(adm_boundaries_gpkg, 'commune')

    # # step 0: test functions
    # if Config.TEST_MODE & (Config.START_STEP <= 0): 
    #     test_layer(adm_commune_layer, field1='JPT_KOD_JE', field2='JPT_NAZWA_')

    for year in CLC.CLC_LAYERS.keys():
        if Config.TEST_MODE & (year != Config.TEST_CLC_YEAR): continue
        print(f'YEAR: {year}')

        # raw clc paths
        raw_clc_folder = '/raw/clc/' + year
        raw_clc_gpkg = build_gpkg(QGS.LAYERS_FOLDER, raw_clc_folder, f'{CLC.CLC_LAYERS[year]}.gpkg')
        raw_clc_layer = build_layer(raw_clc_gpkg, CLC.CLC_LAYERS[year])

        # processed clc paths
        clc_folder = '/processed/clc/' + year
        clc_gpkg = build_gpkg(QGS.LAYERS_FOLDER, clc_folder, f'clc_{year}.gpkg')
        clc_01_poland_layer = build_layer(clc_gpkg, f'clc_{year}_01_poland')
        clc_02_commune_layer = build_layer(clc_gpkg, f'clc_{year}_02_commune')

        # step 1: clip a layer and save to geopackage
        if Config.START_STEP <= 1: clip_to_layer(raw_clc_layer, adm_country_layer, clc_01_poland_layer)

        # step 2: clip layers with commune outlines and store them as separate features
        if Config.START_STEP <= 2: clip_to_features(clc_01_poland_layer, adm_commune_layer, clc_02_commune_layer, {'JPT_KOD_JE': Attributes.TERYT_ID})

        for group in CLC.CLC_CODES.keys():
            if Config.TEST_MODE & (group != Config.TEST_CLC_GROUP): continue
            print(f'YEAR: {year} - CLC GROUP: {group}')

            # paths related to clc codes
            clc_03_filtered_layer = build_layer(clc_gpkg, f'clc_{year}_{group}_03_filtered')
            clc_04_dissolved_layer = build_layer(clc_gpkg, f'clc_{year}_{group}_04_dissolved')
            clc_05_pct_layer = build_layer(clc_gpkg, f'clc_{year}_{group}_05_pct')
            clc_11_baseline = build_layer(clc_gpkg, f'clc_{year}_{group}_11_baseline')
            clc_12_box = build_layer(clc_gpkg, f'clc_{year}_{group}_12_box')
            clc_13_rectangle = build_layer(clc_gpkg, f'clc_{year}_{group}_13_rectangle')
            clc_14_circle = build_layer(clc_gpkg, f'clc_{year}_{group}_14_circle')
            clc_15_convex = build_layer(clc_gpkg, f'clc_{year}_{group}_15_convex')
            clc_16_horizontal = build_layer(clc_gpkg, f'clc_{year}_{group}_16_horizontal')
            clc_17_vertical = build_layer(clc_gpkg, f'clc_{year}_{group}_17_vertical')
           
            # step 3: filter features based on clc codes
            if Config.START_STEP <= 3: filter_by_attributes(clc_02_commune_layer, clc_03_filtered_layer, 'Code', CLC.CLC_CODES[group])

            # step 4: merge group of features sharing the same teryt_id, but keep them disjointed
            if Config.START_STEP <= 4:
                fields_to_delete = [Attributes.OBJECT_ID, Attributes.CODE, Attributes.ID, Attributes.REMARK, Attributes.AREA_HA]
                dissolve_by_attributes(clc_03_filtered_layer, clc_04_dissolved_layer, attributes=[Attributes.TERYT_ID], del_attributes=fields_to_delete)

            # step 5: calculate feature's percentage of total commune size
            if Config.START_STEP <= 5: calculate_percentage(clc_04_dissolved_layer, clc_05_pct_layer, group_by_attr=Attributes.TERYT_ID)

            # step 6: filter out small features below the percentage threshold
            if Config.START_STEP <= 6: prepare_baseline(clc_05_pct_layer, clc_11_baseline, attributes=[Attributes.TERYT_ID])

            # step 7: construct minimum bounding geometries
            if Config.START_STEP <= 7:
                bounding_box(clc_11_baseline, clc_12_box, Attributes.TERYT_ID)
                minimum_oriented_rectangle(clc_11_baseline, clc_13_rectangle, Attributes.TERYT_ID)
                minimum_enclosing_circle(clc_11_baseline, clc_14_circle, Attributes.TERYT_ID)
                convex_hull(clc_11_baseline, clc_15_convex, Attributes.TERYT_ID)

            # commented for a time beeing due to invalid geometry, probably it happens during horizontal / vertical flips
            # we should apply another strategy, from input layer take one feature at the time and do an intersection - longer process but should avoid and be able to track problems
            # step 8: flip layers horizontally and vertically and get their common part with baseline layer
            # if Config.START_STEP <= 8:
            #     horizontal_flip(clc_11_baseline, clc_16_horizontal, input_field=Attributes.TERYT_ID, overlay_field=Attributes.TERYT_ID)
            #     vertical_flip(clc_11_baseline, clc_17_vertical, input_field=Attributes.TERYT_ID, overlay_field=Attributes.TERYT_ID)

            # step 9: save compactness stats
            if Config.START_STEP <= 9:
                result_dict = {}

                count = 0
                baseline_vl = get_vl(clc_11_baseline)
                total = baseline_vl.featureCount()
                for feature in baseline_vl.getFeatures():
                    count += 1
                    teryt_id = feature['teryt_id']
                    area = feature['area']
                    perimeter = feature['perimeter']

                    print(f'BASE: {count:>4} / {total}: {teryt_id}')

                    if teryt_id not in result_dict:
                        result_dict[teryt_id] = {}

                    feature_dict = result_dict[teryt_id]
                    feature_dict['teryt_id'] = teryt_id
                    feature_dict['year'] = year
                    feature_dict['group'] = group
                    feature_dict['base_area'] = area
                    feature_dict['base_perimeter'] = perimeter

                    print(Config.LINE_UP, end=Config.LINE_CLEAR)

                count = 0
                box_vl = get_vl(clc_12_box)
                total = box_vl.featureCount()
                for feature in box_vl.getFeatures():
                    count += 1
                    teryt_id = feature['teryt_id']
                    area = feature['area']
                    perimeter = feature['perimeter']

                    print(f'BOX: {count:>4} / {total}: {teryt_id}')

                    if teryt_id not in result_dict:
                        result_dict[teryt_id] = {}

                    feature_dict = result_dict[teryt_id]
                    feature_dict['box_area'] = area
                    feature_dict['box_perimeter'] = perimeter

                    print(Config.LINE_UP, end=Config.LINE_CLEAR)

                count = 0
                rect_vl = get_vl(clc_13_rectangle)
                total = rect_vl.featureCount()
                for feature in rect_vl.getFeatures():
                    count += 1
                    teryt_id = feature['teryt_id']
                    area = feature['area']
                    perimeter = feature['perimeter']

                    print(f'RECT: {count:>4} / {total}: {teryt_id}')

                    if teryt_id not in result_dict:
                        result_dict[teryt_id] = {}

                    feature_dict = result_dict[teryt_id]
                    feature_dict['rect_area'] = area
                    feature_dict['rect_perimeter'] = perimeter

                    print(Config.LINE_UP, end=Config.LINE_CLEAR)

                count = 0
                circ_vl = get_vl(clc_14_circle)
                total = circ_vl.featureCount()
                for feature in circ_vl.getFeatures():
                    count += 1
                    teryt_id = feature['teryt_id']
                    radius = feature['radius']
                    area = feature['area']

                    print(f'CIRC: {count:>4} / {total}: {teryt_id}')

                    if teryt_id not in result_dict:
                        result_dict[teryt_id] = {}

                    feature_dict = result_dict[teryt_id]
                    feature_dict['circ_radius'] = radius
                    feature_dict['circ_area'] = area

                    print(Config.LINE_UP, end=Config.LINE_CLEAR)

                count = 0
                convex_vl = get_vl(clc_15_convex)
                total = convex_vl.featureCount()
                for feature in convex_vl.getFeatures():
                    count += 1
                    teryt_id = feature['teryt_id']
                    area = feature['area']
                    perimeter = feature['perimeter']

                    print(f'CONV: {count:>4} / {total}: {teryt_id}')

                    if teryt_id not in result_dict:
                        result_dict[teryt_id] = {}

                    feature_dict = result_dict[teryt_id]
                    feature_dict['conv_area'] = area
                    feature_dict['conv_perimeter'] = perimeter

                    print(Config.LINE_UP, end=Config.LINE_CLEAR)

                count = 0
                convex_vl = get_vl(clc_15_convex)
                total = convex_vl.featureCount()
                for feature in convex_vl.getFeatures():
                    count += 1
                    teryt_id = feature['teryt_id']
                    area = feature['area']
                    perimeter = feature['perimeter']

                    print(f'CONV: {count:>4} / {total}: {teryt_id}')

                    if teryt_id not in result_dict:
                        result_dict[teryt_id] = {}

                    feature_dict = result_dict[teryt_id]
                    feature_dict['conv_area'] = area
                    feature_dict['conv_perimeter'] = perimeter

                    print(Config.LINE_UP, end=Config.LINE_CLEAR)

                for res in result_dict.values():
                    res['schwartzberg_radius'] = math.sqrt(float(res['base_area']) / math.pi)
                    res['schwartzberg_circumference'] = 2 * math.pi * res['schwartzberg_radius']

                    res['schwartzberg'] = 1 / (float(res['base_perimeter']) / res['schwartzberg_circumference'])
                    res['polsby_popper'] = 4 * math.pi * float(res['base_area']) / math.pow(float(res['base_perimeter']), 2)
                    res['reock'] = float(res['base_area']) / float(res['circ_area'])
                    res['box'] = float(res['base_area']) / float(res['box_area'])
                    res['rectangle'] = float(res['base_area']) / float(res['rect_area'])
                    res['convex_hull'] = float(res['base_area']) / float(res['conv_area'])

                entry = list(result_dict.values())[0]
                fields = list(entry.keys())
                result_list = [value for value in result_dict.values()]
                
                with open(f'./data/processed/qgis/compactness_{year}_{group}.csv', 'w', newline='') as file: 
                    writer = csv.DictWriter(file, fieldnames = fields)
                    writer.writeheader()
                    writer.writerows(result_list)

    # combine to df / merge with names per teryt_id
    # to compactness.csv

    qgs.exitQgis()


if __name__ == '__main__':
    main()