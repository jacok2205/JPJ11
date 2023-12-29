# The initialization module for the package AntennaDesign, which will be a list of common public libraries,
# see AntennaDesign.__init__ for more information
from AntennaDesign.__init__ import *


class Filing:
    """
    Description:
    ------------
    Facilitates for the various stages of this project to be stored in non-volatile memory for later use.

    Attributes:
    -----------
    __directory__:                  str
                                    A private attribute that the class uses as its root directory.
    __debugging__:                  bool
                                    For debugging purposes (developer mode).

    Methods:
    --------
    __init__(Directories=None, Debugging=False):
                                    The constructor of the class, where a predefined set of directories
                                    could be assigned as an argument and debugging can be enabled if debugging
                                    the project.
    CreateDirectories(Directories=None):
                                    The same functionality for when the method __init__ with Directories. It simply
                                    creates a tree of directories defined by the user, where a list of str type
                                    elements are used to define the directory path(s) and names.
    CreateFile(Filename):
                                    Used to create a file given the path Filename, along with its file extension
                                    (optional).
    DeleteContent(Filename):
                                    The data retained within the file is erased given the full path, from '\\Filing',
                                    including the file extension (optional).
    Read(Filename):
                                    The data within the file is extracted into a list of lists, where each element
                                    is a single data point. The format is [parameters, [[return loss frequency
                                    range, return loss responses], [gain frequency range, gain responses]]].
    Append(Filename, List):
                                    The List parameter is appended to the file given the Filename.
    Save(Filename, Lists):
                                    The file is overwritten with the data contained in the Lists parameter. This
                                    parameter is a list of lists with the same format as the Read function.
    DeleteFile(Filename):
                                    The file is permanently deleted given the Filename.
    Duplicate(Filename, List):
                                    The file, given the Filename, is searched through, where if a match occurs between
                                    the List parameter and current line of data, the full line is returned in the
                                    same format as the Read function, but only for a single data point. If no match
                                    has been found, False is returned.

    Notes:
    ------
    None.
    """

    def __init__(self, Directories=None, Debugging=False):
        """
        Description:
        ------------
        The constructor of the Filing class. It expects 2 parameters (optional), specifically Directories and Debugging.

        Parameters:
        -----------
        Directories:                list
                                    A list of string elements that represent the directories that will be created.
        Debugging:                  bool
                                    For debugging purposes (developer mode).

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        # Create an absolute path string with the 'Filing' directory that potentially does not yet exist
        self.__directory__ = str(pkg_resources.files('AntennaDesign') / 'Filing')
        # For debugging (developer mode)
        self.__debugging__ = Debugging

        # Initialize/Create default directories (the root directory is Filing)
        __temp__ = ''
        for __i__ in self.__directory__.split(sep='\\'):
            __temp__ += __i__ + '\\'
            if not os.path.exists(__temp__):
                try:
                    os.mkdir(path=__temp__, mode=0o777)
                except Exception as __error__:
                    if self.__debugging__:
                        print(f'<Filing: __init__: {__error__}>')

        # Create extra directories according to the defined Directories, if not None, parameter
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
                                print(f'<Filing: __init__: {__error__}>')

    def CreateDirectories(self, Directories=None):
        """
        Description:
        ------------
        Creates a tree of directories under the root directory defined in the constructor of this class.

        Parameters:
        -----------
        Directories:                list
                                    A list of str type elements that are used to create the directory(ies).

        Returns:
        --------
        Returns 0 if all/most the directories received from Directories has been created, else -1 if
        Directories is of None type.

        Notes:
        ------
        None.
        """

        if Directories is None:
            return -1

        for __i__ in Directories:
            __temp__ = self.__directory__
            for __j__ in __i__.split(sep='\\'):
                __temp__ += __j__ + '\\'
                if not os.path.exists(__temp__):
                    try:
                        os.mkdir(path=__temp__, mode=0o777)
                    except Exception as __error__:
                        if self.__debugging__:
                            print(f'<Filing: CreateDirectories: {__error__}>')

        return 0

    def CreateFile(self, Filename):
        """
        Description:
        ------------
        Creates a file given the Filename parameter.

        Parameters:
        -----------
        Filename:                   str
                                    The name of the file to be created. Note that the extensions should be
                                    specified if the user wishes so.

        Returns:
        --------
        Returns 0 if the file was created successfully, else -1 if the file already exists.

        Notes:
        ------
        None.
        """

        if os.path.exists(path=self.__directory__ + Filename):
            return -1

        __temp__ = open(self.__directory__ + Filename, 'w')
        __temp__.close()

        return 0

    def DeleteContent(self, Filename):
        """
        Description:
        ------------
        Wipes the content/data within the specified file.

        Parameters:
        -----------
        Filename:                   str
                                    The name of the file for the data to be erased. If an extension to the file
                                    exists, it must be included.

        Returns:
        --------
        None.

        Notes:
        ------
        If the file does not exist, the file will be created without the intention of doing so.
        """

        __temp__ = open(self.__directory__ + Filename, 'w')
        __temp__.close()

    def Read(self, Filename):
        """
        Description:
        ------------
        Attempts to read all the contents from the given filename, which should be the full path, including the
        extension, to read.

        Parameters:
        -----------
        Filename:                   str
                                    The full path, with the filename and possible extension, of the file
                                    to do the intended operation on.

        Returns:
        -------
        If the file does not exist, -1 will be returned, else a list that has been extracted from the file
        will be returned.

        Notes:
        ------
        None.
        """

        try:

            with open(self.__directory__ + Filename, 'r') as __file_read__:

                __candidates__ = __file_read__.readlines()

                if len(__candidates__) == 0:
                    raise Exception('<Filing: Read: File is empty>')

                __list__ = []
                for __i__ in __candidates__:

                    try:
                        __first_index__ = __i__.index('[')
                        __last_index__ = __i__.index('\n')
                        __list__.append(ast.literal_eval(__i__[__first_index__: __last_index__]))

                    except Exception as __error__:
                        if self.__debugging__:
                            print(f'<Filing: Read: {__error__}>')

                        continue

                __file_read__.close()

                return __list__

        except Exception as __error__:
            if self.__debugging__:
                print(f'<Filing: Read: {__error__}>')

        return -1

    def Append(self, Filename, List):
        """
        Description:
        ------------
        Attempts to append a list to a file with Filename.

        Parameters:
        -----------
        Filename:                   str
                                    The full path, with the filename and possible extension, of the file to do the
                                    intended operation on.
        List:                       list
                                    A list to be appended onto the file Filename.

        Return:
        -------
        Returns 0 when the operation has been successful, else -1 is returned.

        Notes:
        ------
        None.
        """

        try:

            __file_append__ = open(f'{self.__directory__ + Filename}', 'a+')
            __file_append__.write(f'{List}\n')
            __file_append__.close()

            return 0

        except Exception as __error__:

            if self.__debugging__:
                print(f'<Filing: Append: {__error__}>')

            return -1

    def Save(self, Filename, Lists):
        """
        Description:
        ------------
        Attempts to save all the contents in the Lists parameter given the filename.

        Parameters:
        -----------
        Filename:                   str
                                    The full path, with the filename and possible extension, of the file to do the
                                    intended operation on.
        Lists:                      list
                                    A list of lists to save into the file given the Filename parameter. Note that
                                    all the data within the file will be replaced with the content from the Lists
                                    parameter.

        Return:
        -------
        Returns 0 when the operation is successfully complete, else -1 is returned.

        Notes:
        ------
        None.
        """

        try:
            __file_save__ = open(f'{self.__directory__ + Filename}', 'w')

            for __i__ in range(len(Lists)):
                __file_save__.write(f'{Lists[__i__]}\n')
            __file_save__.close()

            return 0

        except Exception as __error__:

            if self.__debugging__:
                print(f'<Filing: Save: {__error__}>')

            return -1

    def DeleteFile(self, Filename):
        """
        Description:
        ------------
        Attempts to delete a file given the absolute path to the file.

        Parameters:
        -----------
        Filename:                   str
                                    The full path, with the filename and possible extension, of the file to do the
                                    intended operation on.

        Return:
        -------
        Returns 0 when the operation is successfully complete, else -1 is returned.

        Notes:
        ------
        None.
        """

        try:
            os.remove(self.__directory__ + Filename)

            return 0

        except Exception as __error__:
            if self.__debugging__:
                print(f'<Filing: DeleteFile: {__error__}>')

        return -1

    def Duplicate(self, Filename, List=None):
        """
        Description:
        ------------
        Searches for a match in the file Filename with the provided list List.

        Parameters:
        -----------
        Filename:                   str
                                    The full path, with the filename and possible extension, of the file to do the
                                    search on.
        List:                       list
                                    The list to compare the data within the file Filename with.

        Return:
        -------
        If a match occurs, the full list, with its simulation results, will be returned in the format of
        [parameters, [[return loss frequency range, return loss responses], [gain frequency range, gain]]].

        Notes:
        ------
        None.
        """

        if List is None:
            return -1

        try:

            __temp__ = self.Read(Filename=Filename)

            for __index__ in range(len(__temp__)):

                # Proceed when the number of parameters between the List and __temp__[__index__] are the same
                if len(List[0]) == len(__temp__[__index__][0]):

                    __parameter_value_duplicate__ = 0

                    # Go through each parameter
                    for __i__ in range(len(__temp__[__index__][0])):

                        if __temp__[__index__][0][__i__] == List[0][__i__]:
                            __parameter_value_duplicate__ += 1

                    # If a duplicate has been found, return the duplicate list that contains the parameters
                    # and simulation results
                    if __parameter_value_duplicate__ == len(List[0]):
                        return __temp__[__index__]

            return False

        # Should an error occur that was unexpected
        except Exception as __error__:
            if self.__debugging__:
                print(f'<Filing: Duplicate: {__error__}>')

        return -1
