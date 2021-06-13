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
    @staticmethod
    def getRegionsPolygons():
        N = 5
        radius = (N-2)
        points = np.array([[x,y] for x in np.linspace(-1,1,N) for y in np.linspace(-1,1,N)])
        points *= radius
        points += np.random.random((len(points), 2)) * (radius / 2)
        vor = Voronoi(points)
        regions = [r for r in vor.regions if -1 not in r and len(r) > 0]
        regions = [Polygon([vor.vertices[i] for i in r]) for r in regions]
        zone = Polygon((2 * np.random.random((8,2)) - 1) * radius ).convex_hull.buffer(radius/1)
        regions = [r for r in regions if zone.contains(r)]
        regionsFull = unary_union(regions)
        regions = [region.buffer(-0.08) for region in regions]
        roads = regionsFull.difference(MultiPolygon(regions))
        return regions, roads

    def __init__(self, population, density=10000, has_walls=False, has_castel=False, has_river=False):

        self.population = population
        self.density = density   # 10 000 ha/km2 par défaut mais peut baisser à 2000 ha/km2 avec les champs et monter à 30000 ha/km2
        self.has_walls = has_walls
        self.has_castel = has_castel
        self.has_river = has_river

        regionsPoly, streetPoly = City.getRegionsPolygons()
        self.districts = [District(regionPoly, random.choice(list(Category))) for regionPoly in regionsPoly]
        self.streets = Street(streetPoly)

        super().__init__(unary_union(regionsPoly), category=Category.STREET, sub_areas=self.districts + [self.streets])

