import numpy as np
from math import cos, asin, sqrt, pi
import pandas as pd

# def distance(a, b):
#     displacement = np.array(a) - np.array(b)
#     return np.sqrt(np.dot(displacement, displacement))

def distance(a, b):
    # credit: users Jan Schultke and Salvador Dali on
    # StackOverflow https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
    lon1, lat1 = a
    lon2, lat2 = b

    r = 6371 # km
    p = pi / 180

    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 2 * r * asin(sqrt(a))


from pyproj import transform

class translate_coordinates:
    def __init__(self, input_coordinate_system, output_coordinate_system):
        self.input_coordinate_system = input_coordinate_system
        self.output_coordinate_system = output_coordinate_system

    def translate(self, x, y):
        output_x, output_y = transform(self.input_coordinate_system, self.output_coordinate_system, x, y)
        return output_x, output_y


def solve_single_driver_route(locations):
    """
    Solves a simplified TSP for a single driver using a nearest-neighbor heuristic.
    Assumes the first location in 'locations' is the driver's starting point.

    Args:
        locations (list): A list of (lon, lat) tuples representing the driver's start
                          and subsequent passenger pickup locations.

    Returns:
        tuple: A tuple containing:
               - list: The optimal order of indices (including the driver's start).
               - float: The total distance of the route.
    """
    num_locations = len(locations)
    if num_locations <= 1:
        return [0], 0.0

    # Calculate distance matrix for all locations
    dist_matrix = np.zeros((num_locations, num_locations))
    for i in range(num_locations):
        for j in range(num_locations):
            if i == j:
                dist_matrix[i, j] = 0
            else:
                dist_matrix[i, j] = distance(locations[i], locations[j])

    # Nearest-neighbor heuristic
    current_location_idx = 0  # Start at the driver's location
    unvisited_indices = set(range(1, num_locations))  # All passengers are unvisited
    route = [current_location_idx]
    total_distance = 0.0

    while unvisited_indices:
        nearest_neighbor_idx = -1
        min_dist = np.inf

        for neighbor_idx in unvisited_indices:
            dist = dist_matrix[current_location_idx, neighbor_idx]
            if dist < min_dist:
                min_dist = dist
                nearest_neighbor_idx = neighbor_idx

        if nearest_neighbor_idx != -1:
            route.append(nearest_neighbor_idx)
            total_distance += min_dist
            unvisited_indices.remove(nearest_neighbor_idx)
            current_location_idx = nearest_neighbor_idx
        else:
            # Should not happen if unvisited_indices is not empty
            break

    return route, total_distance
