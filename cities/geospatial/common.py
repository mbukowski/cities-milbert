import re

# returns gpkg path based on root folder, gpkg location and gpkg name
def build_gpkg(root, location, name):
    return f'{root}{location}/{name}'

# returns layer path based on gpkg and layer name
def build_layer(gpkg, name):
    return f'{gpkg}|layername={name}'

# returns a db connection to gpkg layer
def build_db(layer):
    return f'ogr:dbname="{extract_gpkg(layer)}" table="{extract_layer_name(layer)}" (geom)' 

# extracts gpkg path from layer path
def extract_gpkg(layer):
    p = re.compile('(.*)\\|layername')
    m = p.match(layer)

    return m.group(1)

# extracts gpkg name from layer or gpkg path
def extract_gpkg_name(layer):
    arr = layer.split('/')
    s = arr[len(arr) - 1]

    p = re.compile('(.*)\\.gpkg')
    m = p.match(s)

    return m.group(1)

# extracts layer name from layer path
def extract_layer_name(layer):
    p = re.compile('.*\\|layername=(.*)')
    m = p.match(layer)

    return m.group(1)

