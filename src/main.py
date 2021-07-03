from carto import city
from carto import area
from carto import tools

from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from scipy.spatial import Voronoi
import numpy as np
import random

city = city.City(100)
tools.json(city, "./city/city.json")