import numpy as np
from math import cos, asin, sqrt, pi

# def distance(a, b):
#     displacement = np.array(a) - np.array(b)
#     return np.sqrt(np.dot(displacement, displacement))

def distance(a, b):
    lon1, lat1 = a
    lon2, lat2 = b

    r = 6371 # km
    p = pi / 180

    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 2 * r * asin(sqrt(a))