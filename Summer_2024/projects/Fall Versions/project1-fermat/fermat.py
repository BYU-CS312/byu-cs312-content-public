import random

# This is main function that is connected to the Test button. You don't need to touch it.
def prime_test(N, k):
	return fermat(N,k), miller_rabin(N,k)

# You will need to implement this function and change the return value.
def mod_exp(x, y, N): 
	return 1
	
# You will need to implement this function and change the return value.   
def fprobability(k):
    return 0.0

# You will need to implement this function and change the return value.   
def mprobability(k):
    return 0.0

# You will need to implement this function and change the return value, which should be
# either 'prime' or 'composite'.
#
# To generate random values for a, you will most likley want to use
# random.randint(low,hi) which gives a random integer between low and
# hi, inclusive.
def fermat(N,k):
	return 'prime'

# You will need to implement this function and change the return value, which should be
# either 'prime' or 'composite'.
#
# To generate random values for a, you will most likley want to use
# random.randint(low,hi) which gives a random integer between low and
#  hi, inclusive.
def miller_rabin(N,k):
	return 'composite'
