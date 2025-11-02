# `define_cost.py` Documentation

This script defines the cost function for the driver assignment problem. The cost is defined as the physical distance between a driver and a passenger.

## Functions

### `get_physical_distance_matrix(driver_coords, passenger_coords)`

- **Purpose**: Calculates the cost matrix, where each element $(i, j)$ of the matrix represents the distance between driver $i$ and passenger $j$.
- **Parameters**:
  - `driver_coords` (list of tuples): A list of the coordinates of the drivers, where each coordinate is a (longitude, latitude) tuple.
  - `passenger_coords` (list of tuples): A list of the coordinates of the passengers.
- **Returns**: A NumPy array representing the cost matrix. The shape of the matrix is `(num_drivers, num_passengers)`.

## Mathematical Formulation

The distance between two points on the Earth's surface is calculated using the Haversine formula. This is a more accurate method than using Euclidean distance, as it takes into account the curvature of the Earth.

The distance function `distance(a, b)` is imported from `misc_funcs.py`. It takes two coordinate tuples, `a` and `b`, and returns the Haversine distance between them in kilometers.

The cost matrix $C$ is therefore defined as:

$C_{ij} = \text{distance}(\text{driver_coord}_i, \text{passenger_coord}_j)$

where `driver_coord_i` is the coordinate of the $i$-th driver and `passenger_coord_j` is the coordinate of the $j$-th passenger.
