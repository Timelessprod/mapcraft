from carto.area import Area, Category

class Mansion(Area):
    def __init__(self, polygon):
        super().__init__(polygon=polygon, category=Category.MANSION)