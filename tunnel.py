import random
import sys

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

def main_run(arr_size, iterations):
    """Run the process for a given number of iterations."""
    tendency = 0
    arr = [0] * arr_size  # Initialize array with n elements
    for _ in range(iterations):
        func = random_choice()  # Choose a function
        arr, tendency = func(arr, tendency)  # Apply the function and update tendency
        #print(f"Array: {arr}, Tendency: {tendency}")  # Print the current state of the array and tendency
    return tendency
if __name__ == "__main__":
    tendey_of_tendecy =[]
    for k in range(3):
        tendency_array = [] 
        for i in range(90):
            tnd = main_run(arr_size=50*(10*i+1), iterations=100)  # iterations for each i 
            tendency_array.append(tnd)
       # print( f' sum of tendency : {sum(tendency_array)}' )  # Print tendency for each array size
        tendey_of_tendecy.append( sum(tendency_array) )

    print( f' sum of tendency of tendencies : {sum(tendey_of_tendecy)}' )
    plt.plot(sum(tendey_of_tendecy) )
    plt.show()
