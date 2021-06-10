from shapely.geometry import mapping
import fiona

def json(what, filename):
    schema = {
        'geometry': 'Polygon',
        'properties': {'category': 'int'},
    }
    with fiona.open(filename, 'w', 'GeoJSON', schema) as c:
        for co in what.components():
            c.write({
                'geometry': mapping(co._polygon),
                'properties': {'category': co._category.value},
            })
