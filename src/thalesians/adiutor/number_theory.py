"""
thalesians.adiutor.number_theory
================================

This module provides tools and utilities for exploring concepts in number theory. 
It includes prime number generation, imbalance computations, base-specific digit operations, 
and feature extraction for numerical analysis. The functions are designed to be efficient and 
flexible, supporting individual numbers as well as iterables.

Key Features
------------
1. **Prime Number Utilities**:
   - Generate primes, prime pairs, and semi-primes.
   - Explore relationships between primes, such as their imbalance.

2. **Digit-Based Computations**:
   - Extract digits of a number in any base.
   - Compute the center of mass of digits.

3. **Numerical Feature Extraction**:
   - Extract detailed features of numbers across multiple bases, including statistics like mean, 
     standard deviation, skewness, and kurtosis of their digits.

4. **Imbalance Analysis**:
   - Calculate imbalance metrics for pairs of numbers, with options for exact or fractional results.

Classes
-------
- None

Functions
---------
### Prime and Semi-Prime Generators
- **primes(max_count=None)**:
  - A generator for prime numbers. Optionally, limits the count of primes.

- **prime_pairs(max_count=None)**:
  - A generator for pairs of primes `(p, q)` such that `p >= q`.

- **semi_primes(max_count=None)**:
  - A generator for semi-primes (products of two primes).

### Imbalance Computations
- **imbalance(p, q)**:
  - Computes the normalized imbalance between two numbers `p` and `q`.

- **imbalance_lowest_terms(p, q)**:
  - Returns the imbalance as a fraction in its lowest terms.

- **imbnum(p, q)**:
  - Returns the numerator of the imbalance fraction.

- **imbden(p, q)**:
  - Returns the denominator of the imbalance fraction.

### Base-Specific Operations
- **centre_of_mass(number, base=10)**:
  - Computes the center of mass of non-zero digits in a number's representation.

- **digits(number, base=10)**:
  - Extracts the digits of a number in a given base.

### Feature Extraction
- **features(number, min_base=2, max_base=30)**:
  - Extracts statistical and structural features of a number across multiple bases.

Internal Helper Functions
-------------------------
- **_features_number(number, min_base, max_base)**:
  - Computes features for a single number.

- **_features_iterable(iterable, min_base, max_base)**:
  - Computes features for an iterable of numbers.

Dependencies
------------
- **fractions**: For exact fractional imbalance calculations.
- **numpy**: For digit-based computations and statistical measures.
- **scipy.stats**: For advanced statistics like skewness and kurtosis.
- **sympy**: For efficient primality testing.

Usage
-----
### Generating Primes
    >>> prime_gen = primes(max_count=5)
    >>> list(prime_gen)
    [2, 3, 5, 7, 11]

### Computing Imbalance
    >>> imbalance(5, 7)
    0.16666666666666666

### Extracting Features
    >>> features(123, min_base=2, max_base=10)
    {'number': 123.0, 'normalized_modulo_2': 0.5, 'number_of_digits_2': 7.0, ...}

### Center of Mass
    >>> centre_of_mass(123, base=10)
    1.0

Testing
-------
The module includes a `_test()` function for `doctest` validation.

Notes
-----
- Feature extraction involves statistical analysis of digit distributions across multiple bases, 
  making it useful for numerical research or exploratory data analysis.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

import fractions
import logging

import numpy as np
from scipy.stats import kurtosis, skew
import sympy

import thalesians.adiutor.checks as checks

def primes(max_count=None):
    """A generator for prime numbers using sympy.isprime."""
    n = 2
    count = 0
    while True:
        if max_count is not None and count == max_count: return
        if sympy.isprime(n):
            count += 1
            yield n
        n += 1

def prime_pairs(max_count=None):
    """A generator for pairs of primes (p, q) such that p >= q using sympy.isprime."""
    primes = []
    n = 2
    count = 0
    while True:
        if max_count is not None and count == max_count: return
        if sympy.isprime(n):
            # Add the new prime to the list
            for prime in primes:
                if max_count is not None and count == max_count: return
                count += 1
                yield (n, prime)
            count += 1
            yield (n, n)  # Include the pair (n, n)
            primes.append(n)
        n += 1

def semi_primes(max_count=None):
    for prime_pair in prime_pairs(max_count):
        yield prime_pair
    return
        
def imbalance(p, q):
    return abs(p - q) / (p + q)

def imbalance_lowest_terms(p, q):
    return fractions.Fraction(abs(p - q), p + q)

def imbnum(p, q):
    return imbalance_lowest_terms(p, q).numerator

def imbden(p, q):
    return imbalance_lowest_terms(p, q).denominator

def centre_of_mass(number, base=10):
    if base < 2: raise ValueError("Base must be at least 2")
    digits = np.base_repr(number, base=base)
    positions = [i for i, digit in enumerate(digits) if digit != '0']
    return sum(positions) / len(positions) if positions else 0

def digits(number, base=10):
    if base < 2: raise ValueError("Base must be at least 2")
    if number < 0: raise ValueError("Number must be non-negative")
    digits = []
    while number > 0:
        digits.append(number % base)
        number //= base
    return digits

def features(number, min_base=2, max_base=30):
    if checks.is_iterable(number):
        result = _features_iterable(number, min_base, max_base)
    else:
        result = _features_number(number, min_base, max_base)
    return result

def _features_number(number, min_base, max_base):
    number_features = {'number': float(number)}
    for base in range(min_base, max_base+1):
        number_digits = digits(number, base)
        number_of_digits = len(number_digits)
        number_centre_of_mass = centre_of_mass(number, base)
        number_features[f'normalized_modulo_{base}'] = float(number % base) / base
        number_features[f'number_of_digits_{base}'] = float(number_of_digits)
        number_features[f'centre_of_mass_{base}'] = number_centre_of_mass
        number_features[f'normalized_centre_of_mass_{base}'] = number_centre_of_mass / number_of_digits
        number_features[f'digits_mean_{base}'] = np.mean(number_digits)
        number_features[f'digits_median_{base}'] = np.median(number_digits)
        number_features[f'digits_std_{base}'] = np.std(number_digits)
        number_features[f'digits_skew_{base}'] = skew(number_digits)
        number_features[f'digits_kurtosis_{base}'] = kurtosis(number_digits)
    for name in number_features:
        if not np.isfinite(number_features[name]): number_features[name] = 0.
    return number_features

def _features_iterable(iterable, min_base, max_base):
    logging.info(f"In _features_iterable, {type(iterable)}, {len(iterable)}")
    iterable_features = {}
    for index, number in enumerate(iterable):
        if index % 100 == 0: logging.info(f'Computing features for number {index+1} of {len(iterable)}...')
        number_features = _features_number(number, min_base, max_base)
        for key in number_features:
            if key not in iterable_features: iterable_features[key] = []
            iterable_features[key].append(number_features[key])
    return iterable_features

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()
