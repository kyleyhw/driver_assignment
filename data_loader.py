import pandas as pd

def get_people_df(filename='people.csv'):
    df = pd.read_csv(filename, delimiter=',', dtype='str')
    return df

def get_driver_and_passenger_names(df):
    driver_names = df[df['Driver'] == '1']['Name'].to_numpy(dtype='str')
    passenger_names = df[df['Driver'] == '0']['Name'].to_numpy(dtype='str')
    return driver_names, passenger_names

def get_postcode_from_name(name, df):
    postcode = df[df['Name'] == name]['Postcode'].item()
    return postcode

def get_coord_from_postcode(postcode):
    area_code_info = pd.read_csv('cb_area_codes.csv', delimiter=',')

    postcode_info_row = area_code_info.loc[area_code_info['Postcode'] == postcode]
    longitude = float(postcode_info_row['Longitude'].values[0])
    latitude = float(postcode_info_row['Latitude'].values[0])

    return longitude, latitude


# minimize_distance('people.csv')