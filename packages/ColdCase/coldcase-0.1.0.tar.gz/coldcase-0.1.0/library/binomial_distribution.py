import math
""" 
Description:
    This module provides functions to calculate factorial, combinations, 
    and binomial distribution probabilities.
Functions:
    factorial(n):
    combination(n, r):
    binomial_distribution(n, r, p):
    main(n: int, r: int, p: int) -> None:
Author:
    Andrew Marchese
"""

def factorial(n):
    """
    Calculate the factorial of a given number.
    Parameters:
    n (int): A non-negative integer whose factorial is to be computed.
    Returns:
    int: The factorial of the given number.
    Raises:
    ValueError: If n is a negative integer.
    """

    return math.factorial(n)

def combination(n, r): 
    """
    Calculate the number of combinations (n choose r).
    This function computes the number of ways to choose r items from n items
    without regard to the order of selection. It uses the formula:
        C(n, r) = n! / (r! * (n - r)!)
    Args:
        n (int): The total number of items.
        r (int): The number of items to choose.
    Returns:
        float: The number of combinations.
    """
    
    return factorial(n) / (factorial(r) * factorial(n - r))

def binomial_distribution(n, r, p):
    """
    Calculate the binomial distribution probability.
    Parameters:
    n (int): The number of trials.
    r (int): The number of successful trials.
    p (float): The probability of success on an individual trial.
    Returns:
    float: The probability of having exactly r successes in n trials.
    """
    
    return combination(n, r) * math.pow(p, r) * math.pow(1 - p, n - r)

def main(n: int, r: int, p: int) -> None:
    """
    Calculate and print the binomial distribution for given parameters.
    Args:
        n (int): The number of trials.
        r (int): The number of successful trials.
        p (int): The probability of success in a single trial.
    Returns:
        None
    """
    print(binomial_distribution(n, r, p))

if __name__ == '__main__':
    # n = Number of occurrences of the event of interest
    # r = Number of successful occurrences
    # p = Probability of success per trialp 
    main(n, r, p)
    