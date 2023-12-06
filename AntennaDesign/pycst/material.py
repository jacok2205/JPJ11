# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 22:34:12 2022

@author: Will
@contributor: jacok2205
"""
import sys

from AntennaDesign.pycst.config import debug as debug

try:
    import importlib.resources as pkg_resources

except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources


def display_available_material():
    """
    Displays all the available materials available for this module. Note that the "Material" file was extracted
    and refined from the CST Studio Suite library.

    Parameters
    ----------
    None.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.

    """

    try:

        try:
            inp_file = (pkg_resources.files('AntennaDesign') / 'pycst\\material')
            file = inp_file.open("r")

        except AttributeError:
            __ver__ = sys.version

            if __ver__[0] == 3 and __ver__[2].isdigit() and not __ver__[3].isdigit() and \
                    int(__ver__[2]) < 9:
                # Python < PY3.9, fall back to method deprecated in PY3.11.
                file = pkg_resources.read_text('AntennaDesign', 'pycst\\material')
            else:
                # or for a file-like stream:
                file = pkg_resources.open_text('AntennaDesign', 'pycst\\material')

        # read all content of a file
        __content__ = file.read()
        __index__ = 0
        __i__ = 0

        print("Available materials from pycst, through CST Studio Suite 2022 Material Library, are:")

        while __index__ < len(__content__):
            if __index__ + 4 < len(__content__) and __content__[__index__: __index__ + 4] == 'Name':
                __string__ = ''
                __index__ += 5
                while __content__[__index__] != '\n':
                    __string__ += __content__[__index__]
                    __index__ += 1
                __string__ = __string__.replace('(', '').replace('"', '').replace(')', '')
                print(f'{__i__ + 1}:\t\t{__string__}')
                __i__ += 1
            __index__ += 1

        file.close()

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def load_material(mws, name):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    name : str
        The name of the material that is to be loaded. Note that it is case sensitive.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:

        try:
            inp_file = (pkg_resources.files('AntennaDesign') / 'pycst\\material')
            file = inp_file.open("r")

        except AttributeError:
            # Python < PY3.9, fall back to method deprecated in PY3.11.
            file = pkg_resources.read_text('AntennaDesign', 'pycst\\material')
            # or for a file-like stream:
            file = pkg_resources.open_text('AntennaDesign', 'pycst\\material')

        # read all content of a file
        __content__ = file.read()

        # check if string present in a file
        if f'material.Name("{name}")' in __content__:
            __string__ = ''
            __index__ = __content__.index(f'material.Name("{name}")')
            while __content__[__index__: __index__ + 2] != '\n\n' and __index__ < len(__content__):
                __string__ += __content__[__index__]
                __index__ += 1

            # Create a material object that is addressed from mws
            material = mws.Material
            # Reset all parameters to their defaults
            material.Reset()
            # Execute string as a sequence of command(s)
            exec(__string__)
            # Create the material
            material.Create()
            format(material)
        else:
            print("Material not found in library.")
        file.close()

        return 0

    # If some error is raised
    except Exception as __error__:
        print(__error__)

    return -1


def custom_material(mws, name, epsilon, mu, tanD, thermalConductivity):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    name : TYPE
        DESCRIPTION.
    epsilon : TYPE
        DESCRIPTION.
    mu : TYPE
        DESCRIPTION.
    tanD : TYPE
        DESCRIPTION.
    thermalConductivity : TYPE
        DESCRIPTION.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        material = mws.Material
        material.Reset()
        material.name(name)
        material.FrqType('all')
        material.Type('Normal')
        material.MaterialUnit('Frequency', 'GHz')
        material.MaterialUnit('Geometry', 'mm')
        material.epsilon(str(epsilon))
        material.Mu(str(mu))
        material.Kappa('0.0')
        material.tanD(str(tanD))
        material.tanDFreq('10.0')
        material.tanDGiven('True')
        material.tanDModel('ConsttanD')
        material.KappaM('0.0')
        material.tanDM('0.0')
        material.tanDMFreq('0.0')
        material.tanDMGiven('False')
        material.tanDMModel('ConstKappa')
        material.DispModelEps('None')
        material.DispModelMu('None')
        material.DispersiveFittingSchemeEps('General 1st')
        material.DispersiveFittingSchemeMu('General 1st')
        material.UseGeneralDispersionEps('False')
        material.UseGeneralDispersionMu('False')
        material.Rho('0.0')
        material.ThermalType('Normal')
        material.thermalConductivity(str(thermalConductivity))
        material.ThermalType('Normal')
        material.SetActiveMaterial('all')
        material.Colour('0.94', '0.82', '0.76')
        material.Wireframe('False')
        material.Transparency('0')
        material.Create()
        format(material)

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1


def delete_material(mws, name):
    """
    Parameters
    ----------
    mws : Active3D Object
        The Active3D object that was created from the win32com object (cst.Active3D()).
    name : str
        Name of the material to be deleted. Note that it is case sensitive.

    Returns
    -------
    Returns -1 if some error occurred, else 0 is returned.
    """

    try:
        mws.material.Delete(name)

        return 0

    except Exception as __error__:
        if debug:
            print(__error__)

    return -1
