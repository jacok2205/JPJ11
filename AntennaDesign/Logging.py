"""
    Description:
    ------------
    Enables logging of progress from the coarse modeling, to the optimization of the surrogate modeling.

    Global Variables:
    -----------------
    None.

    Imports:
    --------
    __init__:               The initialization module for the package.
    __config__:             Global variables to access from, according to what was configured from the user.

    Notes:
    ------
    None.
"""

from AntennaDesign.__init__ import *
from AntennaDesign import __config__ as __config__


def __log__(__module__='coarse_model', __indices__=None, __override__=False, __place_holder__=-1):
    """
    Description:
    ------------
    Logs the actions taken from this package (coarse_model). Note that the time stamp is in CAT time. The
    __config__.__date_time__ variable is updated with the format stipulated from __config__.__misc__[0] variable.

    Parameters:
    -----------
    __indices__:        list
                        A list that is mapped from the __config__.__misc__ variable to log the correct message/progress
                        being taken. Default is None.
    __override__:       bool
                        Used to override the date and time stamp when the coarse_model module is being freshly executed.
                        This is to ensure a consistent system_logging system. Default is False.
    __place_holder__:   int
                        Used to update certain messages that don't have a 'f' operator prepended in a string, see
                        __config__.__misc__ variable. Default is -1.

    Return:
    -------
    Returns the latest date and time stamp without any double quote characters which is common when converting a
    datetime.datetime.now() object to a str object.

    Notes:
    ------
    None.
    """

    __config__.__date_time__ = str(datetime.datetime.now().strftime(__config__.__misc__[0])).replace('"', '')

    if not __override__:
        __config__.__misc__[1] = __config__.__date_time__ + ":\t\t"

    if __indices__ is not None:

        if __module__ == 'coarse_model':
            __log_file_index__ = 5
        elif __module__ == 'fine_model':
            __log_file_index__ = 20
        elif __module__ == 'optimization':
            __log_file_index__ = 30
        else:
            return -1

        __config__.__log_file__ = open(__config__.__files__[__log_file_index__], 'a+')

        if not __override__:
            __config__.__log_file__.write(__config__.__misc__[1])

        for __i__ in range(len(__indices__)):

            if __place_holder__ != -1 and __i__ + 1 >= len(__indices__):
                __config__.__misc__[__indices__[__i__]] = __config__.__misc__[__indices__[__i__]].\
                    format(__place_holder__)
            __config__.__log_file__.write(__config__.__misc__[__indices__[__i__]])

        __config__.__log_file__.write('\n')
        __config__.__log_file__.close()

    return datetime.datetime.now().strftime(__config__.__misc__[0]).replace('"', '')
