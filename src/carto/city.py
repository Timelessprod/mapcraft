from carto.area import Area, Category
from carto.district import District
from shapely.geometry import Point
from carto.street import Street
from carto.wall import Wall
from carto.voronoi import *


class City(Area):
    """This is the root class for the whole city, it will contain all the
    districs, the walls, the river, castle etc...

    :param population: Number of people living in the walls
    :type population: int
    :param density: Population density, defaults to 10000
    :type density: int, optional
    :param has_walls: Wether the city has walls around it or not, defaults to False
    :type has_walls: bool, optional
    :param has_castel: Wether the city has a castle inside it or not, defaults to False
    :type has_castel: bool, optional
    :param has_river: Wether the city has a river or not, defaults to False
    :type has_river: bool, optional
    """

    def __init__(self, population, density=10000, has_walls=False, has_castel=False, has_river=False):
        """Constructor Method
        """
        assert(density >= 2_000 and density <= 30_000)

        self.population = population
        self.density = density
        self.has_walls = has_walls
        self.has_castel = has_castel
        self.has_river = has_river

        # 1. We create the base of the city region polygons and streets
        regionsPoly, streetPoly, walls_poly= getRegionsPolygons(population=2_500_000, density=20_000)

        self.districts = []
        self.streets = [Street(streetPoly)]

        if has_walls:
            self.walls = [Wall(walls_poly)]
        else:
            self.walls = []

        epicentre_x = sum([r.centroid.x for r in regionsPoly]) // len(regionsPoly)
        epicentre_y = sum([r.centroid.y for r in regionsPoly]) // len(regionsPoly)

        # For each district, we generate what is inside (house, farms, etc)
        for r in regionsPoly:
            houses, streets = District.generate(r, Point(epicentre_x, epicentre_y))
            self.districts = self.districts + houses
            self.streets = self.streets + streets

        super().__init__(unary_union(regionsPoly), category=Category.COMPOSITE,
                         sub_areas=self.districts + self.streets + self.walls)
