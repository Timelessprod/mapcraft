from carto.area import Category


from carto.area import Area

class Street(Area):
	def __init__(self, streetPoly) -> None:
	    super().__init__(streetPoly, Category.STREET)