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
