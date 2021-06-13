from carto import city
from carto import area
from carto import tools

from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from scipy.spatial import Voronoi
import numpy as np
import random

# Just using the given files to make polygons and make a city out of it
N = 5
radius = (N-2)
points = np.array([[x,y] for x in np.linspace(-1,1,N) for y in np.linspace(-1,1,N)])
points *= radius
points += np.random.random((len(points), 2)) * (radius / 2)
vor = Voronoi(points)

regions = [r for r in vor.regions if -1 not in r and len(r) > 0]
regions = [Polygon([vor.vertices[i] for i in r]) for r in regions]

zone = Polygon((2 * np.random.random((8,2)) - 1) * radius ).convex_hull.buffer(radius/1)
regions = [r for r in regions if zone.contains(r) ]

walls = MultiPolygon(regions).buffer(0.1, join_style=2) # 100 mètres entre les quartiers et les murs
city = MultiPolygon(regions)

sub_areas = [area.Area(r, random.choice(list(area.Category))) for r in regions]

city = area.Area(unary_union(city), area.Category.COMPOSITE, sub_areas=sub_areas)

tools.json(city, "./city/city.json")
