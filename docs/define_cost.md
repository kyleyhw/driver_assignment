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

The distance between two points on the Earth's surface is calculated using the Haversine formula [[1]](#ref-haversine). This is a more accurate method than using Euclidean distance, as it takes into account the curvature of the Earth.

### Rationale for using the Haversine Formula

For the scale of this project (the city of Cambridge), the Earth can be reasonably approximated as a perfect sphere. The Haversine formula calculates the great-circle distance between two points on a sphere, which is the shortest distance along the surface of the sphere. This provides a good approximation of the real-world travel distance, especially in the absence of road network data. While not as precise as road network distances, it is a computationally efficient and sufficiently accurate method for this optimization problem.

The cost matrix $C$ is therefore defined as:

$C_{ij} = \text{distance}(\text{driver_coord}_i, \text{passenger_coord}_j)$

where `driver_coord_i` is the coordinate of the $i$-th driver and `passenger_coord_j` is the coordinate of the $j$-th passenger.

## References

<span id="ref-haversine">[1]</span> Wikipedia. (2023). *Haversine formula*. [https://en.wikipedia.org/wiki/Haversine_formula](https://en.wikipedia.org/wiki/Haversine_formula)
