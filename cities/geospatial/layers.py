from common.utils import *
from geospatial.common import *
from geospatial.globals import *

from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsCoordinateTransformContext, QgsField
from qgis.analysis import *
from PyQt5.QtCore import *
from processing.core.Processing import *

from shapetools import *


# creates an empty layer
def create_layer(template_layer, output_layer, action=QgsVectorFileWriter.CreateOrOverwriteLayer):
    template_vl = get_vl(template_layer)

    transform_context = QgsCoordinateTransformContext()

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.actionOnExistingFile = action
    options.driverName = 'GPKG'
    options.fileEncoding = 'UTF-8'
    options.layerName = extract_layer_name(output_layer)

    schema = template_vl.fields()
    geom = template_vl.wkbType()
    crs = template_vl.sourceCrs()
    
    QgsVectorFileWriter.create(extract_gpkg(output_layer), schema, geom, crs, transform_context, options)

# appends whole layer to existing layer (must exist), both have to have the same schema
def append_layer(input_layer, output_layer, selected_features=False, action=QgsVectorFileWriter.AppendToLayerNoNewFields):
    input_vl = get_vl(input_layer)

    transform_context = input_vl.transformContext()

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.actionOnExistingFile = action
    options.driverName = 'GPKG'
    options.fileEncoding = 'UTF-8'
    options.layerName = extract_layer_name(output_layer)
    options.onlySelectedFeatures = selected_features

    QgsVectorFileWriter.writeAsVectorFormatV3(input_vl, extract_gpkg(output_layer), transform_context, options)

# deletes all features from target layer - longer and error prone solution than clean_db 
def clean_layer(layer):
    vl = QgsVectorLayer(layer)
    with edit(vl):
        for f in vl.getFeatures():
            vl.deleteFeature(f.id())

# drops layer_db
def clean_db(layer):
    layer_name = extract_layer_name(layer)
    params = {
        'DATABASE': layer,
        'SQL': f'DELETE FROM {layer_name}'
    }
    processing.run('native:spatialiteexecutesql', params)

# renames layer_db
def rename_db(layer, from_table, to_table):
    params = {
        'DATABASE': layer,
        'SQL': f'ALTER TABLE {from_table} RENAME TO {to_table}'
    }
    processing.run('native:spatialiteexecutesql', params)    

# returns list of layers for given geopackage
def gpkg_layers(gpkg):
    geo_vl = QgsVectorLayer(gpkg, 'geo', 'ogr')
    list = []

    for sublayer in geo_vl.dataProvider().subLayers():
        table_name = sublayer.split('!!::!!')[1]
        list.append(table_name)

    return list

# returns a QGSField for given layer
def field_by_name(layer, name):
    for field in layer.fields():
        if field.name() == name: return field

    return None

# adds attribute QGSField to existing layer
def add_attributes(layer, new_fields):
    vl = get_vl(layer)
    dp = vl.dataProvider()

    arr = []
    for new_field in new_fields:
        field_name = new_field.name()
        field_index = vl.fields().indexFromName(field_name)
        
        # -1 means a field with given name is not present in the layer
        if field_index != -1:
            print(f'Field \'{field_name}\' already exists in layer {layer} - skipping')
            continue    
        
        arr.append(new_field)

    if len(arr) > 0:
        dp.addAttributes(arr)
        vl.updateFields()

# removes attributes QGSField from existing layer
def delete_attributes(layer, fields):
    vl = get_vl(layer)

    arr = []
    for field in fields:
        if isinstance(field, QgsField):
            field_name = field.name()
        else:
            field_name = field
            
        field_index = vl.fields().indexFromName(field_name)
        arr.append(field_index)

    with edit(vl):
        vl.deleteAttributes(arr)
        vl.updateFields()

# packages input layer and stores to specified geopackage layer
def package_layer(layers, output, overwrite=False, save_styles=True, save_metadata=True, selected_features_only=True, export_related_layers=False):
    params = {
        'LAYERS': layers,
        'OUTPUT': output,
        'OVERWRITE': overwrite,
        'SAVE_STYLES': save_styles,
        'SAVE_METADATA': save_metadata,
        'SELECTED_FEATURES_ONLY': selected_features_only,
        'EXPORT_RELATED_LAYERS': export_related_layers
    }

    result = processing.run('native:package', params)
    return result_vl(result, output)


