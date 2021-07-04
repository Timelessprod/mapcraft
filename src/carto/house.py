from carto.area import Area, Category

class House(Area):
    """Representation of a house. Inherits from Area.

    :param polygon: The surface of the house
    :type polygon: shapely.Polygon
    """
    def __init__(self, polygon):
        super().__init__(polygon=polygon, category=Category.HOUSE)
