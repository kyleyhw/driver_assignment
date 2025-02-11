import pandas as pd
import numpy as np
from misc_funcs import distance, get_coord_from_postcode


def minimize_distance(filename):
    people = pd.read_csv(filename, delimiter=',', dtype='str') # np.genfromtxt('people.csv', delimiter=',', dtype='str')
    people_coords = {}

    for index, people_info in people.iterrows():
        people_coords[people_info[0]] = get_coord_from_postcode(people_info['Postcode'])


    driver_names = people[people['Driver'] == '1']['Name'].to_numpy(dtype='str')
    passenger_names = people[people['Driver'] == '0']['Name'].to_numpy(dtype='str')


    num_drivers = len(driver_names)
    num_passengers = len(passenger_names)

    cost_matrix = np.zeros(shape=(num_drivers, num_passengers))

    for i, driver in enumerate(driver_names):
        for j, passenger in enumerate(passenger_names):
            cost_matrix[i,j] = distance(people_coords[driver], people_coords[passenger])

    return driver_names, passenger_names, cost_matrix

# minimize_distance('people.csv')