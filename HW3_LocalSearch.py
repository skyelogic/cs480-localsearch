# -*- coding: utf-8 -*-
"""
Filename: HW2_InformedSearch.py
Author: Donnel Garner
Date: 2/12/2026
Description: CS480 – Module 3: Local Search

This script allows the user to choose between:

1) Hill Climbing (descending) on the Eggholder function
   - Attempts to find a global minimum
   - Runs 100 independent trials
   - Stops after 100 consecutive non-improving moves
   - Saves scatter and histogram visualizations to folder .png

2) Hill Climbing (Min-Conflicts style) for the N-Queens problem
   - Solves N = 8, 16, 32
   - Runs 100 trials per N
   - Reports number of successful solutions
   - Plots first 10 initial vs final board states
   - Saves .png to folder
"""

import random
import math
from typing import List, Tuple
import matplotlib.pyplot as plt


# ============================================================
# OPTION 1: EGGHOLDER FUNCTION (Continuous Optimization)
# ============================================================

def eggholder(x: float, y: float) -> float:
    """
    Computes the Eggholder function value at (x, y).

    The Eggholder function is a complicated math function often used to test optimization algorithms.
    Because it has many small low points, a hill climbing algorithm can easily stop at
    one of those instead of finding the absolute lowest point.

    Goal: Minimize this function.
    """
    return -(y + 47) * math.sin(math.sqrt(abs(x / 2 + (y + 47)))) \
           - x * math.sin(math.sqrt(abs(x - (y + 47))))


def clamp(v: float, lo: float, hi: float) -> float:
    """
    Ensures that a value stays within the defined search bounds.
    """
    return lo if v < lo else hi if v > hi else v


def hill_climb_eggholder(
    bounds: Tuple[float, float] = (-512.0, 512.0),
    step_size: float = 1.0,
    stall_limit: int = 100,
    max_steps: int = 200000,
) -> Tuple[float, float, float]:
    """
    Performs descending hill climbing on the Eggholder function.

    Algorithm:
      1. Start from a random position in search space
      2. Randomly change x and y within step_size
      3. If new position improves objective (lower value), accept move
      4. Stop if 100 consecutive non-improving moves occur

    Returns:
        Final x, y coordinates and minimum value found
    """

    lo, hi = bounds

    # Random starting position
    x = random.uniform(lo, hi)
    y = random.uniform(lo, hi)
    best = eggholder(x, y)

    stall = 0   # number of consecutive non-improving steps
    steps = 0

    while stall < stall_limit and steps < max_steps:
        steps += 1

        # Generate neighboring candidate solution
        nx = clamp(x + (random.random() - 0.5) * step_size, lo, hi)
        ny = clamp(y + (random.random() - 0.5) * step_size, lo, hi)

        val = eggholder(nx, ny)

        # Accept move only if strictly better (descending hill climbing)
        if val < best:
            x, y, best = nx, ny, val
            stall = 0
        else:
            stall += 1

    return x, y, best


def run_eggholder_experiment(runs: int = 100) -> None:
    """
    Runs hill climbing on Eggholder function 100 times.
    Saves:
      - Scatter plot of found minima locations
      - Histogram of minimum values
    """

    minima = [hill_climb_eggholder() for _ in range(runs)]

    xs = [m[0] for m in minima]
    ys = [m[1] for m in minima]
    vals = [m[2] for m in minima]

    # Scatter plot of final positions use matplotlib
    plt.figure()
    sc = plt.scatter(xs, ys, c=vals, s=18)
    plt.colorbar(sc, label="Function value")
    plt.title("Eggholder Hill Climbing Minima (100 Runs)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.savefig("eggholder_minima_scatter.png", dpi=200)

    # Histogram of final values useing matplotlib
    plt.figure()
    plt.hist(vals, bins=20)
    plt.title("Distribution of Final Minima Values")
    plt.xlabel("Minimum Value Found")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("eggholder_minima_hist.png", dpi=200)

    # Print best result found across runs
    best_idx = min(range(runs), key=lambda i: vals[i])
    print("\n[Eggholder Results]")
    print(f"Best value found: {vals[best_idx]:.6f}")
    print(f"Location: ({xs[best_idx]:.6f}, {ys[best_idx]:.6f})")


# ============================================================
# OPTION 2: N-QUEENS (Discrete Optimization)
# ============================================================

def random_state(n: int) -> List[int]:
    """
    Generates a random N-Queens state.
    Representation:
        state[c] = row index of queen in column c
    Guarantees one queen per column.
    """
    return [random.randrange(n) for _ in range(n)]


def attacks(state: List[int]) -> int:
    """
    Computes total number of attacking queen pairs.
    Objective: minimize this value (goal is 0).
    """
    n = len(state)
    count = 0

    for c1 in range(n):
        for c2 in range(c1 + 1, n):
            r1, r2 = state[c1], state[c2]

            # Same row
            if r1 == r2:
                count += 1

            # Same diagonal
            elif abs(r1 - r2) == abs(c1 - c2):
                count += 1

    return count


def column_conflicts(state: List[int], col: int) -> int:
    """
    Counts how many conflicts a queen in a given column has.
    Used to choose which queen to move.
    """
    n = len(state)
    r = state[col]
    conflicts = 0

    for j in range(n):
        if j == col:
            continue
        rj = state[j]
        if rj == r or abs(r - rj) == abs(col - j):
            conflicts += 1

    return conflicts


def min_conflicts_hill_climb(n: int, max_steps: int = 20000):
    """
    Hill climbing search using Min-Conflicts strategy.

    Algorithm:
      1. Start with random board
      2. If conflicts exist:
         - Choose a conflicted queen
         - Move it to row minimizing total attacks
      3. Repeat until solution or max_steps reached

    Returns:
        final_state, number_of_attacks
    """

    state = random_state(n)
    cur_attacks = attacks(state)

    for _ in range(max_steps):

        if cur_attacks == 0:
            break

        # Select queen currently in conflict
        conflicted_cols = [c for c in range(n) if column_conflicts(state, c) > 0]
        if not conflicted_cols:
            break

        col = random.choice(conflicted_cols)

        best_rows = []
        best_val = None
        original_row = state[col]

        # Try moving queen to every possible row
        for r in range(n):
            state[col] = r
            val = attacks(state)

            if best_val is None or val < best_val:
                best_val = val
                best_rows = [r]
            elif val == best_val:
                best_rows.append(r)

        # Choose randomly among best moves
        state[col] = random.choice(best_rows)
        cur_attacks = attacks(state)

    return state, cur_attacks


def run_nqueens_experiment(trials: int = 100, ns=(8, 16, 32)):
    """
    Runs N-Queens hill climbing 100 times for N=8,16,32.
    Reports number of successful solutions.
    """

    for n in ns:
        successes = 0

        for _ in range(trials):
            _, a = min_conflicts_hill_climb(n)
            if a == 0:
                successes += 1

        print(f"\n[N-Queens Results] N={n}")
        print(f"Solutions found: {successes}/{trials}")


# ============================================================
# MAIN MENU
# ============================================================

def main():
    """
    Displays menu and executes selected local search experiment.
    """

    print("\nCS480 Local Search")
    print("1) Eggholder Optimization")
    print("2) N-Queens Problem")

    choice = input("Choose 1 or 2: ").strip()

    if choice == "1":
        run_eggholder_experiment()
    elif choice == "2":
        run_nqueens_experiment()
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    random.seed()  # seed from system time
    main()
