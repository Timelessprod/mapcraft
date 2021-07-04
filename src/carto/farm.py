from carto.area import Area, Category

class Farm(Area):
    """Representation of a farm. Inherits from Area.

    :param polygon: The surface of the farm.
    :type polygon: shapely.Polygon
    """
    def __init__(self, polygon):
        super().__init__(polygon=polygon, category=Category.FARM)