# `data_loader.py` Documentation

This script is responsible for loading and processing the data required for the driver assignment problem. It reads data from two CSV files: `people.csv` and `cb_area_codes.csv`.

## Functions

### `get_df(filename)`

- **Purpose**: Reads the main data file (`people.csv` by default) into a pandas DataFrame.
- **Parameters**:
  - `filename` (str): The path to the CSV file. Defaults to `people.csv`.
- **Returns**: A pandas DataFrame containing the data from the CSV file.

### `get_driver_and_passenger_names(df)`

- **Purpose**: Separates the names of drivers and passengers from the main DataFrame.
- **Parameters**:
  - `df` (DataFrame): The main DataFrame containing people's information.
- **Returns**: A tuple containing two NumPy arrays: one for driver names and one for passenger names.

### `get_postcode_from_name(name, people_information_dataframe)`

- **Purpose**: Retrieves the postcode of a person given their name.
- **Parameters**:
  - `name` (str): The name of the person.
  - `people_information_dataframe` (DataFrame): The DataFrame containing people's information.
- **Returns**: The postcode (str) of the person.

### `get_coord_from_postcode(postcode)`

- **Purpose**: Retrieves the geographical coordinates (longitude and latitude) for a given postcode.
- **Logic**: It reads the `cb_area_codes.csv` file and looks up the postcode to find the corresponding longitude and latitude.
- **Parameters**:
  - `postcode` (str): The postcode to look up.
- **Returns**: A tuple containing the longitude and latitude (float, float).

### `get_coords_from_name(name, people_information_dataframe)`

- **Purpose**: A convenience function that retrieves the coordinates of a person given their name. It does this by first finding the person's postcode and then finding the coordinates for that postcode.
- **Parameters**:
  - `name` (str): The name of the person.
  - `people_information_dataframe` (DataFrame): The DataFrame containing people's information.
- **Returns**: A tuple containing the longitude and latitude (float, float).

### `get_names_and_coords(people_information_dataframe)`

- **Purpose**: This is the main function of the script. It orchestrates the other functions to produce the final data needed for the solver.
- **Logic**:
  1. It calls `get_driver_and_passenger_names` to separate the drivers and passengers.
  2. It then iterates through the names of drivers and passengers, calling `get_coords_from_name` for each name to get their coordinates.
- **Parameters**:
  - `people_information_dataframe` (DataFrame): The main DataFrame containing people's information.
- **Returns**: A tuple containing four elements: `(driver_names, passenger_names, driver_coords, passenger_coords)`.
