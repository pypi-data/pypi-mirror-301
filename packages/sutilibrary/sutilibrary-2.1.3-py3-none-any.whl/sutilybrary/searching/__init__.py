"""
Searching Algorithms Module

This module provides various searching algorithms and utilities for finding
elements in lists or arrays.
"""

from .searching_algorithms import (
    search,
    linear_search,
    binary_search,
    jump_search,
    interpolation_search,
    exponential_search,
    fibonacci_search,
    sublist_search,
    ternary_search,
    jump_search_2,
    exponential_search_2,
    meta_binary_search,
    galloping_search,
    format_output,
    read_from_file,
    write_to_file
)

__all__ = [
    "search",
    "linear_search",
    "binary_search",
    "jump_search",
    "interpolation_search",
    "exponential_search",
    "fibonacci_search",
    "sublist_search",
    "ternary_search",
    "jump_search_2",
    "exponential_search_2",
    "meta_binary_search",
    "galloping_search",
    "format_output",
    "read_from_file",
    "write_to_file"
]

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Dictionary of available search algorithms
search_algorithms = {
    'linear': linear_search,
    'binary': binary_search,
    'jump': jump_search,
    'interpolation': interpolation_search,
    'exponential': exponential_search,
    'fibonacci': fibonacci_search,
    'sublist': sublist_search,
    'ternary': ternary_search,
    'jump_2': jump_search_2,
    'exponential_2': exponential_search_2,
    'meta_binary': meta_binary_search,
    'galloping': galloping_search
}

# List of available output formats
output_formats = [
    "brackets", "curly_braces", "parentheses", "no_commas", "spaces", "vertical", "horizontal",
    "csv", "tab_separated", "json", "pretty_json", "bullet_points", "numbered_list", "html_list",
    "xml", "yaml", "markdown_table", "latex_array", "binary", "hexadecimal", "scientific_notation",
    "percentage"
]

def get_algorithm_names():
    """Returns a list of available search algorithm names."""
    return list(search_algorithms.keys())

def get_output_formats():
    """Returns a list of available output formats."""
    return output_formats

def get_algorithm(name):
    """
    Returns the search algorithm function by its name.
    
    :param name: Name of the search algorithm
    :return: Search algorithm function
    :raises ValueError: If the algorithm name is not found
    """
    if name not in search_algorithms:
        raise ValueError(f"Unknown search algorithm: {name}")
    return search_algorithms[name]

def is_valid_output_format(format):
    """
    Checks if the given output format is valid.
    
    :param format: Output format to check
    :return: True if valid, False otherwise
    """
    return format in output_formats