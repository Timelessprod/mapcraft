from carto.area import Area, Category

class Mansion(Area):
    """Representation of a plot of a mansion. Inherits from Area.

    :param polygon: The surface of the mansion.
    :type polygon: shapely.Polygon
    """
    def __init__(self, polygon):
        super().__init__(polygon=polygon, category=Category.MANSION)