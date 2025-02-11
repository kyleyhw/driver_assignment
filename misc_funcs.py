import numpy as np
from math import cos, asin, sqrt, pi
import pandas as pd

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

def get_coord_from_postcode(postcode):
    area_code_info = pd.read_csv('cb_area_codes.csv', delimiter=',')
    postcode

    postcode_info_row = area_code_info.loc[area_code_info['Postcode'] == postcode]
    longitude = float(postcode_info_row['Longitude'].values[0])
    latitude = float(postcode_info_row['Latitude'].values[0])

    return longitude, latitude