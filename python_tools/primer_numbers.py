"""
Implementing the Sieve of Eratosthenes algorithm to find all prime numbers up to a given number.
"""

import math

def sieve_of_eratosthenes(n: int) -> set[int]:
    iter_limit: int = math.isqrt(n)
    print(iter_limit)
    prime_nums: set[int] = set(x for x in range(2, n + 1))
    
    for i in range(2, iter_limit + 1):
        if i in prime_nums:
            multiple: int = 2
            while i * multiple <= n:
                prime_nums.discard(i * multiple)
                multiple += 1

    return prime_nums

if __name__ == "__main__":
    primer_numbers: list[int] = sieve_of_eratosthenes(1_000_000)
    print(len(primer_numbers))