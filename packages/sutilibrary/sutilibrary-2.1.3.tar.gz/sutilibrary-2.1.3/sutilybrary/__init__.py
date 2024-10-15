"""
Your Package Name: Comprehensive Algorithms Library
Description: A collection of various algorithms implemented in Python.
"""

# Import sorting algorithms
from .sorting import *

# Import searching algorithms
from .searching import *

from .graph import *

from .work_num import *

from .string import *

__version__ = "0.6.0"

# You can create a dictionary to group algorithms by category
algorithms = {
    'sorting': sorting.__all__,
    'searching': searching.__all__,
    'graph': graph.__all__,
    'work_num': work_num.__all__,
    'string': string.__all__
}

__all__ = (
    sorting.__all__ +
    searching.__all__  + 
    graph.__all__ + 
    work_num.__all__ +
    string.__all__
)