from carto.area import Area, Category

class Land(Area):
    """Representation of a plot of land. Inherits from Area.

    :param polygon: The surface of the land.
    :type polygon: shapely.Polygon
    """
    def __init__(self, polygon):
        super().__init__(polygon=polygon, category=Category.LAND)
