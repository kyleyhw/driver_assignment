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
import pandas as pd

filename = 'people.csv'

driver_assignments = {'a': ['aa', 'bb', 'ff'], 'b': ['cc', 'dd', 'ee']}
people = pd.read_csv(filename, delimiter=',', dtype='str')

plt.figure()

for driver in driver_assignments.keys():
    for passenger in driver_assignments.values():
        passnger_coords = people[people == passenger]['Longitude']
        plt.plot()

