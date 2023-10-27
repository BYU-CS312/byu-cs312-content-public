### Homework Assignment #14

Show all work neatly.

**Question 1 (5)**:  
Find the optimal alignment using dynamic programming (by hand) of **ATGCC** and **TACGCA**. Use the Needleman-Wunsch cost function that you will use for the project, namely: $$c_{indel} = 5,~ c_{sub} = 1,~ c_{match} = -3$$.

- Show your DP table.
- Circle the optimal alignment cost.
- Extract the optimal alignment(s) from the table (keep back-pointers in the table if you want).

**Question 2 (5)**:  
Use dynamic programming to fill a knapsack without repetition having a weight capacity of 10 units with a load of maximum value from the following set of objects:

- Weights: 1, 2, 5, 6, and 7 units
- Values: 1, 7, 11, 21, and 31, respectively.

Your answer should include:

- a table with solutions to sub-problems
- the value of the optimal load
- the objects to be included in the optimal load (keep back-pointers in the table if you want)