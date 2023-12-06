"""
    Description:
    ------------
    A list of functions/equations that are available for determining the dimensions (width and length) of a rectangular
    microstrip patch antenna by using the Transmission-Line model.

    Global Variables:
    -----------------
    None.

    Imports:
    --------
    __init__:           The initialization module for the package.
    __config__:         Global variables to access from, according to what was configured from the user.

    Notes:
    ------
    None.
"""

from AntennaDesign.__init__ import *


def rmsp_epsilon_effective(__er__, __sub_h__, __patch_width__):
    """
    Description:
    ------------
    Calculates the effective electrical permittivity of a rectangular microstrip patch antenna.

    Parameters:
    -----------
    __er__:             float
                        A positive float value that acts as the electrical permittivity of the substrate and should be
                        greater than or equal to 1.0.
    __sub_h__:          float
                        A positive float value that acts as the height of the substrate and must be greater than 0.0.
    __patch_width__:    float
                        A positive float value that acts as the width of the rectangular microstrip patch antenna and
                        should be greater than 0.0.

    Return:
    -------
    Returns the effective electrical permittivity of the rectangular microstrip patch antenna.

    Notes:
    ------
    None.
    """

    return ((__er__ + 1) / 2) + (((__er__ - 1) / 2) * (1 + 12 * (__sub_h__ / __patch_width__)) ** (-0.5))


class RMPA:
    def __init__(self, fr, er):
        self.__fr__ = fr
        self.__er__ = er
        self.eo = 8.854e-12
        self.uo = 4 * np.pi * 1e-7
        self.__Vo__ = 3e8

    def _rmsp_width(self):
        """
        Description:
        ------------
        Calculates the width of a rectangular microstrip patch antenna.

        Parameters:
        -----------
        __fr__:     float
                    A positive float value that acts as the resonant frequency and is in Hertz.
        __er__:     float
                    A positive float value that acts as the electrical permittivity of the substrate and should be greater
                    than or equal to 1.0.

        Return:
        -------
        Returns the width of the rectangular microstrip patch antenna.

        Notes:
        ------
        None.
        """

        return self.__Vo__ / (2 * self.__fr__) * (2 / (self.__er__ + 1)) ** 0.5

    def _rmsp_delta_length(self, SubstrateHeight, PatchWidth):
        """
        Description:
        ------------
        Calculates the delta length ΔL of the rectangular microstrip patch antenna.

        Parameters:
        -----------
        __sub_h__:          float
                            A positive float value that acts as the height of the substrate and must be greater than 0.0.
        __er__:             float
                            A positive float value that acts as the electrical permittivity of the substrate and should be
                            greater than or equal to 1.0.
        __patch_width__:    float
                            A positive float value that acts as the width of the rectangular microstrip patch antenna and
                            should be greater than 0.0.

        Return:
        -------
        Returns the delta length ΔL of the rectangular microstrip patch antenna.

        Notes:
        ------
        None.
        """

        # Calculate the effective electrical permittivity
        er_eff = rmsp_epsilon_effective(__er__=self.__er__, __sub_h__=SubstrateHeight, __patch_width__=PatchWidth)

        return SubstrateHeight * 0.412 * ((er_eff + 0.3) * (PatchWidth / SubstrateHeight + 0.264)) / \
            ((er_eff - 0.258) * (PatchWidth / SubstrateHeight + 0.8))

    def _rmsp_length(self, __patch_width__, __sub_h__):
        """
        Description:
        ------------
        Calculates the physical length L of the rectangular microstrip patch antenna.

        Parameters:
        -----------
        __fr__:             float
                            A positive float value that acts as the resonant frequency and is in Hertz.
        __er__:             float
                            A positive float value that acts as the electrical permittivity of the substrate and should
                            be greater than or equal to 1.0.
        __patch_width__:    float
                            A positive float value that acts as the width of the rectangular microstrip patch antenna and
                            should be greater than 0.0.
        __sub_h__:          float
                            A positive float value that acts as the height of the substrate and must be greater than 0.0.

        Return:
        -------
        Returns the physical length L of the rectangular microstrip patch antenna.

        Notes:
        ------
        None.
        """

        # Calculate the effective electrical permittivity
        er_eff = rmsp_epsilon_effective(self.__er__, __sub_h__, __patch_width__)

        # Use the determined effective electrical permittivity for calculating the delta length of the microstrip patch
        # antenna
        __delta__ = self._rmsp_delta_length(SubstrateHeight=__sub_h__, PatchWidth=__patch_width__)

        return self.__Vo__ / (2 * self.__fr__ * er_eff**0.5) - 2 * __delta__

    def get_rmsp_dimensions(self, __sub_h__):
        """
        Description:
        ------------
        Calculates the physical dimensions (width and length) of the rectangular microstrip patch antenna.

        Parameters:
        -----------
        __fr__:         float
                        A positive float value that acts as the resonant frequency and is in Hertz.
        __sub_h__:      float
                        A positive float value that acts as the height of the substrate and must be greater than 0.0.
        __er__:         float
                        A positive float value that acts as the electrical permittivity of the substrate and should be
                        greater than or equal to 1.0.

        Return:
        -------
        Returns a list with two variables, namely the width and length, of the rectangular microstrip patch antenna.

        Notes:
        ------
        None.
        """

        # Determine the physical width of the rectangular microstrip patch antenna
        __width__ = self._rmsp_width()

        # Determine the physical length of the rectangular microstrip patch antenna
        __length__ = self._rmsp_length(__patch_width__=__width__, __sub_h__=__sub_h__)

        # Print the results, in millimeter, specifically the width and length of the rectangular microstrip strip patch
        # antenna
        print('Width of rectangular microstrip patch antenna: ' + str(round(__width__ * 1000, 4)) + ' mm')
        print('Length of rectangular microstrip patch antenna: ' + str(round(__length__ * 1000, 4)) + ' mm')

        return __width__, __length__

    def TM_x_mode(self, __m__=0, __n__=0, __p__=0, __er__=1, __h__=1, __L__=1, __W__=1):
        """
        Description:
        ------------
        Calculates the resonant frequency of the rectangular microstrip patch antenna.

        Parameters:
        -----------
        __m__:          int
                        An integer value to represent the number of half-wave cycles on the x-axis. Default is 0.
        __n__:          int
                        An integer value to represent the number of half-wave cycles on the y-axis. Default is 0.
        __p__:          int
                        An integer value to represent the number of half-wave cycles on the z-axis. Default is 0.
        __er__:         float
                        A positive float value that acts as the electrical permittivity of the substrate and should be
                        greater than or equal to 1.0. Default is 1.
        __h__:          float
                        A positive float value that acts as the height of the substrate and must be greater than 0.0.
                        Default is 1.
        __L__:          float
                        A positive float value that acts as the length of the rectangular microstrip patch antenna and
                        should be greater than 0.0. Default is 1.
        __W__:          float
                        A positive float value that acts as the width of the rectangular microstrip patch antenna and
                        should be greater than 0.0. Default is 1.0. Default is 1.

        Return:
        -------
        Returns the resonant frequency of the rectangular microstrip patch antenna given the electrical permittivity of the
        substrate, height of the substrate, width of the antenna substrate, and length of the antenna substrate.

        Notes:
        ------
        None.
        """

        return (1 / (2 * np.pi * (self.eo * self.uo * __er__) ** 0.5)) \
            * ((((__m__ * np.pi) / __h__) ** 2) +
               (((__n__ * np.pi) / __L__) ** 2) +
               (((__p__ * np.pi) / __W__) ** 2)) ** 0.5
