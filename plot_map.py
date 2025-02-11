# import geopandas as gpd
# import matplotlib.pyplot as plt
#
# # Load the shapefile (replace with your actual file path)
# gdf = gpd.read_file('ex_sample.shp')
#
# # Plot the polygons
# gdf.plot()
# plt.show()

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
from data_loader import get_coord_from_postcode, get_postcode_from_name, get_df
from solve import solve

df = get_df()
driver_assignments = solve(df=df, verbose=True)

colors = [*mcolors.TABLEAU_COLORS.values()]

plt.figure()

for i, driver_name in enumerate(driver_assignments.keys()):
    driver_postcode = get_postcode_from_name(name=driver_name, df=df)
    driver_coords = get_coord_from_postcode(driver_postcode)
    plt.scatter(*driver_coords, c=colors[i], marker='x', label=driver_name)

    for passenger_name in driver_assignments[driver_name]:
        passenger_postcode = get_postcode_from_name(name=passenger_name, df=df)
        passenger_coords = get_coord_from_postcode(passenger_postcode)
        plt.scatter(*passenger_coords, c=colors[i])

plt.ylabel('Longitude')
plt.xlabel('Latitude')

plt.legend()
plt.grid(which='both')

plt.show()