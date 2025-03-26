import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import contextily as ctx
import xyzservices.providers as xyz
from shapely.geometry import Point
from pyproj import Proj

from data_loader import get_coords_from_name, get_df
from solve import solve
from misc_funcs import translate_coordinates


wgs84 = Proj(init="epsg:4326")  # WGS84 (latitude, longitude)
web_mercator = Proj(init="epsg:3857")  # Web Mercator (meters)
longlat_to_webmercator = translate_coordinates(input_coordinate_system=wgs84, output_coordinate_system=web_mercator).translate


people_information_dataframe = get_df()
driver_assignments = solve(people_information_dataframe=people_information_dataframe, verbose=True)

colors = [*mcolors.TABLEAU_COLORS.values()]

fig, ax = plt.subplots(1, 1)

all_coords = []

for i, driver_name in enumerate(driver_assignments.keys()):
    driver_coords = get_coords_from_name(name=driver_name, people_information_dataframe=people_information_dataframe)
    driver_coords_mercator = longlat_to_webmercator(*driver_coords)
    ax.scatter(*driver_coords_mercator, c=colors[i], marker='x', label=driver_name)
    all_coords.append(driver_coords_mercator)

    for passenger_name in driver_assignments[driver_name]:
        passenger_coords = get_coords_from_name(name=passenger_name, people_information_dataframe=people_information_dataframe)
        passenger_coords_mercator = longlat_to_webmercator(*passenger_coords)
        ax.scatter(*passenger_coords_mercator, c=colors[i])
        all_coords.append(passenger_coords_mercator)

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lon, lat in all_coords], crs="EPSG:3857")

# Add a basemap (choose a different provider if needed)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=gdf.crs, zoom='auto')
# ctx.add_basemap(ax, source=xyz.OpenStreetMap.HOT, crs=gdf.crs, zoom='auto')

ax.set_ylabel('Y coordinate (Web Mercator)')
ax.set_xlabel('X coordinate (Web Mercator)')

ax.legend()
ax.grid(which='both')

plt.savefig('driver_assignment_plot.png')

plt.show()