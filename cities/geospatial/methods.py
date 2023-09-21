from common.utils import *
from geospatial.common import *
from geospatial.globals import *
from geospatial.layers import *

from qgis.core import (
    QgsVectorFileWriter, 
    QgsField, 
    QgsFeatureRequest, 
    QgsExpression
)
from qgis.analysis import *
from PyQt5.QtCore import *
from processing.core.Processing import *


# test function
def test_layer(name, **kwargs):
    vl = get_vl(name)

    print(f'layer: {name}')
    print(f'feature count: {vl.featureCount()}')

    i = 0
    for feature in vl.getFeatures():
        if i > 9: break

        features = [feature[v] for v in kwargs.values()]
        print(f'{i}: {features}')
        i += 1

# creates an empty layer based on template layer, if layer exists it's overwritten
def create_empty_layer(template_layer, layer):
    create_layer(template_layer, layer)

# creates an empty geopackage with initial layer and schema based on input layer, file must not exist
def create_empty_gpkg(template_layer, layer_name):
    create_layer(template_layer, layer_name, action=QgsVectorFileWriter.CreateOrOverwriteFile)

# appends whole layer to existing layer (must exist), both have the same schema
def append_features(input_layer, output_layer):
    append_layer(input_layer, output_layer)

# appends only selected features from input layer to existing layer (must exist), both have the same schema
def append_selected_features(input_layer, output_layer):
    append_layer(input_layer, output_layer, selected_features=True)

# creates a new layer and copies a whole content to a new layer
def copy_layer(input_layer, output_layer):
    create_layer(input_layer, output_layer)
    append_layer(input_layer, output_layer)

# clips an input layer to the outline of the overlay layer and saves an output to gpkg layer
def clip_to_layer(input_layer, overlay_layer, output_layer):
    output_db = build_db(output_layer)

    clip_layer(input_layer, overlay_layer, output_db)

# clips an input layer to every feature of the overlay layer and saves an output to gpkg layer
# enhances clip with attributes' values from the features and stores them in added field
@timeit
def clip_to_features(input_layer, overlay_layer, output_layer, attributes={}):
    output_gpkg = extract_gpkg(output_layer)
    temp_layer = build_layer(output_gpkg, 'temp_overlay')

    create_empty_layer(input_layer, output_layer)
    create_empty_layer(overlay_layer, temp_layer)

    add_attributes(output_layer, attributes.values()) # this one maybe not needed if we have new thingy

    overlay_vl = get_vl(overlay_layer)
    temp_vl = get_vl(temp_layer)
    output_vl = get_vl(output_layer)

    fid = 1
    count = 1
    total = overlay_vl.featureCount()
    for overlay_feature in overlay_vl.getFeatures():
        code = overlay_feature['JPT_KOD_JE']
        unit_name = overlay_feature['JPT_NAZWA_']
        print(f'{count:>4} / {total}: {code} {unit_name}')

        with edit(temp_vl):
            temp_dp = temp_vl.dataProvider()
            temp_dp.addFeature(overlay_feature)

        clipped_vl = clip_layer(input_layer, temp_layer)

        # adds fields based on attributes, where a key is a field in overlay layer from which we take features and value is a field in output layer
        # field in output layer must be added to clipped layer, these fields must be already in output_layer format otherwise we would have encounter a compatibility issue
        for overlay_field_name in attributes.keys():
            output_field_name = attributes[overlay_field_name].name()
            field = field_by_name(overlay_vl, overlay_field_name)
            add_attributes(clipped_vl, [QgsField(name=output_field_name, type=field.type(), len=field.length())])

        # for each feature in clipped layer we add values based on overlay layer and we add them to output layer
        with edit(output_vl):
            for clipped_feature in clipped_vl.getFeatures():
                for overlay_field_name in attributes.keys():
                    output_field_name = attributes[overlay_field_name].name()
                    clipped_feature[output_field_name] = overlay_feature[overlay_field_name]
                    clipped_feature['fid'] = fid

                    output_vl.addFeature(clipped_feature)
                    fid += 1

        print(Config.LINE_UP, end=Config.LINE_CLEAR)
        clean_db(temp_layer)

        count += 1
        if Config.TEST_MODE & (count > Config.TEST_FEATUER_COUNT):
            break

# filters an input layer for a given list of possible values for given attribute
@timeit
def filter_by_attributes(input_layer, output_layer, attribute_name, values=[]):
    codes = [f'\'{c}\'' for c in values]
    expression = f'"{attribute_name}" in ({", ".join(codes)})'
    output_db = build_db(output_layer)
    
    filter_by_expression(input_layer, output_db, expression)

# dissolves an input layer, groups features by attributes and keeps separate polygons disjointed and adds geometry
@timeit
def dissolve_by_attributes(input_layer, output_layer, attributes=[], del_attributes=[]):
    attr_names = [attr.name() for attr in attributes]

    temp_clc_layer = build_layer(extract_gpkg(output_layer), 'temp_clc')
    create_empty_layer(input_layer, temp_clc_layer)
    create_empty_layer(input_layer, output_layer)

    vl = dissolve_layer(input_layer, fields=attr_names, separate_disjoint=True)
    append_features(vl, temp_clc_layer)
    
    vl = add_geometry(temp_clc_layer)
    add_attributes(output_layer, [Attributes.AREA, Attributes.PERIMETER])
    append_features(vl, output_layer)

    # cleanup unnecessary fields which may bring confusion
    delete_attributes(output_layer, del_attributes)
    
