# CS480 – Module 3 Assignment
Local Search: Hill Climbing  
Author: Donnel Garner  
Date: 02/12/2026  

This project implements two hill climbing–based local search algorithms:  
- Descending Hill Climbing to minimize the Eggholder function
- Hill Climbing (Min-Conflicts style) to solve the N-Queens problem

Both problems demonstrate how hill climbing behaves in:  
- A continuous search space (Eggholder)
- A discrete combinatorial search space (N-Queens)

To run with output in the terminal: 
- Run python3 HW3_LocalSearch.py  
- The program will direct you from there.

WEBSITE: https://donnelgarner.com/projects/CS480/localsearch/index.html
GOOGLE COLAB: N/A  
GITHUB: https://github.com/skyelogic/cs480-localsearch/

## INTRODUCTION

Both problems demonstrate how hill climbing behaves in:  
- A continuous search space (Eggholder)
- A discrete combinatorial search space (N-Queens)

## Eggholder Function

Minimize the Eggholder function over the domain:  
		-512 ≤ x ≤ 512  
		-512 ≤ y ≤ 512  
		
Algorithm:
- Random starting point  
- Random neighbor generated using:  
		x' = x + (rand() - 0.5) * 1.0  
		y' = y + (rand() - 0.5) * 1.0  
- If the neighbor has a lower value, move to it
- Stop after 100 consecutive non-improving moves
- Repeat 100 independent runs

The program generates:
- eggholder_minima_scatter.png
	- Scatter plot of final positions
- eggholder_minima_hist.png
	- Histogram of minimum values found

## N-Queens Problem

Place N queens on an N×N board such that:
- No two queens share the same row
- No two queens share the same diagonal

Tested for:
- N = 8, 16, 32

Each value of N runs 100 trials.

Algorithm (Min-Conflicts Hill Climbing):  
1. Generate random initial board
2. If conflicts exist:
	- Choose a queen involved in conflict
	- Move it to the row that minimizes total attacks
3. Repeat until:
	- Solution found
	- Max steps reached
	
For each N:
Prints number of successful solutions (out of 100)

Saves board visualizations:
- nqueens_N8_examples.png
- nqueens_N16_examples.png
- nqueens_N32_examples.png

## Observations
Eggholder
- Frequently converges to different local minima
- Rarely finds the true global minimum
- Demonstrates limitation of basic hill climbing in rugged landscapes

N-Queens
- Performs very well with Min-Conflicts strategy
- High success rate for N = 8 and N = 16
- Slightly lower success for N = 32 due to increased complexity

## Conclusion

This project throws hill climbing into two very different environments.

In the Eggholder function, the algorithm often gets comfortable in the first valley it finds. In the N-Queens problem, however, a well-designed heuristic helps it navigate conflicts efficiently and reach a clean solution.

## REFERENCES
Russell & Norvig, Artificial Intelligence: A Modern Approach  
https://code.claude.com/docs/en/overview  
https://code.visualstudio.com/
