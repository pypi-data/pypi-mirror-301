from .work_num_algorithm import (
    gcd,
    lcm,
    sieve_of_eratosthenes,
    fast_power,
    prime_factors,
    is_prime,
    extended_gcd,
    chinese_remainder_theorem,
    factorial,
    fibonacci,
    is_perfect_number,
    binomial_coefficient,
    euler_totient,
    modular_inverse,
    NumberError
)

__all__ = [
    'gcd',
    'lcm',
    'sieve_of_eratosthenes',
    'fast_power',
    'prime_factors',
    'is_prime',
    'extended_gcd',
    'chinese_remainder_theorem',
    'factorial',
    'fibonacci',
    'is_perfect_number',
    'binomial_coefficient',
    'euler_totient',
    'modular_inverse',
    'NumberError'
]

__version__ = '1.0.0'

def run_algorithm(algorithm: str, *args):
    algorithms = {
        'gcd': gcd,
        'lcm': lcm,
        'sieve_of_eratosthenes': sieve_of_eratosthenes,
        'fast_power': fast_power,
        'prime_factors': prime_factors,
        'is_prime': is_prime,
        'extended_gcd': extended_gcd,
        'chinese_remainder_theorem': chinese_remainder_theorem,
        'factorial': factorial,
        'fibonacci': fibonacci,
        'is_perfect_number': is_perfect_number,
        'binomial_coefficient': binomial_coefficient,
        'euler_totient': euler_totient,
        'modular_inverse': modular_inverse
    }

    if algorithm not in algorithms:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    return algorithms[algorithm](*args)