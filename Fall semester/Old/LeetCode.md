# Project 6: Algorithmic Problem Solving

![Bob the Builder](./images/bob.jpg)

## Purpose and Background

The purpose of this project is to give you hands-on practice with solving algorithmic problems. One of the most important skills you can have as a computer scientist, no matter where your career takes you, is to be able to solve problems. One important part is to be able to implement a known solution, apply an existing algorithm, etc. The other important part is to be able to see a problem and figure out a good/ideal way to solve it.  You need to develop both facets to this problem-solving skill, and the goal of this project is to help you do that.

### Problem Solving Tools

You can think of the topics we've covered in CS 312 as tools in your problem-solving toolbelt. Just like real tools (those on Bob the Builder’s toolbelt), some are for very specific problems, while others can be applied at different times, in different ways. Here are some of the tools that you have learned about and used this semester:

- **Analyzing Algorithms**
    - correctness, complexity, can we do better?
- **Asymptotic Complexity**
    - Big-O, Big-Θ, Big-Ω
- **Divide and Conquer**
    - Master Theorem
- **Greedy Algorithms**
    - Minimum Spanning Trees, Huffman Coding
- **Graph Algorithms**
    - BFS/DFS
    - Linearization/Topological Sort
    - Strongly-connected Components
    - Shortest Paths: Dijkstra’s/Bellman-Ford
- **Dynamic Programming**
    - Longest increasing  subsequence, Edit Distance, Knapsack (0/1, w/reps)
- **Linear Programming**
- **Intelligent Search**
    - Backtracking
    - Branch-and-bound
    - Local Search
- **Complexity Classes** (P, NP, NPC, etc.)
    - NP-Complete: Reductions
- **Approximation Algorithms**
- **Randomized Algorithms**
    - Las Vegas/Monte Carlo

While you have some experience with each of these tools, your practice has generally been limited (sometimes just one class discussion and 1-2 homework problems). 
You also typically have been told which tool to apply in a given situation -- this generally won’t be the case in the real world. 
It is helpful to develop the ability to know which tool or tools to apply in a given situation (i.e. to a given problem to be solved).

This project is intended both to give you a little bit more practice and to help you realize the need for continued practice; it will truly benefit you. 

## Project Description

This project will consist of a set of 12 LeetCode problems of which **you will need to complete at least 6**. 

The specific problems you may choose from are:

