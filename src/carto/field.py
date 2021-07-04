from carto.area import Area, Category

class Field(Area):
    """Representation of a field. Inherits from Area.

    :param polygon: The surface of the field.
    :type polygon: shapely.Polygon
    """
    def __init__(self, polygon):
        super().__init__(polygon=polygon, category=Category.FIELD)
