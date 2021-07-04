from carto.area import Area, Category

class Park(Area):
    """Representation of a plot of a park. Inherits from Area.

    :param polygon: The surface of the park.
    :type polygon: shapely.Polygon
    """
    def __init__(self, polygon):
        super().__init__(polygon=polygon, category=Category.PARK)