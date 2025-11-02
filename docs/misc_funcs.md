# `misc_funcs.py` Documentation

This script contains miscellaneous helper functions used by other scripts in the project.

## Functions

### `distance(a, b)`

- **Purpose**: Calculates the great-circle distance between two geographical points, `a` and `b`, using the Haversine formula.
- **Parameters**:
  - `a` (tuple): A (longitude, latitude) tuple for the first point.
  - `b` (tuple): A (longitude, latitude) tuple for the second point.
- **Returns**: The distance between the two points in kilometers.

#### Haversine Formula

The Haversine formula is used to calculate the distance between two points on a sphere. It is a more accurate method for calculating geographical distances than Euclidean distance because it accounts for the Earth's curvature.

The formula is implemented as follows:

$a = \sin^2(\frac{\Delta\phi}{2}) + \cos(\phi_1) \cdot \cos(\phi_2) \cdot \sin^2(\frac{\Delta\lambda}{2})$

$d = 2 \cdot R \cdot \text{asin}(\sqrt{a})$

where:
- $\phi$ is latitude, $\lambda$ is longitude
- $R$ is the radius of the Earth (6371 km)

This function is credited to StackOverflow users Jan Schultke and Salvador Dali.

## Classes

### `translate_coordinates`

- **Purpose**: A class to translate coordinates from one coordinate system to another.
- **Initialization**:
  - `__init__(self, input_coordinate_system, output_coordinate_system)`: Initializes the translator with the input and output coordinate systems. These should be specified in a format that the `pyproj` library can understand (e.g., EPSG codes).
- **Methods**:
  - `translate(self, x, y)`: Translates the coordinates `(x, y)` from the input coordinate system to the output coordinate system.
    - **Parameters**:
      - `x`, `y`: The coordinates to be translated.
    - **Returns**: A tuple `(output_x, output_y)` representing the translated coordinates.

This class is a wrapper around the `pyproj.transform` function, providing a convenient way to perform coordinate transformations.
