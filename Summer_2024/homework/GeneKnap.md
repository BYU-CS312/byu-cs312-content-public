### Homework Assignment #14

Show all work neatly.

**Question 1 (5)**:  
Find the optimal alignment using dynamic programming (by hand) of **ATCGT** and **AGTCGA**. Use the Needleman-Wunsch cost function that you will use for the project, namely: $$c_{indel} = 5,~ c_{sub} = 1,~ c_{match} = -3$$.

- Show your complete Dynamic Programming table. Include the edit distance score
    of each cell and show the previous pointer(s) from each cell.
- What is the Edit Distance of the 2 strings?
- Is there more than one optimal alignment?
- Bold the previous pointers along the optimal path from the goal cell.
- Show the alignment of the two strings with the first above the second.


**Question 2 (5)**: Knapsack without repetition

Use dynamic programming to fill a knapsack without repetition having a maximum weight capacity of 10 units with a load of maximum value from the following objects:


| Object | Weight | Value |
| --- | --- | --- |
| A | 1 | 1 |
| B | 2 | 7 |
| C | 5 | 11 |
| D | 6 | 21 |
| E | 7 | 31 |

Show a table giving the maximum value at each weight.
What is the maximum value and what objects does the knapsack comprise of at this weight?
