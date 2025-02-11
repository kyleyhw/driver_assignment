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
from data_loader import get_coord_from_postcode

filename = 'people.csv'

driver_assignments = {'a': ['aa', 'bb', 'ff'], 'b': ['cc', 'dd', 'ee']}
people = pd.read_csv(filename, delimiter=',', dtype='str')

colors = [*mcolors.TABLEAU_COLORS.values()]

plt.figure()

for i, driver_name in enumerate(driver_assignments.keys()):
    driver_postcode = people[people['Name'] == driver_name]['Postcode'].item()
    driver_coords = get_coord_from_postcode(driver_postcode)
    plt.scatter(*driver_coords, c=colors[i], marker='x', label=driver_name)
    for passenger_name in driver_assignments[driver_name]:
        passenger_postcode = people[people['Name'] == passenger_name]['Postcode'].item()
        passenger_coords = get_coord_from_postcode(passenger_postcode)
        # print(passenger_postcode)
        plt.scatter(*passenger_coords, c=colors[i])

plt.legend()

plt.show()