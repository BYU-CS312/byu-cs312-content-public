### Homework Assignment #20

For the following 4-city TSP problems assume that the initial BSSF is infinite and that the city cost/distance matrix is

| []() | | | |
| --- | --- | --- | --- |
| $\infty$ | 7 | 3 | 12 |
| 3 | $\infty$ | 6 | 14 |
| 5 | 8 | $\infty$ | 6 |
| 9 | 3 | 5 | $\infty$ |

This is the same as the previous homework and the initial state should start with the same reduced cost matrix that you did for the previous homework for both problems below.

**Question 1 (5)**:  
Use the partial path state search approach we discussed in class. This assumes the path starts at city 1, each node represents a city, and a link from a parent to a child node in the search space means a path between the cities. Expanding a node means generating a child state for each node to which the parent node has a path.

The state for the root of the search tree is the answer to the last homework. Show the search tree that branch and bound would generate for this problem. Show each state including the reduced cost matrix and bound. Also show when _BSSF_ is updated and use it for proper pruning, etc.

**Question 2 (5)**:  
This time use the include/exclude state search approach we discussed in class. This does not assume a particular start city, and at each branch chooses one edge to include/exclude from the solution. At each branch, choose the edge which maximizes $bound(S_{excluded})~–~bound(S_{included})$

Show the search tree that branch and bound would generate for this problem. Show each state including the reduced cost matrix and bound. Also show when _BSSF_ is updated and use it for proper pruning, etc.