# for each feature calculate percantege of total area for each commune recognised by passed attribute
@timeit
def calculate_percentage(input_layer, output_layer, group_by_attr):
    copy_layer(input_layer, output_layer)
    add_attributes(output_layer, [Attributes.PCT])
    vl = get_vl(output_layer)

    area_dict = {}
    for feature in vl.getFeatures():
        group_by_attr_id = feature[group_by_attr.name()]
        area = feature[Attributes.AREA.name()]
        
        if group_by_attr_id in area_dict:
            area_dict[group_by_attr_id] += area
        else:
            area_dict[group_by_attr_id] = area

    with edit(vl):
        for feature in vl.getFeatures():
            group_by_attr_id = feature[group_by_attr.name()]
            area = feature[Attributes.AREA.name()]
            pct = area / area_dict[group_by_attr_id]
            pct = pct * 100

            field_id = vl.fields().indexFromName(Attributes.PCT.name())
            vl.changeAttributeValue(feature.id(), field_id, pct)

# prepares baseline by filtering out unnecessary features
@timeit
def prepare_baseline(input_layer, output_layer, attributes=[]):
    attr_names = [attr.name() for attr in attributes]

    temp_clc_layer = build_layer(extract_gpkg(output_layer), 'temp_clc')
    create_empty_layer(input_layer, temp_clc_layer)
    
    input_vl = get_vl(input_layer)
    vl = get_vl(temp_clc_layer)
    
    query = f'"{Attributes.PCT.name()}" >= {Config.PCT_THRESHOLD}'
    expression = QgsExpression(query)
    request = QgsFeatureRequest(expression)
    selected_features = [feature for feature in input_vl.getFeatures(request)]
    with edit(vl):
        vl.addFeatures(selected_features)

    vl = dissolve_layer(temp_clc_layer, fields=attr_names, separate_disjoint=False)
    delete_attributes(vl, [Attributes.AREA, Attributes.PERIMETER, Attributes.PCT])
    copy_layer(vl, temp_clc_layer)

    vl = add_geometry(temp_clc_layer)
    copy_layer(vl, output_layer)

# constructs bounding box around features
@timeit
def bounding_box(input_layer, output_layer, attribute):
    vl = minimum_bounding_geometry(input_layer, attribute.name(), Geometry.BOUNDING_BOX)
    copy_layer(vl, output_layer)

# constructs minimum orientend rectangle around features
@timeit
def minimum_oriented_rectangle(input_layer, output_layer, attribute):
    vl = minimum_bounding_geometry(input_layer, attribute.name(), Geometry.MINIMUM_ORIENTED_RECTANGLE)
    copy_layer(vl, output_layer)

# constructs minimum enclosing circle around features
@timeit
def minimum_enclosing_circle(input_layer, output_layer, attribute):
    vl = minimum_bounding_geometry(input_layer, attribute.name(), Geometry.MINIMUM_ENCLOSING_CIRCLE)
    copy_layer(vl, output_layer)

# constructs convex hull around features
@timeit
def convex_hull(input_layer, output_layer, attribute):
    vl = minimum_bounding_geometry(input_layer, attribute.name(), Geometry.CONVEX_HULL)
    copy_layer(vl, output_layer)

# constructs intersection between horizontal flipped and baseline layer
# keep only one field from input and overlay layer
@timeit
def horizontal_flip(input_layer, output_layer, input_field, overlay_field):
    temp_clc_layer = build_layer(extract_gpkg(output_layer), 'temp_clc')

    vl = flip_layer(input_layer, FlipMode.FLIP_HORIZONTAL)
    copy_layer(vl, temp_clc_layer)

    input_name = input_field.name()
    overlay_name = overlay_field.name()
    vl = intersection_layers(input_layer, temp_clc_layer, input_fields=[input_name], overlay_fields=[overlay_name])
    
    # delete features which are not equal for overlay and input parameters
    with edit(vl):
        for f in vl.getFeatures():
            val1 = f[input_name]
            val2 = f[QGS.PREFIX + overlay_name]
            if val1 != val2:
                vl.deleteFeature(f.id())

    delete_attributes(vl, [QGS.PREFIX + overlay_name])
    copy_layer(vl, temp_clc_layer)

    vl = add_geometry(temp_clc_layer)
    copy_layer(vl, output_layer)

# constructs intersection between horizontal flipped and baseline layer
# keep only one field from input and overlay layer
@timeit
def vertical_flip(input_layer, output_layer, input_field, overlay_field):
    temp_clc_layer = build_layer(extract_gpkg(output_layer), 'temp_clc')

    vl = flip_layer(input_layer, FlipMode.FLIP_VERTICAL)
    copy_layer(vl, temp_clc_layer)

    input_name = input_field.name()
    overlay_name = overlay_field.name()
    vl = intersection_layers(input_layer, temp_clc_layer, input_fields=[input_name], overlay_fields=[overlay_name])
    
    # delete features which are not equal for overlay and input parameters
    with edit(vl):
        for f in vl.getFeatures():
            val1 = f[input_name]
            val2 = f[QGS.PREFIX + overlay_name]
            if val1 != val2:
                vl.deleteFeature(f.id())

    delete_attributes(vl, [QGS.PREFIX + overlay_name])
    copy_layer(vl, temp_clc_layer)

    vl = add_geometry(temp_clc_layer)
    copy_layer(vl, output_layer)
