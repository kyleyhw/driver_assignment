import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from data_loader import get_coord_from_postcode, get_postcode_from_name, get_df
from solve import solve
import contextily as ctx
from shapely.geometry import Point

people_information_dataframe = get_df()
driver_assignments = solve(people_information_dataframe=people_information_dataframe, verbose=True)

colors = [*mcolors.TABLEAU_COLORS.values()]

fig, ax = plt.subplots(1, 1)

all_coords = []

for i, driver_name in enumerate(driver_assignments.keys()):
    driver_postcode = get_postcode_from_name(name=driver_name, people_information_dataframe=people_information_dataframe)
    driver_coords = get_coord_from_postcode(driver_postcode)
    ax.scatter(*driver_coords, c=colors[i], marker='x', label=driver_name)
    all_coords.append(driver_coords)

    for passenger_name in driver_assignments[driver_name]:
        passenger_postcode = get_postcode_from_name(name=passenger_name, people_information_dataframe=people_information_dataframe)
        passenger_coords = get_coord_from_postcode(passenger_postcode)
        ax.scatter(*passenger_coords, c=colors[i])
        all_coords.append(passenger_coords)

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lon, lat in all_coords], crs="EPSG:4326")
# Convert to Web Mercator for contextily (EPSG:3857)
gdf = gdf.to_crs(epsg=3857)
# Add a basemap (choose a different provider if needed)
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, crs=gdf.crs)

ax.set_ylabel('Longitude')
ax.set_xlabel('Latitude')

ax.legend()
ax.grid(which='both')

plt.savefig('driver_assignment_plot.png')

plt.show()