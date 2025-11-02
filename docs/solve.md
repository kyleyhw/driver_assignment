# `solve.py` Documentation

This is the main script for the driver assignment project. It brings together the data loading, cost definition, and optimization to solve the assignment problem.

## Functions

### `solve(people_information_dataframe, verbose=False)`

- **Purpose**: Solves the driver assignment problem.
- **Parameters**:
  - `people_information_dataframe` (DataFrame): The DataFrame containing the information about drivers and passengers.
  - `verbose` (bool): If `True`, the function will print the details of the assignments and the distance for each assignment.
- **Returns**: A dictionary where the keys are driver names and the values are lists of the names of the passengers assigned to that driver.

## Optimization Model

The problem is modeled as an integer programming problem and solved using the CP-SAT solver from Google's OR-Tools library.

### 1. Data Preparation

The first step is to prepare the data. This involves:
- Getting the names and coordinates of drivers and passengers using `get_names_and_coords` from `data_loader.py`.
- Calculating the cost matrix (distances between drivers and passengers) using `get_physical_distance_matrix` from `define_cost.py`.

### 2. Model Definition

A CP-SAT model is initialized using `cp_model.CpModel()`.

### 3. Variables

The variables for the model are a set of boolean variables, $x_{ij}$, where:

$x_{ij} = \begin{cases} 1 & \text{if driver } i \text{ is assigned to passenger } j \\ 0 & \text{otherwise} \end{cases}$

These are created in the code using `model.new_bool_var()`.

### 4. Constraints

Two main constraints are applied to the model:

1.  **Each passenger is assigned to exactly one driver.** This ensures that every passenger is picked up.
    
    $\sum_{i=1}^{N_d} x_{ij} = 1 \quad \forall j \in \{1, ..., N_p\}$
    
    where $N_d$ is the number of drivers and $N_p$ is the number of passengers. This is implemented using `model.add_exactly_one()`.

2.  **Each driver is assigned a limited number of passengers.** This ensures that the capacity of each car is not exceeded. The current implementation hardcodes the car capacity to 3 passengers.
    
    $\sum_{j=1}^{N_p} x_{ij} \le 3 \quad \forall i \in \{1, ..., N_d\}$
    
    This is implemented using `model.add()`.

### 5. Objective Function

The objective of the optimization is to minimize the total distance traveled by all drivers to pick up their assigned passengers. The objective function is therefore:

$\text{minimize} \sum_{i=1}^{N_d} \sum_{j=1}^{N_p} C_{ij} x_{ij}$

where $C_{ij}$ is the cost (distance) of assigning driver $i$ to passenger $j$. This is implemented using `model.minimize()`.

### 6. Solving the Model

The model is solved using `cp_model.CpSolver()`. If a solution is found (either optimal or feasible), the function processes the results to create the `driver_assignments` dictionary.
