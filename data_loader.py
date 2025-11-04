import pandas as pd

df_filename = 'people.csv'

name_header = 'Name'
postcode_header = 'Postcode'
driver_header = 'Driver'
driver_yes = '1'
driver_no = '0'
longitude_header = 'Longitude'
latitude_header = 'Latitude'

def get_df(df_filename='data/people_1.csv'):
    df = pd.read_csv(df_filename, delimiter=',', dtype='str', header=0)
    return df

def get_driver_and_passenger_names(df):
    driver_names = df[df[driver_header] == driver_yes][name_header].to_numpy(dtype='str')
    passenger_names = df[df[driver_header] == driver_no][name_header].to_numpy(dtype='str')
    return driver_names, passenger_names

def get_postcode_from_name(name, people_information_dataframe):
    postcode = people_information_dataframe[people_information_dataframe[name_header] == name][postcode_header].item()
    return postcode

def get_coord_from_postcode(postcode):
    area_code_info = pd.read_csv('cb_area_codes.csv', delimiter=',', header=0)

    postcode_info_row = area_code_info.loc[area_code_info['Postcode'] == postcode]
    if postcode_info_row.empty:
        return None, None
    longitude = float(postcode_info_row[longitude_header].values[0])
    latitude = float(postcode_info_row[latitude_header].values[0])

    return longitude, latitude

def get_coords_from_name(name, people_information_dataframe):
    postcode = get_postcode_from_name(name, people_information_dataframe)
    longitude, latitude = get_coord_from_postcode(postcode)
    if longitude is None:
        return None
    return longitude, latitude


def get_names_and_coords(people_information_dataframe):
    driver_names_all, passenger_names_all = get_driver_and_passenger_names(people_information_dataframe)

    driver_names = []
    driver_coords = []
    for name in driver_names_all:
        coords = get_coords_from_name(name=name, people_information_dataframe=people_information_dataframe)
        if coords is not None:
            driver_names.append(name)
            driver_coords.append(coords)

    passenger_names = []
    passenger_coords = []
    for name in passenger_names_all:
        coords = get_coords_from_name(name=name, people_information_dataframe=people_information_dataframe)
        if coords is not None:
            passenger_names.append(name)
            passenger_coords.append(coords)
    return driver_names, passenger_names, driver_coords, passenger_coords


# get_names_and_coords('people_information_dataframe.csv')
