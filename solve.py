"""Solves a simple assignment problem."""
from ortools.sat.python import cp_model
from data_loader import get_names_and_coords
from define_cost import get_physical_distance_matrix, get_driving_distance_matrix
from misc_funcs import solve_single_driver_route
import numpy as np

def solve(people_information_dataframe, verbose=False, cost_function=None, api_key=None):
    # Data
    driver_names, passenger_names, driver_coords, passenger_coords = get_names_and_coords(people_information_dataframe=people_information_dataframe)

    if cost_function is None or cost_function == get_physical_distance_matrix:
        costs = get_physical_distance_matrix(driver_coords=driver_coords, passenger_coords=passenger_coords)
    elif cost_function == get_driving_distance_matrix:
        if api_key is None:
            raise ValueError("API key must be provided when using get_driving_distance_matrix.")
        costs = get_driving_distance_matrix(driver_coords=driver_coords, passenger_coords=passenger_coords, api_key=api_key)
    else:
        raise ValueError("Invalid cost_function provided.")
    num_drivers = len(costs)
    num_passengers = len(costs[0])

    task_sizes = np.ones(shape=(num_passengers))
    # Maximum total of passenger sizes for any driver
    total_size_max = 3

    # Model
    model = cp_model.CpModel()

    # Variables
    x = {}
    for driver in range(num_drivers):
        for passenger in range(num_passengers):
            x[driver, passenger] = model.new_bool_var(f"x[{driver},{passenger}]")

    # Constraints
    # Each driver is assigned to at most one passenger.
    for driver in range(num_drivers):
        model.add(
            sum(task_sizes[task] * x[driver, task] for task in range(num_passengers))
            <= total_size_max
        )

    # Each passenger is assigned to exactly one driver.
    for passenger in range(num_passengers):
        model.add_exactly_one(x[worker, passenger] for worker in range(num_drivers))

    # Objective
    objective_terms = []
    for driver in range(num_drivers):
        for passenger in range(num_passengers):
            objective_terms.append(costs[driver][passenger] * x[driver, passenger])
    model.minimize(sum(objective_terms))

    # Solve
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    driver_assignments = None
    # Print solution and collect driver assignments.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # print(f"Total distance = {solver.objective_value}\n")
        driver_assignments = {driver_name: {"passengers": [], "route": [], "total_route_distance": 0.0} for driver_name in driver_names}
        
        # First, populate assigned passengers
        assigned_passenger_coords = {} # To easily get passenger coords by name
        for passenger_idx, passenger_name in enumerate(passenger_names):
            assigned_passenger_coords[passenger_name] = passenger_coords[passenger_idx]

        for driver_idx, driver_name in enumerate(driver_names):
            current_driver_assigned_passengers = []
            for passenger_idx, passenger_name in enumerate(passenger_names):
                if solver.boolean_value(x[driver_idx, passenger_idx]):
                    current_driver_assigned_passengers.append((passenger_name, passenger_coords[passenger_idx]))
                    driver_assignments[driver_name]["passengers"].append(passenger_name)
            
            if current_driver_assigned_passengers:
                # Prepare locations for TSP solver: driver's start + assigned passenger locations
                locations_for_route = [driver_coords[driver_idx]] + [p_coord for p_name, p_coord in current_driver_assigned_passengers]
                
                # Solve for pickup order
                route_indices, total_route_distance = solve_single_driver_route(locations_for_route)
                
                # Map indices back to passenger names
                ordered_passenger_names = []
                for idx in route_indices[1:]: # Skip driver's start location
                    ordered_passenger_names.append(current_driver_assigned_passengers[idx-1][0]) # -1 because driver is at index 0
                
                driver_assignments[driver_name]["route"] = ordered_passenger_names
                driver_assignments[driver_name]["total_route_distance"] = total_route_distance

                if verbose:
                    print(f"Driver {driver_name} assigned to passengers: {driver_assignments[driver_name]['passengers']}")
                    print(f"  Pickup order: {driver_name} -> {' -> '.join(driver_assignments[driver_name]['route'])}")
                    print(f"  Total route distance: {driver_assignments[driver_name]['total_route_distance']:.2f} km")
            elif verbose:
                print(f"Driver {driver_name} has no assigned passengers.")
    else:
        print("No solution found.")

    return driver_assignments, driver_names, driver_coords, passenger_names, passenger_coords

if __name__ == '__solve__':
    from data_loader import get_df
    solve(people_information_dataframe=get_df(), verbose=True)