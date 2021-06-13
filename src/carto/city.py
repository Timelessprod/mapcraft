import carto.tools as tools
from shapely.geometry import mapping, Polygon, Point, LineString, MultiPolygon
from carto.area import Area, Category

class City(Area):
    def __init__(self, population, density=10000, has_walls=False, has_castel=False, has_river=False):
        super().__init__(Polygon([(0,0), (10,0), (15,15), (-5,10)]), Category.COMPOSITE)
        self.population = population
        self.density = density   # 10 000 ha/km2 par défaut mais peut baisser à 2000 ha/km2 avec les champs et monter à 30000 ha/km2
        self.has_walls = has_walls
        self.has_castel = has_castel
        self.has_river = has_river
        self.districts = []
        ...

if __name__ == "__main__":
    city = City(5000)
    tools.json(city, '/tmp/city.json')