- [1137\. N-th Tribonacci Number](https://leetcode.com/problems/n-th-tribonacci-number/) (Easy 63.5%)
- [1\. Two Sum](https://leetcode.com/problems/two-sum/) (Easy 51.1%)
- [39\. Combination Sum](https://leetcode.com/problems/combination-sum/) (Medium 70.3%)
- [1584\. Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) (Medium 66.5%)
- [102\. Binary Tree Level-order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) (Medium 66.1%)
- [547\. Number of Provinces](https://leetcode.com/problems/number-of-provinces/) (Medium 65.6%)
- [120\. Triangle](https://leetcode.com/problems/triangle/) (Medium 55.8%)
- [279\. Perfect Squares](https://leetcode.com/problems/perfect-squares/) (Medium 53.1%)
- [1042\. Flower Planting With No Adjacent](https://leetcode.com/problems/flower-planting-with-no-adjacent/) (Medium 51.0%)
- [207\. Course Schedule](https://leetcode.com/problems/course-schedule/) (Medium 46.3%)
- [406\. Queue Reconstruction by Height](https://leetcode.com/problems/queue-reconstruction-by-height/) (Medium 73.2%)
- [236\. Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) (Medium 60.7%)

<!-- - [11\. Container with Most Water](https://leetcode.com/problems/container-with-most-water/) (Medium 54.3%) -->

There are two parts to the project.

### Part A [36 pts]

For *each* problem that you select, do the following:

1. [6 pts] Solve the problem in LeetCode

Part A is due before Part B. Please review the [course schedule](../../schedule.md) to be clear on the deadlines. 

To submit part A, use this google form: [CS312 - Project 6 - LeetCode Problems](https://docs.google.com/forms/d/e/1FAIpQLSdS6C6Y76yFSa7RbUvsUoz4Z5Hvtt9pq3UOD_0r-90oEa41ZQ/viewform)

Be sure to update your **submission** links, and not the problem description link (i.e. when someone clicks your link, they should go straight to the page that shows your code and the accepted/rejected status).

Please, **do not look at solutions**, on LeetCode or other websites, nor at a classmate’s solution, until **after** you have solved a given problem. If you’re stuck, you can refer to the hints below, but you’re encouraged to try the problem on your own before looking at the hints. If with the hints you’re still stuck, you can reach out to the TAs or to your instructor.

### Part B [60 pts]

Turn in a PDF that includes the following for each problem (up to six) that you solve:

1. Your source code (from part A)
1. [6 pts] Provide a brief analysis of the time and space complexity of your solution
2. [4 pts] Meet with another student in the class that solved the same problem and compare your solutions and problem solving strategies. Then provide a brief report (e.g. one paragraph per problem) describing what you learned and discussed.

To facilitate this part of the project, we will be using lecture time during the last week of class to discuss solutions (please see the [course schedule](../../schedule.md) for the specific date). If you are present in class that day, you will have time to discuss most, if not all, of the six problems you need to have solved with other students during class and will only need to write the report as homework.

If you are unable to attend class that day, you will be responsible for making time and finding other students to meet with to discuss your solutions.

### Extra Credit [30 pts]

You may choose to solve the remaining 6 problems for 5 points of extra credit each. For the extra credit, you only need to solve the problem in LeetCode; you are not required to discuss your solution nor provide a report (though you are welcome to do so). 

### FAQs

Q1.  How fast does our solution need to run?

A1.  Your solution needs to be accepted by LeetCode. Some LeetCode problems are carefully designed such that inefficient algorithms will timeout, but reasonably efficient algorithms will pass (e.g. a quadratic sort will fail, but an $n \log n$ sort will pass). I don't know that they publish the time limit, either per problem or globally, but after solving a problem, you can see the runtime distribution of successful submissions for each problem, for any given language. I’m happy to share that info for the problems I’ve solved (almost all with python3).

Q2.  When reviewing solutions with each other, do we just discuss Big-O?

A2.  No, please discuss each other’s code!  =)  (After both having solved the problem)

Q3.  Do we need to use Python3?

A3.  No, you’re welcome to use any of the languages supported for a given problem.  The purpose of these is for you to practice using algorithms to solve the problems, language is totally secondary.

Q4.  Does our code have to be discussed with someone in the class, or could it be discussed with someone else?

A4.  Please discuss with someone else from class -- they will have solved the problem and therefore you can learn from each other’s solutions.  You’ll be helping them as well.

Q5.  What if I've already done one of the problems on the specified list?

A5. We've specified a list of 12 problems in hopes to provide you with alternatives, both in case you get stuck on one or if you happen to have already done some of them.  If you've already done one or more problems, please choose among the rest of them on the specified list (the TAs are familiar with these problems and we have hints for solving those).  In the event that you solve all of the problems and still need or want more to get the credit you want (whether you want the minimum 6 but have already done 7+ of them, or, if you're trying to earn extra credit by solving N total, but have already solved 12-N+1 or more...) you may select any LeetCode **medium** difficulty problems that have an acceptance rate of less than 50% and use those.  You may substitute problems *if and only if* you have completed (now or previously) all of the problems on the specified list.

### Hints

<details>
    <summary>1137. N-th Tribonacci Number</summary>

HINT 1 of 1: Don’t try to solve recursively, instead try dynamic programming.

</details>

<details>
    <summary>1. Two Sum</summary>

HINT 1 of 2: If you are trying to find two elements that sum to a target $T$, and one might be $a$, then the other would have to be $T-a$.

HINT 2 of 2: An $O(n^2)$ solution is possible and LeetCode will accept it.  However, an $O(n)$ solution is also doable and not very difficult.  A hashtable might come in handy, and it can be done either in two passes, or even just one.

</details>

<details>
    <summary>39. Combination Sum</summary>

HINT 1 of 2: At some level, you need to generate/enumerate all of the ways you can create a given sum, using the candidate values provided (with possible duplicates of the candidates).

HINT 2 of 2: For problems that are asking you to make a sum, it sometimes is helpful to keep track of what composes a partial solution and how far from the solution you are (e.g. the target minus the total of what you have so far).

</details>

<details>
    <summary>1584. Min Cost to Connect All Points</summary>

HINT 1 of 2: This is a graph problem: what are the nodes? what are the edge weights? 

HINT 2 of 2: There are many ways to solve this problem—we discussed several in class and in the HW. How might the density of the graph influence your choice of implementation?

</details>

<details>
    <summary>102. Binary Tree Level-order Traversal</summary>

HINT 1 of 1: You need to group all the nodes of a given level. How might you keep track of nodes for a given level? How might you know what level a given node is on?

</details>

<details>
    <summary>547. Number of Provinces</summary>

HINT 1 of 2: This is another problem you can think of as a graph. City connections are undirected edges. 

HINT 2 of 2: What graph property represents a province?

</details>

<details>
    <summary>120. Triangle</summary>

HINT 1 of 1: If you know the minimum path lengths to all elements at one level, does that help you determine the paths for the next level?

</details>

<details>
    <summary>279. Perfect Squares</summary>

HINT 1 of 1: If you have solved the problem for a smaller number, can that solution help you determine the solution for a larger number?

</details>

<details>
    <summary>1042. Flower Planting With No Adjacent</summary>

HINT 1 of 2: This is a graph problem, much like graph coloring. First you need to construct the graph from the paths (edges). 

HINT 2 of 2: Given the limit on number of edges for each node, can you create a scenario where a node cannot be assigned because it would conflict with a neighboring node? Can a greedy approach work for this problem, or do you need something fancier?

</details>

<details>
    <summary>207. Course Schedule</summary>

HINT 1 of 2: It might be helpful to think about this problem as a graph on courses with prerequisite pairs as edges.

HINT 2 of 2: What’s the problematic graph property that would prevent one from completing all the courses and how can you determine whether that’s present?

</details>

<details>
    <summary>406. Queue Reconstruction by Height</summary>

    HINT 1 of 2: Try building your own queue of different heights and computing the associated $k$ values; how do those $k$ change if you shuffle heights in the queue?

    HINT 2 of 2: Consider the relative ordering of a pair of heights. Also consider how inserting a height into the queue might or might not change the $k$ values.

</details>

<details>
    <summary>236. Lowest Common Ancestor of a Binary Tree</summary>

    HINT 1 of 1: Think about the paths from the root to each of the two nodes in question. How do you find those paths, and how do you compare them. For this problem you want to determine the last node that both paths have in common, the one which is furthest from the root.

</details>


<!-- <details>
    <summary>11. Container with Most Water</summary>

    HINT 1 of 2: This can be solved in multiple ways, but one of the most effective is to solve it with a greedy approach/algorithm.

    HINT 2 of 2: Start with the widest container possible and gradually consider slightly smaller ones.  Think about the two possible containers immediately smaller than the largest, can you eliminate either of them as provably smaller?

</details> -->

