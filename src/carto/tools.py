from shapely.geometry import mapping
import fiona

SCHEMA = {
    'geometry': 'Polygon',
    'properties': {'category': 'int'},
}

def json(what, filename):
    with fiona.open(filename, 'w', 'GeoJSON', SCHEMA) as c:
        for co in what.components():
            if type(co._polygon) == MultiPolygon:
                for p in co._polygon:
                    c.write({
                        'geometry': mapping(p),
                        'properties': {'category': co._category.value},
                    })
            else:
                c.write({
                    'geometry': mapping(co._polygon),
                    'properties': {'category': co._category.value},
                })