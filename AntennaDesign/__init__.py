
"""
    Description:
    ------------
    A module to keep all library links.

    Global Variables:
    -----------------
    __all__:                        list
                                    A list of strings, where each string is the name of a module. All elements are
                                    unique.

    Imports:
    --------
    os:                             utility module
                                    Used for file manipulation.
    numpy:                          python library
                                    Used for data manipulation.
    math:                           built-in module
                                    Used for rounding a float value, where the bankers method is used.
    datetime:                       module
                                    Used to keep a date and time stamp after an execution has been made.
    pyplot:                         plotting library
                                    Used for visual realizations of individuals.
    ast:                            module
                                    Used for extracting lists from a file that contains lists.
    pkg_resources:                  module
                                    Used for getting the absolute path of a file or a set of files.

    Notes:
    ------
    None.
"""

import os as os
import numpy as np
import math as math
import datetime as datetime
import time as time
from matplotlib import pyplot as plt
import ast as ast
import importlib.resources as pkg_resources
import random
from AntennaDesign import pycst

__all__ = [
    'os',
    'np',
    'math',
    'datetime',
    'time',
    'pkg_resources',
    'plt',
    'ast',
    'random',
    'pycst'
]
