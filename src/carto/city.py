from re import A
import re
from carto.district import District
import carto.tools as tools
from shapely.geometry import mapping, Polygon, Point, LineString, MultiPolygon
from carto.area import Area, Category
from scipy.spatial import Voronoi
import numpy as np
import random
from shapely.ops import unary_union
from carto.street import Street


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

    @staticmethod
    def getRegionsPolygons():
        """Uses the Voronoi algorithm to generate districts of a city and the roads between those districts.

        :return: The regions and road polygons
        :rtype: list(Polygon), Polygon
        """
        N = 5
        radius = (N - 2)

        # 1. Generate points that are in a grid pattern and then randomly move them
        points = np.array([[x, y] for x in np.linspace(-1, 1, N)
                          for y in np.linspace(-1, 1, N)])
        points *= radius
        points += np.random.random((len(points), 2)) * (radius / 2)

        # 2. Voronoi algorithm will returns the areas closest to each points
        vor = Voronoi(points)

        # 3. Keep only the areas that are not on the edge of the plot
        regions = [r for r in vor.regions if - 1 not in r and len(r) > 0]

        # 4. Make Polygons for each area
        regions = [Polygon([vor.vertices[i] for i in r]) for r in regions]

        # 5. Create a zone thats englobing the areas and only keep the areas fully in that zone
        zone = Polygon((2 * np.random.random((8, 2)) - 1) *
                       radius).convex_hull.buffer(radius/1)
        regions = [r for r in regions if zone.contains(r)]

        # 6. agregate all the areas.
        regionsFull = unary_union(regions)

        # 7. Shrink the areas to make room between them
        regions = [region.buffer(-0.08) for region in regions]

        # 8. take the diff between the agregated non shrink areas and the shrinked areas, these will be the roads.
        roads = regionsFull.difference(MultiPolygon(regions))

        return regions, roads

    def __init__(self, population, density=10000, has_walls=False, has_castel=False, has_river=False):
        """Constructor Method
        """

        self.population = population
        # 10 000 ha/km2 par défaut mais peut baisser à 2000 ha/km2 avec les champs et monter à 30000 ha/km2
        self.density = density
        self.has_walls = has_walls
        self.has_castel = has_castel
        self.has_river = has_river

        # 1. We create the base of the city region polygons and streets
        regionsPoly, streetPoly = City.getRegionsPolygons()

        # 2. We create the districts for each regions (these disticts will be split up themselves)
        self.districts = [District(regionPoly, Category.HOUSE) for regionPoly in regionsPoly]

        # 3. We create the streets
        self.streets = Street(streetPoly)

        super().__init__(unary_union(regionsPoly), category=Category.COMPOSITE,
                         sub_areas=self.districts + [self.streets])
