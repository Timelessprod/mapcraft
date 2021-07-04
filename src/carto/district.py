from carto.house import House
import carto.tools as tools
from shapely.geometry import mapping, Polygon, Point, LineString, MultiPolygon, box
from carto.area import Area, Category
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import random
from shapely.ops import unary_union
from carto.street import Street
import matplotlib.pyplot as plt
from carto.voronoi import voronoi_finite_polygons_2d
from carto.mansion import Mansion
from carto.park import Park


class District(Area):
    @staticmethod
    def getRegionsPolygons(polygon):
        """Uses the Voronoi algorithm to generate districts of a city and the roads between those districts.

        :return: The regions and road polygons
        :rtype: list(Polygon), Polygon
        """

        N = 10
        radius = N

        lineX = np.linspace(polygon.bounds[0], polygon.bounds[2], N)
        lineY = np.linspace(polygon.bounds[1], polygon.bounds[3], N)

        # 1. Generate points that are in a grid pattern and then randomly move them
        points = np.array([[x, y] for x in lineX for y in lineY if polygon.contains(Point(x, y))])

        points += np.random.random((len(points), 2)) * (radius * 3)

        # 2. Voronoi algorithm will returns the areas closest to each points
        vor = Voronoi(points)

        regions, vertices = voronoi_finite_polygons_2d(vor)

        # 4. Make Polygons for each area
        regions = [Polygon([vertices[i] for i in r]) for r in regions]

        all_regions = unary_union(regions)
        b = box(*all_regions.bounds)
        b_minus_poly = b.difference(polygon)

        # 5. Create a zone thats englobing the areas and only keep the areas fully in that zone
        regions = [r.difference(b_minus_poly) for r in regions if r.difference(b_minus_poly).area != 0]

        # 6. agregate all the areas.
        #		regionsFull = unary_union(regions)

        # 7. Shrink the areas to make room between them
        regions = [region.buffer(-1) for region in regions]

        # 8. take the diff between the agregated non shrink areas and the shrinked areas, these will be the roads.
        #		roads = regionsFull.difference(MultiPolygon(regions))

        streets = polygon.difference(MultiPolygon(regions))

        return regions, [Street(streets)]

    @staticmethod
    def generate(polygon):
        regionsPoly, streets = District.getRegionsPolygons(polygon)

        number_of_mansions = random.randint(0, 5)
        mansion_ids = [random.randint(0, len(regionsPoly) - 1) for i in range(number_of_mansions)]

        number_of_parks = random.randint(0, 5)
        parks_id = [random.randint(0, len(regionsPoly) - 1) for i in range(number_of_parks)]

        houses = [House(regionPoly) for i, regionPoly in enumerate(regionsPoly) if i not in (mansion_ids + parks_id)]
        mansions = [Mansion(regionsPoly[i]) for i in mansion_ids]
        parks = [Park(regionsPoly[i]) for i in parks_id]

        return houses + mansions + parks, streets
