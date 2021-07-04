from carto.area import Area, Category

class Garden(Area):
    """Representation of a garden. Inherits from Area.

    :param polygon: The surface of the garden.
    :type polygon: shapely.Polygon
    """
    def __init__(self, polygon):
        super().__init__(polygon=polygon, category=Category.GARDEN)
