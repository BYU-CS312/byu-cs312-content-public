# Project 1: Primality Test

![](project1_files/Proj1GUI.png)

## Instructions

1. Download the [provided code](../project1-fermat/project1-fermat.zip/) for Project 1. 
Before you can run the provided GUI, you will need to setup [Python 3 and install PyQT5](../../installing-python.md#python) 
1. You will need to implement the code that will be executed when the "Test Primality" button is clicked. The provided file `fermat.py` includes six functions, three of which are called from the GUI. You will need to implement five of these functions (the sixth simply passes your results back to the GUI):
1. Code up the Fermat primality test pseudocode from Figure 1.8 of the text. You may set $k$ to any value you like (see p. 27). This value indicates how many random trials (values of $a$) are used.
2. Implement modular exponentiation (pseudo-code in Figure 1.4 on p. 19). Your primality test should use your modular exponentiation function and should work properly for numbers as large as 1073741824.
3. Code the probability that $k$ Fermat trials gave you the correct answer -- see the discussion between Figure 1.7 and Figure 1.8.
4. Implement the Miller-Rabin primality test. There is no pseudo-code in the book for this, but you can find what you need in the sidebar on p. 28 and in the discussion that follows.
1. Code the probability that $k$ Miller-Rabin trials gave you the correct answer -- see the note in the sidebar on p. 28 and the discussion below.


## The Miller-Rabin test


Let's say the number we are testing is $N=97$; just as in the Fermat case, we choose a random test in the range $1 ≤ a < N$. Suppose for our test we chose $a=3$; then, 

$$
a^{(N-1)} = 3^{96} = 6362685441135942358474828762538534230890216321 \equiv 1 \pmod {97}, 
$$

as Fermat's theorem says it should. Since this is $1 \pmod {97}$, if we take the square root, we would expect the result to be either 1 or -1. We can check this by computing 

$$
(3^{96})^{(\frac{1}{2})} = 3^{48} = 79766443076872509863361 \equiv 1 \pmod {97}
$$

just as expected. But, since this is also 1, we can take the square root again by computing 

$$
(3^{48})^{\frac{1}{2}} = 3^{24} = 282429536481 \equiv 96 \equiv -1 \pmod {97}.
$$

which passed (still looks prime).


Continuing the sequence (purely for demonstration purposes; once we get a $-1$, we can stop the sequence knowing the number is prime), we can take yet another square root, but since we are now taking the square root of -1, we don't expect such nice 
behavior, and indeed, we get 


$$
(3^{24})^{\frac{1}{2}} = 3^{12} = 531441 \equiv 75 \pmod {97}. 
$$


We can complete the sequence with 

$$
(3^{12})^{\frac{1}{2}} = 3^6 = 729 \equiv 50 \pmod {97}
$$
and
$$
(3^6)^{\frac{1}{2}} = 3^3 = 27 \equiv 27 \pmod {97}, 
$$

and we can't divide the exponent by 2 anymore, so the sequence ends.

To summarize, what we are doing here is repeatedly taking the square root of a number that is $\equiv 1 \pmod N$. 
For a while, the result is, 
not unexpectedly, $1 \pmod N$, but at some point it is $-1 \pmod N$. 
As we know, taking the square root of -1 is weird (though in this modular case that doesn't mean complex numbers; rather, we just get away from 1). 

What Miller and Rabin showed is that for prime numbers, for all choices of $a$, $1 \leq a < N$, this sequence of square roots, starting with a $1 \pmod N$, will either 
consist of all $1 \pmod N$, or, if at some point it changes to something else, that something else will always be $N-1 \equiv -1 \pmod N$, 
which is exactly what we saw in our example. 

What they also showed was that for composites (*including* Carmichael numbers), for 
at least **3/4** of the possible choices for $a$, this will not be the case—either the initial test will not equal 
$1 \pmod N$, just as in the Fermat case, or, if it does, in taking the series of square roots, the first number to show up 
after the sequence of $1$s will be something other than $N-1 \equiv -1 \pmod N$.


Here is another example: suppose $N=561$ and we choose $a=4$. Then, computing our sequence of square roots, we get

$$
4^{560} = \text{a really big number}  \equiv 1 \pmod {561} 
$$

$$
4^{280} = \text{a smaller but still really big number}  \equiv 1 \pmod {561}
$$

$$
4^{140} = \text{a still pretty big number}  \equiv 1 \pmod {561}
$$

$$
4^{70} = 1393796574908163946345982392040522594123776 \equiv 67 \pmod {561} \leftarrow \text{Failed. Composite}. 
$$

Notice that this time, that when we encountered something other than $1 \pmod N$ in the sequence, it was also not $N-1 \equiv -1 \pmod N$.

This is common for composites, but **never** happens for primes. 

Hopefully now it is becoming clear how we can implement an
alternative to the Fermat-test-based primality testing
algorithm with this new information—if our number $N$ passes the initial test $a$
(which is equivalent to a Fermat test, right?), we then compute this sequence of square roots, looking for the first result that is not $1 \pmod N$. 
If there isn't one (because the entire sequence is 1s) or if the first such non-1 number is $N-1 \equiv -1 \pmod N$, 
$N$ has passed one round of the Miller-Rabin test $a$. We still don't know anything for sure (we can only demonstrate that a number is **not** prime vs is *probably* prime). 

So we continue to choose another random $a$ and repeat our test; however, if we instead find that there is a first result in the sequence that is neither $1 \: \text{nor} \: N-1 \equiv -1 \pmod N$, then we know the number is composite.


## Submission


A report consisting of: 

1. [10 points] At least one screenshot of your application with a working example (distinct from the one above).
2. All of the code that you wrote. 
  - [20 points] A correct implementation of modular exponentiation.
  - [20 points] A correct implementation of the Fermat primality tester.
  - [20 points] A correct implementation of the check for Carmichael numbers.

3. [10 points] Explain the time and space complexity of your algorithm by showing and summing up the complexity of each subsection of your code. 
  NOTE: to make this easy for the TAs to find, this should appear as a subsection of your report (that is,it is great to have this info in your code comments, but you should also pull it out and include it in the report proper).
1. [10 points] Discuss the equation you used to compute the probability $p$ of correctness that appears in the output.


Note that there is no performance requirement for this project. Correctness is the only criterion.

Submit as a PDF by following the submission directions in the course syllabus.


