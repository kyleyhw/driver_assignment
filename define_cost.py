import numpy as np
import requests
from misc_funcs import distance


def get_physical_distance_matrix(driver_coords, passenger_coords):
    num_drivers = len(driver_coords)
    num_passengers = len(passenger_coords)

    cost_matrix = np.zeros(shape=(num_drivers, num_passengers))

    for i, driver_coord in enumerate(driver_coords):
        for j, passenger_coord in enumerate(passenger_coords):
            cost_matrix[i,j] = distance(driver_coord, passenger_coord)

    return cost_matrix


def get_driving_distance_matrix(driver_coords, passenger_coords, api_key):
    """
    Calculates the driving distance matrix using the Google Maps Distance Matrix API.

    Args:
        driver_coords (list): A list of (latitude, longitude) tuples for drivers.
        passenger_coords (list): A list of (latitude, longitude) tuples for passengers.
        api_key (str): Your Google Maps API key.

    Returns:
        numpy.ndarray: A cost matrix where the entry (i, j) is the driving distance
                       in kilometers from driver i to passenger j.
    """
    num_drivers = len(driver_coords)
    num_passengers = len(passenger_coords)
    cost_matrix = np.zeros(shape=(num_drivers, num_passengers))

    origins = '|'.join([f"{lat},{lon}" for lon, lat in driver_coords])
    destinations = '|'.join([f"{lat},{lon}" for lon, lat in passenger_coords])

    url = (
        "https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={origins}"
        f"&destinations={destinations}"
        f"&key={api_key}"
    )

    response = requests.get(url)
    data = response.json()

    if data['status'] != 'OK':
        print(f"Error from Google Maps API: {data['error_message']}")
        return None

    for i, row in enumerate(data['rows']):
        for j, element in enumerate(row['elements']):
            if element['status'] == 'OK':
                # Distance is in meters, convert to kilometers
                cost_matrix[i, j] = element['distance']['value'] / 1000
            else:
                # Handle cases where a route could not be found
                cost_matrix[i, j] = np.inf

    return cost_matrix
