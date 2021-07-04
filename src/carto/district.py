from carto.area import Area, Category
from shapely.ops import unary_union
from carto.house import House
from carto.street import Street
from carto.mansion import Mansion
from carto.park import Park
from carto.farm import Farm
from carto.garden import Garden
from carto.field import Field
from carto.land import Land
from carto.voronoi import *
import random


class District(Area):

    @staticmethod
    def generate(polygon, centerPoint):
        """Will generate the composents of a district represented by the polygon.

        :param polygon: The polygon of the district, all components will be inside of that polygons.
        :type polygon: shapely.Polygon
        :param centerPoint: The center point of the city, used to know where the district is in the city
        :type centerPoint: shapely.Point
        :return: a list of all the elements in the district (houses, mansions etc..), as well as the streets in the districts
        :rtype: tuple(list(carto.Area), list(carto.Area))
        """
        if (centerPoint.distance(polygon.centroid) > 170):
            regionsPoly, _ = splitDistrictPolygon(polygon, has_streets=False)

            nb_houses = random.randint(1, 5)
            houses_id = [random.randint(0, len(regionsPoly) - 1) for i in range(nb_houses)]
            houses = [Farm(regionsPoly[i]) for i in houses_id]

            nb_fields = random.randint(3, 10)
            fields_id = [random.randint(0, len(regionsPoly) - 1) for i in range(nb_fields)]
            fields = [Land(regionsPoly[i]) for i in fields_id]

            land = [Field(poly) for i, poly in enumerate(regionsPoly) if i not in (houses_id + fields_id)]

            return fields + houses + land, []

        regionsPoly, streets = splitDistrictPolygon(polygon)
        number_of_mansions = random.randint(0, 5)
        mansion_ids = [random.randint(0, len(regionsPoly) - 1) for i in range(number_of_mansions)]

        number_of_parks = random.randint(0, 5)
        parks_id = [random.randint(0, len(regionsPoly) - 1) for i in range(number_of_parks)]

        mansions = [Mansion(regionsPoly[i]) for i in mansion_ids]
        parks = [Park(regionsPoly[i]) for i in parks_id]

        houses_garden_poly = [make_inside_garden(poly) for i, poly in enumerate(regionsPoly) if i not in (mansion_ids + parks_id)]
        houses = [House(poly[0]) for i, poly in enumerate(houses_garden_poly)]
        gardens = [Garden(poly[1]) for i, poly in enumerate(houses_garden_poly)]

        return houses + mansions + parks + gardens, [Street(streets)]
