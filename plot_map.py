import geopandas as gpd
import matplotlib.pyplot as plt

# Load the shapefile (replace with your actual file path)
gdf = gpd.read_file('ex_sample.shp')

# Plot the polygons
gdf.plot()
plt.show()