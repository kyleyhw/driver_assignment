import numpy as np

from data_loader import get_df, get_coord_from_postcode, get_driver_and_passenger_names, get_postcode_from_name
from misc_funcs import distance

def minimize_distance():
    people = get_df()

    people_coords = {}

    driver_names, passenger_names = get_driver_and_passenger_names(people)

    for name in np.concatenate((driver_names, passenger_names)):
        postcode = get_postcode_from_name(name, df=people)
        people_coords[name] = get_coord_from_postcode(postcode)

    num_drivers = len(driver_names)
    num_passengers = len(passenger_names)

    cost_matrix = np.zeros(shape=(num_drivers, num_passengers))

    for i, driver in enumerate(driver_names):
        for j, passenger in enumerate(passenger_names):
            cost_matrix[i,j] = distance(people_coords[driver], people_coords[passenger])

    return driver_names, passenger_names, cost_matrix