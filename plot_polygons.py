import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point
import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, LineString
from shapely.ops import polygonize
from pyproj import Transformer
import os

# Set a persistent cache directory
os.environ["CXT_CACHE_DIR"] = "./tile_cache"  # Change to any local directory

# Load the CSV file
csv_path = "cb_area_codes.csv"
df = pd.read_csv(csv_path)

# Inspect the first few rows
print(df.head())

postcode_header = 'Postcode'
longitude_header = 'Longitude'
latitude_header = 'Latitude'

# Convert DataFrame to GeoDataFrame (EPSG:4326 - WGS 84)
geometry = [Point(xy) for xy in zip(df[longitude_header], df[latitude_header])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Extract coordinates for Voronoi tessellation
coords = np.array(list(zip(gdf.geometry.x, gdf.geometry.y)))

# Compute Voronoi diagram
vor = Voronoi(coords)

# Convert Voronoi edges to polygons
lines = [LineString(vor.vertices[line]) for line in vor.ridge_vertices if -1 not in line]
polygons = list(polygonize(lines))

# Create a GeoDataFrame from polygons
voronoi_gdf = gpd.GeoDataFrame(geometry=polygons, crs="EPSG:4326")

# Assign postcodes to the polygons by spatial join (approximate matching)
gdf = gdf.set_geometry("geometry")
voronoi_gdf = voronoi_gdf.sjoin_nearest(gdf[[postcode_header, "geometry"]])

# Save the Voronoi postcode boundaries
voronoi_gdf.to_file("cambridge_postcode_boundaries.geojson", driver="GeoJSON")

# Reproject for correct map alignment
voronoi_gdf_3857 = voronoi_gdf.to_crs(epsg=3857)
gdf_3857 = gdf.to_crs(epsg=3857)

# Define bounding box in longitude & latitude
lon_min, lon_max = 0.08, 0.2
lat_min, lat_max = 52.15, 52.23

# Convert bounding box to EPSG:3857
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
x_min, y_min = transformer.transform(lon_min, lat_min)
x_max, y_max = transformer.transform(lon_max, lat_max)

# Plot results
fig, ax = plt.subplots(figsize=(10, 10))

# Plot Voronoi postcode boundaries
voronoi_gdf_3857.plot(ax=ax, edgecolor="black", facecolor="none", linewidth=1)

# Plot postcode centroids
gdf_3857.plot(ax=ax, markersize=5, color="red", alpha=0.5)

# Add basemap (correct projection)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=16)

# Set title
plt.title("Cambridge Postcode Boundaries (Voronoi)")

# Set correct map limits
ax.set_xlim([x_min, x_max])
ax.set_ylim([y_min, y_max])

# Convert axis labels back to Longitude & Latitude
def merc_to_lonlat(x, y):
    """Convert EPSG:3857 to EPSG:4326."""
    return transformer.transform(x, y)

xticks = ax.get_xticks()
yticks = ax.get_yticks()

ax.set_xticklabels([f"{merc_to_lonlat(x, y_min)[0]:.4f}" for x in xticks])
ax.set_yticklabels([f"{merc_to_lonlat(x_min, y)[1]:.4f}" for y in yticks])

# Set axis labels
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Show plot
plt.show()
