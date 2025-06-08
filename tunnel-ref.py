import os
import sys
import random
import statistics
from tqdm import tqdm
import numpy as np
import math
from collections import Counter

# import matplotlib.pyplot as plt  # Uncomment if plotting is needed

def calculate_mean_numpy(data_list):
    """
    Calculates the mean (average) of a list of numbers using NumPy.

    Args:
        data_list (list): A list of numerical values.

    Returns:
        numpy.float64: The mean of the list.
    """
    # Convert list to a NumPy array for efficient calculation
    numpy_array = np.array(data_list)
    return np.mean(numpy_array)

def calculate_information_content(data_list):
    """
    Calculates the Shannon entropy of a list and compares it to the maximum
    possible entropy if the list values were purely random (uniformly distributed).

    Information content is expressed as a ratio (actual_entropy / max_entropy),
    ranging from 0 (completely predictable) to 1 (maximally random).

    Args:
        data_list (list): The input list of values (can contain numbers, strings, etc.).

    Returns:
        dict: A dictionary containing:
            - 'entropy': The calculated Shannon entropy of the list.
            - 'max_entropy': The maximum possible entropy for the number of unique elements.
            - 'normalized_info_content': The ratio of actual entropy to max entropy.
            - 'message': A descriptive message about the calculation.
    """
    if not data_list:
        return {
            "entropy": 0.0,
            "max_entropy": 0.0,
            "normalized_info_content": 0.0,
            "message": "Empty list provided. Entropy is 0."
        }

    # 1. Calculate frequencies of each unique item
    counts = Counter(data_list)
    total_elements = len(data_list)

    # 2. Calculate probabilities
    probabilities = {item: count / total_elements for item, count in counts.items()}

    # 3. Compute Shannon Entropy (H = -sum(p * log2(p)))
    # We use log2 for entropy in bits
    entropy = 0.0
    for p in probabilities.values():
        if p > 0:  # Ensure p is not zero to avoid math.log2(0) error
            entropy -= p * math.log2(p)

    # 4. Determine Maximum Possible Entropy
    # Max entropy occurs when all unique observed elements are equally probable.
    # H_max = log2(number_of_unique_elements)
    num_unique_elements = len(counts) # Number of unique items observed in the list

    max_entropy = 0.0
    if num_unique_elements > 1:
        max_entropy = math.log2(num_unique_elements)
    # If num_unique_elements is 0 or 1, max_entropy is 0 (log2(1) = 0)

    # 5. Calculate Normalized Information Content
    normalized_info_content = 0.0
    if max_entropy > 0:
        normalized_info_content = entropy / max_entropy
    elif entropy == 0 :
        # If there's only one unique element (or empty list), both entropy and max_entropy are 0.
        # This means there's no randomness to measure, so normalized content is 0 (perfectly predictable).
        normalized_info_content = 0.0

    return {
        "entropy": entropy,
        "max_entropy": max_entropy,
        "normalized_info_content": normalized_info_content,
        "message": "Calculation successful."
    }


def modify_array(arr, tendency, mode="zero", direction="decrease"):
    """
    Modifies the array based on the mode and updates tendency.

    Parameters:
        arr (list): Input array.
        tendency (int): Current tendency value.
        mode (str): 'zero' or 'random'.
        direction (str): 'increase' or 'decrease' tendency.

    Returns:
        tuple: (modified array, updated tendency)
    """
    if direction == "increase":
        tendency += 1
    else:
        tendency -= 1

    if mode == "zero":
        arr = [0] * len(arr)
    elif mode == "random":
        arr = [random.randint(0, sys.maxsize) for _ in arr]
    return arr, tendency


def secure_random_choice(set_zero_fn, set_random_fn):
    """
    Securely choose between two functions using system randomness.

    Returns:
        function: Either set_zero_fn or set_random_fn.
    """
    return set_zero_fn if os.urandom(1)[0] % 2 == 0 else set_random_fn


def main_run(arr_size, iterations, set_zero_fn, set_random_fn):
    """
    Run a randomized transformation on an array multiple times.

    Returns:
        int: Final tendency after transformations.
    """
    arr = [0] * arr_size
    tendency = 0
    for _ in range(iterations):
        func = secure_random_choice(set_zero_fn, set_random_fn)
        arr, tendency = func(arr, tendency)
    return tendency


# Define two variants (original and reversed tendency directions)
def set_to_zero(arr, tendency): return modify_array(arr, tendency, "zero", "decrease")
def set_to_random(arr, tendency): return modify_array(arr, tendency, "random", "increase")
def set_to_zero_alt(arr, tendency): return modify_array(arr, tendency, "zero", "increase")
def set_to_random_alt(arr, tendency): return modify_array(arr, tendency, "random", "decrease")


if __name__ == "__main__":
    for MODE in ["original" , "alt"] :
        #MODE = "alt"  # Change to "original" or "alt" to switch behavior

        if MODE == "original":
            zero_func, rand_func = set_to_zero, set_to_random
        else:
            zero_func, rand_func = set_to_zero_alt, set_to_random_alt

        tendency_results = []
        for _ in tqdm(range(500), desc="Processing"):
            iteration_results = []
            for i in range(1, 100, 50):
                t = main_run(arr_size=50 * (10 * i), iterations=50, set_zero_fn=zero_func, set_random_fn=rand_func)
                iteration_results.append(t)
            tendency_results.append(sum(iteration_results))
        
        print(f"--------------------{MODE}----------------------")
        total = sum(tendency_results)
        print(f"\nSum of tendency of tendencies: {total}")
       
        result1 = calculate_information_content(tendency_results)
        mean1 = calculate_mean_numpy(tendency_results)
        print(f"Mean : {mean1}")
        print(f"  Entropy: {result1['entropy']:.4f} bits")
        print(f"  Max Entropy: {result1['max_entropy']:.4f} bits")
        print(f"  Normalized Information Content: {result1['normalized_info_content']:.4f}")
        print(f"  Message: {result1['message']}\n")
        print("---------------------------------------------ended")
