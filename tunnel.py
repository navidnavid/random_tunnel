import os
import random
import sys
from tqdm import tqdm
import matplotlib.pyplot as plt

def set_to_zero(arr, tendency):
    """Set all elements of the array to zero and decrease tendency."""
    tendency -= 1
    return [0] * len(arr), tendency

def set_to_random(arr, tendency):
    """Set all elements of the array to random values and increase tendency."""
    tendency += 1
    return [random.randint(0, sys.maxsize) for _ in arr], tendency

def random_choice():
    """Choose randomly between set_to_zero and set_to_random with 50/50 probability."""
    return random.choice([set_to_zero, set_to_random])


def secure_random_choice():
    """
    Chooses between set_to_zero and set_to_random with a 50/50 probability
    using system-level cryptographic randomness.
    """
    # os.urandom(1) returns 1 byte of random data (0-255).
    # We check if the byte value is even or odd to make a 50/50 choice.
    random_byte = os.urandom(1)
    if random_byte[0] % 2 == 0: # Check if the byte's integer value is even
        return set_to_zero
    else: # It's odd
        return set_to_random


def main_run(arr_size, iterations):
    """Run the process for a given number of iterations."""
    tendency = 0
    arr = [0] * arr_size  # Initialize array with n elements
    for _ in range(iterations):
        # func_p = random_choice()  # Choose a function
        func_p = secure_random_choice()
        arr, tendency = func_p(arr, tendency)  # Apply the function and update tendency
        #print(f"Array: {arr}, Tendency: {tendency}")  # Print the current state of the array and tendency
    return tendency
if __name__ == "__main__":
    tendey_of_tendecy =[]
    for ii in tqdm(range(100), desc="Processing"):
        tendency_array = [] 
        for i in range(1,200,50):
            tnd = main_run(arr_size=50*(10*i), iterations=20)  # iterations for each i 
            tendency_array.append(tnd)
       # print( f' sum of tendency : {sum(tendency_array)}' )  # Print tendency for each array size
        tendey_of_tendecy.append( sum(tendency_array) )

    sum_tend_tend = sum(tendey_of_tendecy)
    print(f' sum of tendency of tendencies : {sum_tend_tend}')
    plt.xlabel(f"itr, sum total tendency {sum_tend_tend} ")
    plt.ylabel(f"tendey_of_tendecy ")
    plt.plot(tendey_of_tendecy)
    plt.savefig(f"tendency_plot_{sum_tend_tend}.png")
    plt.show()
