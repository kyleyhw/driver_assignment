import pandas as pd

df_filename = 'people.csv'

name_header = 'Name'
postcode_header = 'Postcode'
driver_header = 'Driver'
driver_yes = '1'
driver_no = '0'
longitude_header = 'Longitude'
latitude_header = 'Latitude'

def get_df(filename=df_filename):
    df = pd.read_csv(filename, delimiter=',', dtype='str')
    return df

def get_driver_and_passenger_names(df):
    driver_names = df[df[driver_header] == driver_yes][name_header].to_numpy(dtype='str')
    passenger_names = df[df[driver_header] == driver_no][name_header].to_numpy(dtype='str')
    return driver_names, passenger_names

def get_postcode_from_name(name, df):
    postcode = df[df[name_header] == name][postcode_header].item()
    return postcode

def get_coord_from_postcode(postcode):
    area_code_info = pd.read_csv('cb_area_codes.csv', delimiter=',')

    postcode_info_row = area_code_info.loc[area_code_info['Postcode'] == postcode]
    longitude = float(postcode_info_row[longitude_header].values[0])
    latitude = float(postcode_info_row[latitude_header].values[0])

    return longitude, latitude


# minimize_distance('people.csv')