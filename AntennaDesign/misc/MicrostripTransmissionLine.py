"""
    Description:
    ------------
    A list of functions/equations that are available for determining the dimensions (width and length) of a microstrip
    transmission line using the ideal microstrip transmission line method from Ulaby.

    Global Variables:
    -----------------
    None.

    Imports:
    --------
    __init__:           The initialization module for the package.

    Notes:
    ------
    None.
"""

from AntennaDesign.__init__ import *


def x(__er__):
    """
    Description:
    ------------
    Calculates the sub equation within the equation of determining the propagation velocity.

    Parameters:
    -----------
    __er__:     float
                A positive float value that acts as the electrical permittivity of the substrate and should be greater
                than or equal to 1.0.

    Return:
    -------
    Returns the x value of the larger equation, see equation 2.30 from JPJ11 OneNote labbook.

    Notes:
    ------
    None.
    """

    return 0.56 * ((__er__ - 0.9) / (__er__ + 3)) ** 0.05


def y(__ms_w__, __sub_h__):
    """
    Description:
    ------------
    Calculates the sub equation within the equation of determining the propagation velocity.

    Parameters:
    -----------
    __ms_w__:   float
                The width of the microstrip transmission line and should be greater than 0.0.
    __sub_h__:  float
                A positive float value that acts as the height of the substrate and must be greater than 0.0.

    Return:
    -------
    Returns the y value of the larger equation, see equation 2.31 from JPJ11 OneNote labbook.

    Notes:
    ------
    None.
    """

    return 1 + 0.02 * np.log(((__ms_w__ / __sub_h__) ** 4 + 3.7e-4 * (__ms_w__ / __sub_h__) ** 2) /
                             ((__ms_w__ / __sub_h__) ** 4 + 0.43)) + 0.05 * \
        np.log(1 + 1.7e-4 * (__ms_w__ / __sub_h__) ** 3)


def effective_epsilon(__er__, __ms_w__, __sub_h__):
    """
    Description:
    ------------
    Calculates the effective electrical permittivity of the substrate given the relative permittivity of the substrate,
    the microstrip transmission line width and the substrate height.

    Parameters:
    -----------
    __er__:     float
                A positive float value that acts as the electrical permittivity of the substrate and should be greater
                than or equal to 1.0.
    __ms_w__:   float
                The width of the microstrip transmission line.
    __sub_h__:  float
                A positive float value that acts as the height of the substrate and must be greater than 0.0.

    Return:
    -------
    Returns the effective electrical permittivity of the substrate.

    Notes:
    ------
    Functions x() and y() are used for calculating the effective permittivity of the substrate.
    """

    return (__er__ + 1) / 2 + (__er__ - 1) / 2 * (1 + 10 * (__ms_w__ / __sub_h__)) \
        ** (-x(__er__) * y(__ms_w__, __sub_h__))


def q(__er__, __Zo__):
    """
    Description:
    ------------
    Calculates the sub equation within the equation of determining the width-to-height ratio.

    Parameters:
    -----------
    __er__:     float
                A positive float value that acts as the electrical permittivity of the substrate and should be greater
                than or equal to 1.0.
    __Zo__:     float
                A positive float value that acts as the characteristic impedance of the microstrip transmission line.

    Return:
    -------
    Returns the q value of the larger equation, see equation 2.35b from JPJ11 OneNote labbook.

    Notes:
    ------
    This function is only used when Zo <= (44 - 2 * er) ohm.
    """

    return (60 * np.pi ** 2) / (__Zo__ * __er__ ** 0.5)


def p(__er__, __Zo__):
    """
    Description:
    ------------
    Calculates the sub equation within the equation of determining the width-to-height ratio.

    Parameters:
    -----------
    __er__:     float
                A positive float value that acts as the electrical permittivity of the substrate and should be greater
                than or equal to 1.0.
    __Zo__:     float
                A positive float value that acts as the characteristic impedance of the microstrip transmission line.

    Return:
    -------
    Returns the p value of the larger equation, see equation 2.36b from OneNote labbook.

    Notes:
    ------
    This function is only used when Zo >= (44 - 2 * er) ohm.
    """

    return ((__er__ + 1) / 2) ** 0.5 * (__Zo__ / 60) + ((__er__ - 1) / (__er__ + 1)) * (0.23 + 0.12 / __er__)


