# `plot_polygons.py` Documentation

This script is a utility for creating and visualizing postcode boundaries using Voronoi tessellation. It is not a part of the main driver assignment workflow but can be used for geographical analysis of the postcode data.

## Libraries Used

- `pandas`: For reading the CSV data.
- `geopandas`: For working with geospatial data.
- `matplotlib`: For plotting.
- `contextily`: For adding a basemap.
- `shapely`: For geometric objects and operations.
- `scipy`: For Voronoi tessellation.
- `pyproj`: For coordinate transformations.

## Script Logic

1.  **Load Data**: It loads the `cb_area_codes.csv` file, which contains postcode centroids (longitude and latitude).

2.  **Voronoi Tessellation**: It uses `scipy.spatial.Voronoi` to compute a Voronoi diagram from the postcode centroids. A Voronoi diagram is a partitioning of a plane into regions based on distance to points in a specific subset of the plane. For each postcode centroid, there will be a corresponding region consisting of all points closer to that centroid than to any other.

3.  **Create Polygons**: The edges of the Voronoi diagram are converted into `shapely.geometry.Polygon` objects.

4.  **Create GeoDataFrame**: A `geopandas.GeoDataFrame` is created from the Voronoi polygons. The postcodes are then assigned to these polygons using a spatial join (`sjoin_nearest`).

5.  **Save Boundaries**: The resulting postcode boundaries are saved as a GeoJSON file named `cambridge_postcode_boundaries.geojson`.

6.  **Plotting**: The script then plots the Voronoi polygons on a map. It also plots the original postcode centroids. A basemap from OpenStreetMap is added for context.

This script is a good example of how to use Voronoi tessellation to create service areas or boundaries from a set of points. The resulting GeoJSON file could be used in other GIS applications.
