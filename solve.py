"""Solves a simple assignment problem."""
from ortools.sat.python import cp_model
from define_cost import minimize_distance
import numpy as np


def solve(verbose=False):
    # Data
    driver_names, passenger_names, costs = minimize_distance()
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
        driver_assignments = {driver_name: [] for driver_name in driver_names}
        for driver, driver_name in enumerate(driver_names):
            for passenger, passenger_name in enumerate(passenger_names):
                if solver.boolean_value(x[driver, passenger]):
                    if verbose:
                        print(
                            f"Driver {driver_names[driver]} assigned to passenger {passenger_names[passenger]} km."
                            + f" Distance = {costs[driver][passenger]}"
                        )
                    driver_assignments[driver_name].append(passenger_name)
    else:
        print("No solution found.")

    return driver_assignments

solve(verbose=True)