def microstrip_width(__sub_h__, __er__, __Zo__):
    """
    Description:
    ------------
    Calculates the width of a microstrip transmission line.

    Parameters:
    -----------
    __sub_h__:  float
                A positive float value that acts as the height of the substrate and must be greater than 0.0.
    __er__:     float
                A positive float value that acts as the electrical permittivity of the substrate and should be greater
                than or equal to 1.0.
    __Zo__:     float
                A positive float value that acts as the characteristic impedance of the microstrip transmission line.

    Return:
    -------
    Returns the width of the microstrip transmission line.

    Notes:
    ------
    Functions p() and q() are used as part of the whole equation.
    """

    if __Zo__ <= (44 - 2 * __er__):
        result = __sub_h__ * 2 / np.pi * ((q(__er__, __Zo__) - 1) -
                                          np.log(2 * q(__er__, __Zo__) - 1) +
                                          (__er__ - 1) / (2 * __er__) *
                                          (np.log(q(__er__, __Zo__) - 1) + 0.29 - 0.52 / __er__))

    else:
        result = __sub_h__ * ((8 * np.e ** p(__er__, __Zo__)) / (np.e ** (2 * p(__er__, __Zo__)) - 2))

    print("Microstrip transmission line width is " + str(round(result, 4) * 1000) + "mm")

    return result


def wavelength_in_air(__freq__):
    """
    Description:
    ------------
    Calculates the free space wavelength given the frequency __freq__ parameter.

    Parameters:
    -----------
    __freq__:   float
                The frequency used for determining the free-space wavelength and is in Hertz.

    Return:
    -------
    Returns the free space wavelength given the frequency __freq__.

    Notes:
    ------
    None.
    """

    return 3e8 / __freq__


def microstrip_length(__freq__, __er__):
    """
    Description:
    ------------
    Calculates the length of the microstrip transmission line.

    Parameters:
    -----------
    __freq__:   float
                A positive float value that acts as the resonant frequency and is in Hertz.
    __er__:     float
                A positive float value that acts as the electrical permittivity of the substrate and should be greater
                than or equal to 1.0.

    Return:
    -------
    Returns the length of the microstrip transmission line.

    Notes:
    ------
    None.
    """

    # Calculate the wavelength
    __result__ = wavelength_in_air(__freq__) / __er__ ** 0.5

    # Print the minimum length of the microstrip line, which is a quarter-wavelength
    print("Microstrip transmission line length must be a factor of " + str(round(__result__, 4) * 1000 / 4) +
          " mm (1/4 wavelength)")

    return __result__


def get_microstrip_transmission_dimensions(__freq__, __er__, __sub_h__, __Zo__):
    """
    Description:
    ------------
    Calculates the dimensions, width and length, of the microstrip transmission line.

    Parameters:
    -----------
    __freq__:   float
                A positive float value that acts as the resonant frequency and is in Hertz.
    __er__:     float
                A positive float value that acts as the electrical permittivity of the substrate and should be greater
                than or equal to 1.0.
    __sub_h__:  float
                A positive float value that acts as the height of the substrate and must be greater than 0.0.
    __Zo__:     float
                A positive float value that acts as the characteristic impedance of the microstrip transmission line.

    Return:
    -------
    Returns a list with two variables, namely the width and length, which are the dimensions of the microstrip
    transmission line.

    Notes:
    ------
    None.
    """

    # Calculate the width
    __width__ = microstrip_width(__sub_h__, __er__, __Zo__)

    # Calculate the length
    __length__ = microstrip_length(__freq__, __er__)

    return __width__, __length__
