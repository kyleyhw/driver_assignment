import numpy as np

from misc_funcs import distance



def get_physical_distance_matrix(driver_coords, passenger_coords):
    num_drivers = len(driver_coords)
    num_passengers = len(passenger_coords)

    cost_matrix = np.zeros(shape=(num_drivers, num_passengers))

    for i, driver_coord in enumerate(driver_coords):
        for j, passenger_coord in enumerate(passenger_coords):
            cost_matrix[i,j] = distance(driver_coord, passenger_coord)

    return cost_matrix