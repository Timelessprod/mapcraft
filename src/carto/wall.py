from carto.area import Area, Category

class Wall(Area):
    """Representation of a wall around the city. Inherits from Area.

    :param polygon: The surface of the wall.
    :type polygon: shapely.Polygon
    """
    def __init__(self, polygon):
        super().__init__(polygon=polygon, category=Category.WALL)