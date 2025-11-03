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


def plot_driver_routes(driver_assignments, driver_names, driver_coords_raw, passenger_names_raw, passenger_coords_raw, output_filename='driver_assignment_plot.png'):
    """
    Plots the driver assignments, including pickup order with arrows, and a legend.

    Args:
        driver_assignments (dict): Dictionary containing driver assignments, routes, and distances.
                                   Format: {driver_name: {"passengers": [...], "route": [...], "total_route_distance": float}}
        driver_names (list): List of driver names.
        driver_coords_raw (list): List of (lon, lat) tuples for drivers, corresponding to driver_names.
        passenger_names_raw (list): List of (lon, lat) tuples for passengers, corresponding to passenger_names_raw.
        output_filename (str): Name of the file to save the plot.
    """
    colors = [*mcolors.TABLEAU_COLORS.values()]
    
    # Create mappings for easy coordinate lookup
    driver_coords_map = {name: coord for name, coord in zip(driver_names, driver_coords_raw)}
    passenger_coords_map = {name: coord for name, coord in zip(passenger_names_raw, passenger_coords_raw)}

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    all_coords_mercator = []
    
    # Plot drivers and passengers, and draw routes
    for i, driver_name in enumerate(driver_names):
        driver_raw_coord = driver_coords_map[driver_name]
        driver_mercator_coord = longlat_to_webmercator(*driver_raw_coord)
        
        # Plot driver
        ax.scatter(*driver_mercator_coord, c=colors[i % len(colors)], marker='X', s=100, zorder=5, label=f'Driver {driver_name}')
        all_coords_mercator.append(driver_mercator_coord)

        assigned_passengers_for_driver = driver_assignments.get(driver_name, {}).get("passengers", [])
        route_for_driver = driver_assignments.get(driver_name, {}).get("route", [])

        if route_for_driver:
            current_location_mercator = driver_mercator_coord
            
            for passenger_in_route_name in route_for_driver:
                passenger_raw_coord = passenger_coords_map[passenger_in_route_name]
                passenger_mercator_coord = longlat_to_webmercator(*passenger_raw_coord)
                
                # Plot passenger
                ax.scatter(*passenger_mercator_coord, c=colors[i % len(colors)], marker='o', s=70, zorder=4)
                all_coords_mercator.append(passenger_mercator_coord)

                # Draw arrow from current location to next passenger
                ax.annotate('', xy=passenger_mercator_coord, xytext=current_location_mercator,
                            arrowprops=dict(facecolor=colors[i % len(colors)], shrink=0.05, width=1, headwidth=8, headlength=10),
                            zorder=3)
                
                current_location_mercator = passenger_mercator_coord
        elif assigned_passengers_for_driver: # Driver has assigned passengers but no route (e.g., only one passenger)
             passenger_raw_coord = passenger_coords_map[assigned_passengers_for_driver[0]]
             passenger_mercator_coord = longlat_to_webmercator(*passenger_raw_coord)
             ax.scatter(*passenger_mercator_coord, c=colors[i % len(colors)], marker='o', s=70, zorder=4)
             all_coords_mercator.append(passenger_mercator_coord)
             ax.annotate('', xy=passenger_mercator_coord, xytext=driver_mercator_coord,
                            arrowprops=dict(facecolor=colors[i % len(colors)], shrink=0.05, width=1, headwidth=8, headlength=10),
                            zorder=3)


    # Create a GeoDataFrame for basemap extent
    if all_coords_mercator:
        gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lon, lat in all_coords_mercator], crs="EPSG:3857")
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=gdf.crs, zoom='auto')
    else:
        # If no points to plot, just add a default basemap
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs="EPSG:3857", zoom=10)


    ax.set_ylabel('Y coordinate (Web Mercator)')
    ax.set_xlabel('X coordinate (Web Mercator)')

    # Custom Legend
    from matplotlib.lines import Line2D
    legend_elements = []
    for i, driver_name in enumerate(driver_names):
        legend_elements.append(Line2D([0], [0], marker='X', color='w', label=f'Driver {driver_name}',
                                      markerfacecolor=colors[i % len(colors)], markersize=10))
    
    # Add generic legend entries for Driver and Passenger symbols
    legend_elements.append(Line2D([0], [0], marker='X', color='w', label='Driver Location',
                                  markerfacecolor='gray', markersize=10))
    legend_elements.append(Line2D([0], [0], marker='o', color='w', label='Passenger Location',
                                  markerfacecolor='gray', markersize=7))

    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
    ax.grid(which='both')
    plt.tight_layout() # Adjust layout to prevent legend from overlapping
    plt.savefig(output_filename)
    plt.show()


if __name__ == '__main__':
    people_information_dataframe = get_df()
    driver_assignments, driver_names, driver_coords, passenger_names, passenger_coords = solve(people_information_dataframe=people_information_dataframe, verbose=True)
    
    plot_driver_routes(driver_assignments, driver_names, driver_coords, passenger_names, passenger_coords)