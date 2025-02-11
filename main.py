"""Solves a simple assignment problem."""
from ortools.sat.python import cp_model
from data_loader import data_loader_minimize_distance
import numpy as np


def main() -> None:
    # Data
    driver_names, passenger_names, costs = data_loader_minimize_distance(filename='people.csv')
    num_workers = len(costs)
    num_tasks = len(costs[0])

    task_sizes = np.ones(shape=(num_tasks))
    # Maximum total of task sizes for any worker
    total_size_max = 3

    # Model
    model = cp_model.CpModel()

    # Variables
    x = {}
    for worker in range(num_workers):
        for task in range(num_tasks):
            x[worker, task] = model.new_bool_var(f"x[{worker},{task}]")

    # Constraints
    # Each worker is assigned to at most one task.
    for worker in range(num_workers):
        model.add(
            sum(task_sizes[task] * x[worker, task] for task in range(num_tasks))
            <= total_size_max
        )

    # Each task is assigned to exactly one worker.
    for task in range(num_tasks):
        model.add_exactly_one(x[worker, task] for worker in range(num_workers))

    # Objective
    objective_terms = []
    for worker in range(num_workers):
        for task in range(num_tasks):
            objective_terms.append(costs[worker][task] * x[worker, task])
    model.minimize(sum(objective_terms))

    # Solve
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    # Print solution.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for worker in range(num_workers):
            for task in range(num_tasks):
                if solver.boolean_value(x[worker, task]):
                    print(
                        f"Driver {driver_names[worker]} assigned to passenger {passenger_names[task]} km."
                        + f" Distance = {costs[worker][task]}"
                    )
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()