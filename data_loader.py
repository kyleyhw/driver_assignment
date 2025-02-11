import pandas as pd
import numpy as np
from misc_funcs import distance


def data_loader_minimize_distance(filename):
    area_code_info = pd.read_csv('cb_area_codes.csv', delimiter=',')
    people = pd.read_csv(filename, delimiter=',', dtype='str') # np.genfromtxt('people.csv', delimiter=',', dtype='str')
    people_coords = {}

    for index, people_info in people.iterrows():
        people_postcode = people_info['Postcode']

        postcode_info_row = area_code_info.loc[area_code_info['Postcode'] == people_postcode]
        longitude = float(postcode_info_row['Longitude'].values[0])
        latitude = float(postcode_info_row['Latitude'].values[0])

        people_coords[people_info[0]] = (longitude, latitude)


    driver_names = people[people['Driver'] == '1']['Name'].to_numpy(dtype='str')
    passenger_names = people[people['Driver'] == '0']['Name'].to_numpy(dtype='str')


    num_drivers = len(driver_names)
    num_passengers = len(passenger_names)

    cost_matrix = np.zeros(shape=(num_drivers, num_passengers))

    for i, driver in enumerate(driver_names):
        for j, passenger in enumerate(passenger_names):
            cost_matrix[i,j] = distance(people_coords[driver], people_coords[passenger])

    return driver_names, passenger_names, cost_matrix

# data_loader_minimize_distance('people.csv')