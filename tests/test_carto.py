from carto import __version__
import carto.city as city
import carto.area as area
import carto.tools as tools


def test_version():
    assert __version__ == '0.1.0'


def test_city():
    c = city.City(5000)
    tools.json(c, 'city/city.json')


def test_area():
    #>>> surf = Area(Polygon([(0,0), (20,0), (20,40), (0,40)]), Category.HOUSE)
    #>>> surf.split(0.5, 0, False)  # house takes 1/2 of surface and is north
    #(Category.HOUSE:POLYGON ((20 20, 20 0, 0 0, 0 20, 20 20)), Category.GARDEN:POLYGON ((0 20, 0 40, 20 40, 20 20, 0 20)))
    zone = area.Area(area.Polygon(
        [(0, 0), (10, 0), (15, 15), (-5, 10)]), area.Category.HOUSE)
    zone.split(0.4, 180, inplace=True)
    tools.json(zone, "./city/house.json")
    assert len(zone._sub_areas) == 2
