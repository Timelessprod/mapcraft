from shapely.geometry import mapping, MultiPolygon
import fiona

def json(what, filename):
    schema = {
        'geometry': 'Polygon',
        'properties': {'category': 'int'},
    }
    with fiona.open(filename, 'w', 'GeoJSON', schema) as c:
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