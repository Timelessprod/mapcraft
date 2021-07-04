from shapely.geometry import mapping, MultiPolygon
import fiona

SCHEMA = {
    'geometry': 'Polygon',
    'properties': {'category': 'int'},
}

def json(what, filename):
    """Function used to serialize an Area to a JSON file.

    :param what: The city or any surface.
    :type what: carto.Area
    :param filename: The path of the file where the JSON wil be serialized.
    :type filename: str
    """
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