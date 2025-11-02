# `plot_map.py` Documentation

This script is responsible for visualizing the results of the driver assignment. It plots the locations of drivers and their assigned passengers on a map of Cambridge.

## Libraries Used

- `geopandas`: For working with geospatial data.
- `matplotlib`: For creating the plot.
- `contextily`: For adding a basemap to the plot.
- `shapely`: For creating `Point` objects from coordinates.
- `pyproj`: For coordinate system transformations.

## Script Logic

1.  **Load Data**: The script starts by loading the `people.csv` data and solving the driver assignment problem using `solve.py` to get the `driver_assignments` dictionary.

2.  **Coordinate Transformation**: It sets up a projection transformation to convert the WGS84 (latitude, longitude) coordinates to the Web Mercator projection (EPSG:3857), which is used by many web mapping services.

3.  **Plotting**: It iterates through the `driver_assignments` dictionary. For each driver, it:
    - Gets the driver's coordinates and transforms them to Web Mercator.
    - Plots the driver's location on the map with a unique color and a marker (an 'x').
    - Then, it iterates through the passengers assigned to that driver, gets and transforms their coordinates, and plots their locations with the same color as the driver.

4.  **Basemap**: It uses `contextily` to add a basemap from OpenStreetMap to the plot. This provides geographical context to the plotted points.

5.  **Final Touches**: It sets the axis labels, adds a legend to identify the drivers, and saves the plot as `driver_assignment_plot.png`.

This script provides a clear and intuitive way to visualize the solution to the driver assignment problem, making it easy to see which passengers are assigned to which driver and their relative locations.
