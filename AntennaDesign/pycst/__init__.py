# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 17:05:45 2022

@author: mario
"""

from AntennaDesign.pycst.config import *
from AntennaDesign.pycst.home import *
from AntennaDesign.pycst.material import *
from AntennaDesign.pycst.model import *
from AntennaDesign.pycst.post_process import *
from AntennaDesign.pycst.session import *
from AntennaDesign.pycst.simulation import *
# The two tries that follow is to import importlib.resources or importlib_resources
# to access the 'Material' file.
try:
    import importlib.resources as pkg_resources

except ImportError:
    # Try back-ported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

__all__ = ['home', 'material', 'model', 'post_process', 'session', 'simulation', 'config', 'pkg_resources']
