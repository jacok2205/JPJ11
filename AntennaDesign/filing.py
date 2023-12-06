"""
    Description:
    ------------
    Facilitates for the various stages of this project to be stored in non-volatile memory.

    Global Variables:
    -----------------
    None.

    Imports:
    --------
    AntennaDesign.__init__:     The initialization module for the package, which will be a list of common public
                                libraries.

    Notes:
    ------
    None.
"""

from AntennaDesign.__init__ import *


class Filing:
    def __init__(self, Directories=None, Debugging=False):
        """"
        Description:
        ------------
        The constructor of the Filing class. It expects 2 parameters (optional), specifically Directories and Debugging.

        Parameters:
        -----------
        Directories:        list
                            A list of string elements that represent the directories that will be created.
        Debugging:          bool
                            For debugging purposes (developer mode).

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        self.__directory__ = str(pkg_resources.files('AntennaDesign') / 'Filing')
        self.__debugging__ = Debugging

        # Initialize/Create default directories (the root directory is Dataset)
        __temp__ = ''
        for __i__ in self.__directory__.split(sep='\\'):
            __temp__ += __i__ + '\\'
            if not os.path.exists(__temp__):
                try:
                    os.mkdir(path=__temp__, mode=0o777)
                except Exception as __error__:
                    if self.__debugging__:
                        print(__error__)

        # Create extra directories according to the defined Directories variable
        if Directories is not None:
            for __i__ in Directories:
                __temp__ = self.__directory__ + '\\'
                for __j__ in __i__.split(sep='\\'):
                    __temp__ += __j__ + '\\'
                    if not os.path.exists(__temp__):
                        try:
                            os.mkdir(path=__temp__, mode=0o777)
                        except Exception as __error__:
                            if self.__debugging__:
                                print(__error__)

    def CreateDirectories(self, Directories=None):
        if Directories is None:
            return

        for __i__ in Directories:
            __temp__ = self.__directory__
            for __j__ in __i__.split(sep='\\'):
                __temp__ += __j__ + '\\'
                if not os.path.exists(__temp__):
                    try:
                        os.mkdir(path=__temp__, mode=0o777)
                    except Exception as __error__:
                        if self.__debugging__:
                            print(__error__)

    def CreateFile(self, Filename):
        if os.path.exists(path=self.__directory__ + Filename):
            return -1
        __temp__ = open(self.__directory__ + Filename, 'w')
        __temp__.close()
        return 0

    def DeleteContent(self, Filename):
        __temp__ = open(self.__directory__ + Filename, 'w')
        __temp__.close()

    def Read(self, Filename):
        """
        Description:
        ------------
        Attempts to read all the contents from the given filename, which should be the full path, including the
        actual file and its extension, to read.

        Parameters:
        -----------
        Filename:                   str
                                    The full path, with the filename and possible extension, of the file
                                    to do the intended operation on.

        Return:
        -------
        If the file does not exist, -1 will be returned, else a list that has been extracted from the file will be returned.

        Notes:
        ------
        This function is executed when generation_file() receives __mode__='read'.
        """

        try:

            with open(self.__directory__ + Filename, 'r') as __file_read__:

                __candidates__ = __file_read__.readlines()

                if len(__candidates__) == 0:
                    raise Exception('File is empty')

                __list__ = []
                for __i__ in __candidates__:

                    try:
                        __first_index__ = __i__.index('[')
                        __last_index__ = __i__.index('\n')
                        __list__.append(ast.literal_eval(__i__[__first_index__: __last_index__]))

                    except Exception as __error__:
                        if self.__debugging__:
                            print(__error__)

                        continue

                __file_read__.close()

                return __list__

        except Exception as __error__:
            if self.__debugging__:
                print(__error__)

            return -1

    def Append(self, Filename, List):
        """
        Description:
        ------------
        Attempts to append a single individual's data.

        Parameters:
        -----------
        __filename__:                   str
                                        The full path, with the filename and possible extension, of the file
                                        to do the intended operation on.
        __candidate_number__:           int
                                        The number to name the individual.
        __gen__:                        list
                                        The data of the individual.
        __custom__:                     bool
                                        When True, the __config__.__generation_number__ global variable is not used.
                                        Conversely, if False, the __config__.__generation_number__ global variable is
                                        used as a postfix to the __filename__ parameter.

        Return:
        -------
        Returns 0 when the operation has been successful, else -1 is returned.

        Notes:
        ------
        This function is executed when generation_file() receives __mode__='append'.
        """

        try:
            __file_append__ = open(f'{self.__directory__ + Filename}', 'a+')
            __file_append__.write(f'{List}\n')

            __file_append__.close()

            return 0

        except Exception as __error__:
            if self.__debugging__:
                print(f'Filing: Append: {__error__}')

            return -1

    def Save(self, Filename, Lists):
        """
        Description:
        ------------
        Attempts to save the full generation data.

        Parameters:
        -----------
        __filename__:                   str
                                        The full path, with the filename and possible extension, of the file
                                        to do the intended operation on.
        __gen__:                        list
                                        A list of all the individuals in current or new generation population, where each
                                        individual is a list.

        Return:
        -------
        Returns 0 when the operation is successfully complete, else -1 is returned.

        Notes:
        ------
        This function is executed when generation_file() receives __mode__='save'.
        """

        try:
            __file_save__ = open(f'{self.__directory__ + Filename}', 'w')

            for __i__ in range(len(Lists)):
                __file_save__.write(f'{__i__} = {Lists[__i__]}\n')
            __file_save__.close()

            return 0

        except Exception as __error__:
            if self.__debugging__:
                print(__error__)

            return -1

    def DeleteFile(self, Filename):
        """
        Description:
        ------------
        Attempts to delete a file given the absolute path to the file.

        Parameters:
        -----------
        __filename__:                   str
                                        The full path, with the filename and possible extension, of the file
                                        to do the intended operation on.

        Return:
        -------
        Returns 0 when the operation is successfully complete, else -1 is returned.

        Notes:
        ------
        This function is executed when generation_file() receives __mode__='delete'.
        """

        try:
            os.remove(self.__directory__ + Filename)

            return 0

        except Exception as __error__:
            if self.__debugging__:
                print(__error__)

        return -1

    def Duplicate(self, Filename, List=None):
        """
        Description:
        ------------
        Updates the 'explored_designs' file if and only if the __gen__ parameter in question is unique,
        i.e., it cannot be found in the 'explored_designs' file. Note that the __S11__ parameter is only
        filled as a list when one wants to update the 'explored_designs' file (to save the S11 response from
        the given __gen__ parameter), hence the geometry list __gen__ and simulation results __S11__ is combined as
        one list when the user wants to save.

        Parameters:
        -----------
        __gen__:                    list
                                    The individual to save, where the list has the format of
                                    [[x1_min, x1_max, y1_min, y1_max], ..., [xn_min, xn_max, yn_min, yn_max]] for layer n.
                                    Default is None.
        __S11__:                    list
                                    A list that contains a frequency range and the S11 responses from those frequency
                                    values, i.e., [freq_range, S11_response]. Default is None.

        Return:
        -------
        The function will attempt to find a match of the __gen__ parameter in the 'explored_designs' file. If a match has
        been found, the associated S11 response list will be returned, else 0 will be returned. -1 is returned when an
        unexpected error occurred.

        Notes:
        ------
        None.
        """

        if List is None:
            return -1

        try:

            # The first element is the chromosome list of an individual (its geometry characteristics) and the second
            # element is the |S11| response values that was collected from CST Studio Suite of the individual, thus:
            # [[layer_1, layer_2, layer_3], [frequencies, |S11| responses]]

            __temp__ = self.Read(Filename=Filename)

            for __index__ in range(len(__temp__)):

                # Proceed when the number of layers between the __gen__ and __temp__[__index__] are the same
                if len(List) == len(__temp__[__index__][0]):

                    __layer_duplicate__ = [False] * len(List)
                    __number_of_duplicates__ = [0] * len(List)

                    # Go through each layer
                    for __i__ in range(len(__temp__[__index__][0])):

                        # Proceed when the first, second, and third elements are equal to one another between
                        # the __gen__ and __config__.__File__[index]. As well as the number of geometry components
                        # between the __gen__ and __config__.__File__[index]
                        if __temp__[__index__][0][__i__][0] == List[__i__][0] and \
                                __temp__[__index__][0][__i__][1] == List[__i__][1] and \
                                __temp__[__index__][0][__i__][2] == List[__i__][2] and \
                                __temp__[__index__][0][__i__][3][0] == List[__i__][3][0] and \
                                __temp__[__index__][0][__i__][3][1] == List[__i__][3][1] and \
                                len(__temp__[__index__][0][__i__][4]) == len(List[__i__][4]):

                            # Go through each geometry component
                            for __j__ in range(len(__temp__[__index__][0][__i__][4])):

                                # If the geometry component is matched with __config__.__File__[index][0][__s__][-1]
                                # geometry component list, increment the appropriate layer counter
                                if __temp__[__index__][0][__i__][4].__contains__(List[__i__][4][__j__]):
                                    __number_of_duplicates__[__i__] += 1

                        # If the value of the geometry component counter is the same as the length of the
                        # __config__.__File__[index][__s__][-1] list (which is the geometry component list), then
                        # the number of duplicates are the same. Thus, this __gen__ parameter must be a duplicate
                        if __number_of_duplicates__[__i__] == len(__temp__[__index__][0][__i__][4]):
                            __layer_duplicate__[__i__] = True

                    # If a duplicate has been found, return the individual
                    if sum(__layer_duplicate__) == len(__layer_duplicate__):
                        return __temp__[__index__][1]

            return False

        # Should an error occur that was unexpected
        except Exception as __error__:
            if self.__debugging__:
                print(__error__)

        return -1
