from carto.area import Area, Category

class District(Area):
	def __init__(self, polygon, category):
		super().__init__(polygon=polygon, category=category)
		self.components = []