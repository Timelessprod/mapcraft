from shapely.geometry import mapping, Polygon, Point, LineString, MultiPolygon, box
from shapely.ops import unary_union
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
import numpy as np
import math

def make_inside_garden(poly):
    """Take a poly and carv a hole inside it.

    :param poly: The original shape
    :type poly: shapely.Polygon
    :return: the old poly as well as the new inside polygon.
    :rtype: shapely.Polygon, shapely.Polygon
    """
    inside_poly = poly.buffer(-6)
    return poly, inside_poly

def splitDistrictPolygon(polygon, has_streets=True):
    """Take a surface represented by polygon and splits it and sub areas using Voronoir algorithm.

    :param polygon: The surface to split.
    :type polygon: shapely.Polygon
    :param has_streets: Wether we want space between the sub areas or no, defaults to True
    :type has_streets: bool, optional
    :return: return a list containing all the new polygons of the new areas and possibly the new streets.
    :rtype: list(shapely.Polygon), list(shapely.Polygon)
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

    # 7. Shrink the areas to make room between them
    if (has_streets):
        regions = [region.buffer(-1.3) for region in regions]
        # 8. take the diff between the agregated non shrink areas and the shrinked areas, these will be the roads.
        streets = polygon.difference(MultiPolygon(regions))

        return regions, streets
    return regions, None

def getRegionsPolygons(population=20_000_000, density=10_000):
    """Create a region separated in districts with streets between them.

    :param population: Population inside the city., defaults to 20_000_000
    :type population: int, optional
    :param density: population density, defaults to 10_000
    :type density: int, optional
    :return: A list of the new shape representing the district as well as the streets and the walls
    :rtype: list(shapely.polygon), list(shapely.polygon), list(shapely.Polygon)
    """
    surface = (population // density) * 1_000

    l = math.sqrt(surface)
    N = int(l) // 60

    if N == 0:
        N = 1

    radius = N

    # 1. Generate points that are in a grid pattern and then randomly move them
    points = np.array([[x, y] for x in np.linspace(-l, l, N)
                       for y in np.linspace(-l, l, N)])

    points += np.random.random((len(points), 2)) * (radius * 19)

    # 2. Voronoi algorithm will returns the areas closest to each points
    vor = Voronoi(points)

    # 3. Keep only the areas that are not on the edge of the plot
    regions = [r for r in vor.regions if - 1 not in r and len(r) > 0]

    # 4. Make Polygons for each area
    regions = [Polygon([vor.vertices[i] for i in r]) for r in regions]

    # 5. Create a zone thats englobing the areas and only keep the areas fully in that zone
    zone = Polygon((2 * np.random.random((8, 2)) - 1) * radius).convex_hull.buffer(radius * 65)
    regions = [r for r in regions if zone.contains(r)]

    # 6. agregate all the areas.
    regionsFull = unary_union(regions)

    walls = MultiPolygon(regions).buffer(5, join_style=2)
    walls = walls.difference(regionsFull)

    # 7. Shrink the areas to make room between them
    regions = [region.buffer(-2.5) for region in regions]

    # 8. take the diff between the agregated non shrink areas and the shrinked areas, these will be the roads.
    roads = regionsFull.difference(MultiPolygon(regions))

    return regions, roads, walls

def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.

    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.

    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.

    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1] # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)