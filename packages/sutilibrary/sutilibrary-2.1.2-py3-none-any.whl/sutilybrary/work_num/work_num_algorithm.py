import math
import argparse
from typing import List, Tuple
import json

class NumberError(Exception):
    pass

def gcd(a: int, b: int) -> int:
    if a == 0 and b == 0:
        raise NumberError("GCD is undefined for 0 and 0")
    while b:
        a, b = b, a % b
    return abs(a)

def lcm(a: int, b: int) -> int:
    if a == 0 and b == 0:
        raise NumberError("LCM is undefined for 0 and 0")
    return abs(a * b) // gcd(a, b)

def sieve_of_eratosthenes(n: int) -> List[int]:
    if n < 2:
        return []
    primes = [True] * (n + 1)
    primes[0] = primes[1] = False
    for i in range(2, int(n**0.5) + 1):
        if primes[i]:
            for j in range(i*i, n+1, i):
                primes[j] = False
    return [i for i in range(n+1) if primes[i]]

def fast_power(base: int, exponent: int, modulus: int = None) -> int:
    if exponent < 0:
        raise NumberError("Exponent must be non-negative")
    result = 1
    while exponent > 0:
        if exponent & 1:
            result = result * base if modulus is None else (result * base) % modulus
        exponent >>= 1
        base = base * base if modulus is None else (base * base) % modulus
    return result

def prime_factors(n: int) -> List[int]:
    if n < 2:
        raise NumberError("Number must be greater than 1")
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
        if d * d > n:
            if n > 1:
                factors.append(n)
            break
    return factors

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0 and b == 0:
        raise NumberError("GCD is undefined for 0 and 0")
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def chinese_remainder_theorem(remainders: List[int], moduli: List[int]) -> int:
    if len(remainders) != len(moduli):
        raise NumberError("The number of remainders must equal the number of moduli")
    total = 0
    product = math.prod(moduli)
    for remainder, modulus in zip(remainders, moduli):
        p = product // modulus
        total += remainder * pow(p, -1, modulus) * p
    return total % product

def factorial(n: int) -> int:
    if n < 0:
        raise NumberError("Factorial is undefined for negative numbers")
    return math.factorial(n)

def fibonacci(n: int) -> int:
    if n < 0:
        raise NumberError("Fibonacci is undefined for negative numbers")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def is_perfect_number(n: int) -> bool:
    if n <= 1:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def binomial_coefficient(n: int, k: int) -> int:
    if k < 0 or k > n:
        raise NumberError("k must be between 0 and n")
    return math.comb(n, k)

def euler_totient(n: int) -> int:
    if n < 1:
        raise NumberError("n must be positive")
    result = n
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            while n % i == 0:
                n //= i
            result *= (1 - (1 / i))
    if n > 1:
        result *= (1 - (1 / n))
    return int(result)

def modular_inverse(a: int, m: int) -> int:
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise NumberError("Modular inverse does not exist")
    return x % m

def run_algorithm(algorithm: str, *args):
    try:
        if algorithm == 'gcd':
            return gcd(*map(int, args))
        elif algorithm == 'lcm':
            return lcm(*map(int, args))
        elif algorithm == 'sieve_of_eratosthenes':
            return sieve_of_eratosthenes(int(args[0]))
        elif algorithm == 'fast_power':
            return fast_power(*map(int, args))
        elif algorithm == 'prime_factors':
            return prime_factors(int(args[0]))
        elif algorithm == 'is_prime':
            return is_prime(int(args[0]))
        elif algorithm == 'extended_gcd':
            return extended_gcd(*map(int, args))
        elif algorithm == 'chinese_remainder_theorem':
            remainders = list(map(int, args[0].split(',')))
            moduli = list(map(int, args[1].split(',')))
            return chinese_remainder_theorem(remainders, moduli)
        elif algorithm == 'factorial':
            return factorial(int(args[0]))
        elif algorithm == 'fibonacci':
            return fibonacci(int(args[0]))
        elif algorithm == 'is_perfect_number':
            return is_perfect_number(int(args[0]))
        elif algorithm == 'binomial_coefficient':
            return binomial_coefficient(*map(int, args))
        elif algorithm == 'euler_totient':
            return euler_totient(int(args[0]))
        elif algorithm == 'modular_inverse':
            return modular_inverse(*map(int, args))
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    except NumberError as e:
        raise
    except ValueError as e:
        raise NumberError(f"Invalid input: {e}")
    except OverflowError:
        raise NumberError("Number too large to compute")
    except Exception as e:
        raise NumberError(f"Unexpected error: {e}")

def save_result(result, filename):
    try:
        with open(filename, 'w') as f:
            json.dump({"result": result}, f)
        print(f"Result saved to {filename}")
    except IOError as e:
        print(f"Error saving result: {e}")

def main():
    parser = argparse.ArgumentParser(description="Number Algorithms")
    parser.add_argument('algorithm', choices=[
        'gcd', 'lcm', 'sieve_of_eratosthenes', 'fast_power', 'prime_factors',
        'is_prime', 'extended_gcd', 'chinese_remainder_theorem', 'factorial',
        'fibonacci', 'is_perfect_number', 'binomial_coefficient', 'euler_totient',
        'modular_inverse'
    ], help="Choose an algorithm")
    parser.add_argument('args', nargs='*', help="Arguments for the algorithm")
    parser.add_argument('--output', '-o', help="Output file for the result")
    
    args = parser.parse_args()
    
    try:
        result = run_algorithm(args.algorithm, *args.args)
        print(result)
        
        if args.output:
            save_result(result, args.output)
    except NumberError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()