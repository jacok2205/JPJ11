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
    datetime:                       built-in module
                                    Used to keep a date and time stamp after an execution has been made.
    time:                           built-in module
                                    Used for keeping relative track of time for processes.
    pkg_resources:                  built-in module
                                    Used for getting the absolute path of a file or a set of files.
    pyplot:                         plotting library
                                    Used for visual realizations of individuals.
    ast:                            built-in module
                                    Used for extracting lists from a file that contains lists.
    random:                         built-in module
                                    Used for generating random values within a defined range.
    copy:                           built-in module
                                    Used to generate deep copies of lists.
    pycst:                          module
                                    Used as the 'driver' for controlling the CST Studio Suite software.

    Notes:
    ------
    None.
"""

import os as os
import numpy as np
import math as math
import datetime as datetime
import time as time
import importlib.resources as pkg_resources
from matplotlib import pyplot as plt
import ast as ast
import random
import copy
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
    'copy',
    'pycst'
]
