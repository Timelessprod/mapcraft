from carto.area import Area, Category

class Park(Area):
    def __init__(self, polygon):
        super().__init__(polygon=polygon, category=Category.PARK)