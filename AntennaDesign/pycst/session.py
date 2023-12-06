# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 17:15:38 2022

@author: Yates
@contributor: jacok2205
"""

from AntennaDesign.pycst.config import debug as debug


try:
    import win32com.client

except ModuleNotFoundError:
    print("Cheap fix for readthedocs")
    pass


def connect():
    """
    Loads a local CST session.
    
    Since this is a Window-specific API, this functions creates an instance of
    a stand-alone client.
    
    TODO:
        In the far, far future, the need to open a Circuits & Systems or PCB
        instance may be required. I should look into that at some point. 
    """
    try:
        cst = win32com.client.dynamic.Dispatch("CSTStudio.Application")

        return cst

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def close(cst):
    """
    Quits the CST Studio Suite application.

    Parameters
    ----------
    None.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        cst.Quit()
        print("Exiting...")

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1