# this function doesn't need to be still here, we are already having this functionality with append_layer
# copies features between two layers, keep in mind both schemas must be the same
# output layer must be empty
def copy_features(input_layer, output_layer):
    input_vl = get_vl(input_layer)
    output_vl = get_vl(output_layer)

    if output_vl.featureCount() > 0:
        print('Can\'t copy features, output layer is not empty')
        exit()
    
    input_vl = reindex(input_vl) # no chyba ze to ponizej to trzeba zrobic z dpk 

    fid = 1
    output_dp = output_vl.dataProvider() # shouldn't this be inside edit?
    for feature in input_vl.getFeatures():
        with edit(output_vl):
            feature['fid'] = fid
            output_dp.addFeature(feature)
            fid += 1

    return output_vl


# reindexes IDs for given input layer
def reindex(layer):
    vl = get_vl(layer)

    fid = 1
    for feature in vl.getFeatures():
        feature['fid'] = fid
        fid += 1

    return vl

# gets vector layer either directly or by converting to an object
def get_vl(layer):
    if isinstance(layer, QgsVectorLayer):
        return layer
    
    return QgsVectorLayer(layer, extract_layer_name(layer), 'ogr')

# converts result to vector layer based on an output parameter
def result_to_vl(result, output, key='OUTPUT'):
    if output == QGS.MEMORY:
        return result[key]

    return QgsVectorLayer(output, 'output_layer', 'ogr')

# clips input layer on the outline layer and stores to specified geopackage in layer
def clip_layer(input, overlay, output=QGS.MEMORY):
    params = {
        'INPUT': input,
        'OVERLAY': overlay,
        'OUTPUT': output
    }

    result = processing.run('native:clip', params)
    return result_to_vl(result, output)

# merge all features for given input layer
# keep disjointed separate - we will be counting their area and compare to general one
# group them by provided list of fields
def dissolve_layer(input, output=QGS.MEMORY, fields=[], separate_disjoint=True):
    params = {
        'INPUT': input,
        'FIELD': fields,
        'SEPARATE_DISJOINT': separate_disjoint,
        'OUTPUT': output
    }
  
    result = processing.run('native:dissolve', params)
    return result_to_vl(result, output)

# filters existing layer to a new one based on provided expresion
def filter_by_expression(input, output, expression):
    params = {
        'INPUT': input,
        'EXPRESSION': expression,
        'OUTPUT': output
    }

    result = processing.run('native:extractbyexpression', params)
    return result_to_vl(result, output)

# adds a geometry to input layer and saves
def add_geometry(input, output=QGS.MEMORY):
    params = {
        'INPUT': input,
        'CALC_METHOD': 0,
        'OUTPUT': output
    }

    result = processing.run('qgis:exportaddgeometrycolumns', params)
    return result_to_vl(result, output)

# for each feature creates minimum bounding geometry
def minimum_bounding_geometry(input, attribute='', geometry_type=Geometry.BOUNDING_BOX, output=QGS.MEMORY):
    params = {
        'INPUT': input,
        'FIELD': attribute,
        'TYPE': geometry_type,
        'OUTPUT': output
    }

    result = processing.run('qgis:minimumboundinggeometry', params)
    return result_to_vl(result, output)

# creates intersection between input and output layer
def intersection_layers(input, overlay, input_fields=[], overlay_fields=[], prefix=QGS.PREFIX, output=QGS.MEMORY, grid_size=None):
    params = {
        'INPUT': input,
        'OVERLAY': overlay,
        'INPUT_FIELDS': input_fields,
        'OVERLAY_FIELDS': overlay_fields,
        'OVERLAY_FIELDS_PREFIX': prefix,
        'OUTPUT': output,
        'GRID_SIZE': grid_size
    }    
    
    result = processing.run('native:intersection', params)
    return result_to_vl(result, output)     

# to use flip layer algorithms we have to install shepetools plugin
def flip_layer(input, flip_mode=FlipMode.FLIP_HORIZONTAL, output=QGS.MEMORY):
    params = {
        'InputLayer': input,
        'FlipMode': flip_mode,
        'OutputLayer': output
    }

    result = processing.run('shapetools:geodesicflip', params)
    return result_to_vl(result, output, key='OutputLayer')
