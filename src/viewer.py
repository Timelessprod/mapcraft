import matplotlib.pylab as plt
from matplotlib.colors import ListedColormap
import geopandas as gpd
import sys

try:
    filename = sys.argv[1]
except:
    filename = '/tmp/house.json'

colors_dic = {1:[0.9,0.9,0.2, 1],
              2:[1, 1, 0.5, 1],
              3:[0.25, 0.6, 0.25, 1],
              4:[0.25, 0.75, 0.9, 1],
              8:[0.8, 0.9, 0.55, 1],
              10:[0.85, 0.55, 0.25, 1],
              11:[0.95, 0.9, 0.8, 1],
              12:[0.85, 0.5, 0.85, 1],
              31:[0.4, 0.4, 0.4, 1],
              32:[0.6, 0.6, 0.6, 1],
              33:[1, 0.95, 0.6, 1],
              }
colors = [[1,0,0,1] for _ in range(max(colors_dic.keys())+1)]
for i in colors_dic:
    colors[i] = colors_dic[i]
color_map = ListedColormap(colors, name='Archi')

shapes = gpd.read_file(filename)
shapes.plot(column='category', cmap=color_map,
            k=len(colors)+1, vmin=0, vmax=len(colors),
            edgecolor='black')
plt.show()
