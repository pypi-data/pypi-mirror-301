"""
Your Package Name: Comprehensive Algorithms Library
Description: A collection of various algorithms implemented in Python.
"""

# Import sorting algorithms
from .sorting import *

# Import searching algorithms
from .searching import *

__version__ = "0.2.0"

# You can create a dictionary to group algorithms by category
algorithms = {
    'sorting': sorting.__all__,
    'searching': searching.__all__
}

__all__ = (
    sorting.__all__ +
    searching.__all__ 
)