from carto.area import Category

from carto.area import Area

class Street(Area):
	"""Representation of a plot of the streets. Inherits from Area.

	:param polygon: The surface of the streets.
	:type polygon: shapely.Polygon
	"""
	def __init__(self, streetPoly) -> None:
		super().__init__(streetPoly, Category.STREET)