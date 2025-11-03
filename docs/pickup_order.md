# Pickup Order Determination

## 1. Introduction

When a driver is assigned to multiple passengers, the problem of determining the most efficient sequence for picking up these passengers arises. This is a classic optimization problem known as the Traveling Salesperson Problem (TSP) or a variant thereof. The goal is to find the shortest possible route that visits each assigned passenger exactly once and returns to the starting point (though in our case, it's a one-way trip from the driver's start through all passengers).

## 2. Mathematical Explanation: The Traveling Salesperson Problem (TSP)

The Traveling Salesperson Problem (TSP) is a fundamental problem in combinatorial optimization. Given a list of cities and the distances between each pair of cities, the problem is to find the shortest possible route that visits each city exactly once and returns to the origin city.

### 2.1 Formal Definition

Let $V = \{v_0, v_1, \dots, v_n\}$ be a set of $n+1$ locations, where $v_0$ is the driver's starting location and $v_1, \dots, v_n$ are the passenger pickup locations. Let $d(v_i, v_j)$ be the distance between location $v_i$ and location $v_j$. We assume $d(v_i, v_j) \ge 0$ and $d(v_i, v_j) = d(v_j, v_i)$ (symmetric TSP).

A tour is a permutation $\pi = (\pi_0, \pi_1, \dots, \pi_n)$ of the locations, where $\pi_0 = v_0$ (the driver's starting point). The objective is to find a tour that minimizes the total distance:

$$ \min_{\pi} \left( \sum_{i=0}^{n-1} d(\pi_i, \pi_{i+1}) \right) $$

In our specific case, the driver does not return to the origin after the last pickup, so the objective is to minimize the sum of distances between consecutive pickups.

The TSP is known to be NP-hard, meaning that there is no known polynomial-time algorithm that can solve it exactly for all instances. This necessitates the use of heuristics or approximation algorithms for larger problem sizes [[1]](#ref-cormen-2009).

## 3. Nearest Neighbor Heuristic

For the initial implementation, the nearest-neighbor heuristic was chosen due to its simplicity and computational efficiency.

### 3.1 Algorithm Description

The nearest-neighbor heuristic constructs a tour as follows:

1.  Start at the driver's initial location ($v_0$). 
2.  From the current location, visit the unvisited location that is closest.
3.  Repeat step 2 until all locations have been visited.

### 3.2 Advantages

*   **Simplicity:** Easy to understand and implement.
*   **Speed:** Computationally very fast, making it suitable for real-time applications or scenarios with many drivers and small numbers of passengers per driver.

### 3.3 Disadvantages

*   **Sub-optimality:** The nearest-neighbor heuristic is a greedy algorithm and does not guarantee an optimal solution. It can often get "stuck" in local optima, leading to routes that are significantly longer than the true shortest path. The quality of the solution can vary greatly depending on the starting point and the distribution of locations.

## 4. Comparison to Other Options

### 4.1 Brute Force (Exact Solution)

*   **Method:** This involves calculating the total distance for every possible permutation of pickup locations and choosing the shortest one.
*   **Complexity:** For $n$ passenger locations, there are $(n-1)!$ possible permutations (if the driver's start is fixed). The factorial growth makes this approach computationally infeasible for even a small number of passengers. For example, with 10 passengers, there are $9! = 362,880$ permutations. With 20 passengers, the number becomes astronomically large.
*   **Comparison to Nearest Neighbor:** Brute force guarantees the optimal solution but is impractical for $n > \approx 10-12$. Nearest neighbor is much faster but provides a sub-optimal solution.

### 4.2 Other Heuristics and Approximation Algorithms

Several other methods exist that offer a better trade-off between solution quality and computational time than nearest neighbor:

*   **2-Opt, 3-Opt:** These are local search algorithms that iteratively improve a given tour by swapping edges. They can significantly improve upon a nearest-neighbor solution.
*   **Genetic Algorithms (GAs):** Inspired by natural selection, GAs can explore a large solution space and often find good solutions for complex TSP instances.
*   **Ant Colony Optimization (ACO):** Based on the foraging behavior of ants, ACO algorithms can find good solutions by simulating pheromone trails.
*   **Specialized Solvers (e.g., OR-Tools TSP Solver):** Libraries like Google OR-Tools provide highly optimized algorithms (often based on metaheuristics or exact methods for smaller instances) that can find near-optimal or optimal solutions for larger TSP problems within reasonable timeframes. These are generally more complex to set up but offer superior performance.
*   **Comparison to Nearest Neighbor:** These methods are generally more complex to implement and computationally more intensive than nearest neighbor but yield significantly better (closer to optimal) solutions.

## 5. Why Nearest Neighbor was Chosen for Initial Implementation

The nearest-neighbor heuristic was chosen for the `solve_single_driver_route` function for the following reasons:

*   **Simplicity and Rapid Prototyping:** It allowed for quick implementation of the pickup order functionality without introducing significant complexity to the codebase.
*   **Reasonable Performance for Small Instances:** In a typical ride-sharing scenario, a single driver is unlikely to be assigned a very large number of passengers (e.g., usually 2-4). For such small numbers, the nearest-neighbor solution is often close to optimal or at least acceptable.
*   **Foundation for Future Improvements:** It provides a working baseline that can be easily replaced or enhanced with more sophisticated algorithms (like OR-Tools' TSP solver) in the future if higher solution quality is required.

---

## References

<span id="ref-cormen-2009">[1]</span> Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. [Link to book's website](https://mitpress.mit.edu/books/introduction-algorithms)
