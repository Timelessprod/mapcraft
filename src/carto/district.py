from carto.house import House
import carto.tools as tools
from shapely.geometry import mapping, Polygon, Point, LineString, MultiPolygon
from carto.area import Area, Category
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import random
from shapely.ops import unary_union
from carto.street import Street
import matplotlib.pyplot as plt

class District(Area):
	@staticmethod
	def getRegionsPolygons(polygon):
		"""Uses the Voronoi algorithm to generate districts of a city and the roads between those districts.

		:return: The regions and road polygons
		:rtype: list(Polygon), Polygon
		"""

		N = 15
		radius = (N - 2)
		lineX= np.linspace(polygon.bounds[0], polygon.bounds[2], N)
		lineY = np.linspace(polygon.bounds[1], polygon.bounds[3], N)

		# 1. Generate points that are in a grid pattern and then randomly move them
		points = np.array([[x, y] for x in lineX for y in lineY if polygon.contains(Point(x, y))])


		points += np.random.random((len(points), 2)) * 1/2

		# 2. Voronoi algorithm will returns the areas closest to each points
		vor = Voronoi(points)

		regions = [r for r in vor.regions if -1 not in r and len(r) > 0]

		# 4. Make Polygons for each area
		regions = [Polygon([vor.vertices[i] for i in r]) for r in regions]

		# 5. Create a zone thats englobing the areas and only keep the areas fully in that zone
#		zone = Polygon((2 * np.random.random((8, 2)) - 1) *
		#		radius).convex_hull.buffer(radius/1)
		regions = [r for r in regions if polygon.contains(r)]

		x, y = polygon.exterior.xy
		plt.plot(x, y)
		for r in regions:
			plt.plot(*r.exterior.xy)
		plt.show()

		print(regions)
		# 6. agregate all the areas.
#		regionsFull = unary_union(regions)

		# 7. Shrink the areas to make room between them
#		regions = [region.buffer(-0.08) for region in regions]

		# 8. take the diff between the agregated non shrink areas and the shrinked areas, these will be the roads.
#		roads = regionsFull.difference(MultiPolygon(regions))

		return regions

	def __init__(self, polygon, category):
		regionsPoly  = District.getRegionsPolygons(polygon)
		# 2. We create the districts for each regions (these disticts will be split up themselves)
		#self.districts = [House(regionPoly) for regionPoly in regionsPoly]

		self._sub_areas = []

		# 3. We create the streets
		super().__init__(unary_union(regionsPoly), category=Category.COMPOSITE, sub_areas=self.districts)