# The initialization module for the package AntennaDesign, which will be a list of common public libraries,
# see AntennaDesign.__init__ for more information
from AntennaDesign.__init__ import *


class FineModel:
    """
    Description:
    ------------
    Simulates the antenna model defined in the ModelGeometry class within the antennaModel.py file.

    Attributes:
    -----------
    __cst__:                       COM object
                                   Creates a new session with CST studio suite software by opening it. This object
                                   will be able to do basic commands to the software such as opening a project.
    __mws__:                       COM object
                                   Controls the current project opened, where modeling, port creation, and simulations
                                   can be executed.
    __debugging__:                 bool
                                   For debugging purposes (developer mode).

    Methods:
    --------
    __init__(Debugging=False):
                                   The constructor of the class, where the attributes __cst__ and __mws__ are
                                   both initialized as None type, and expects an argument for debugging (optional).
    Initialize(FrequencyRangeMin, FrequencyRangeMax, DimensionUnits='mm', TemperatureUnits='Kelvin', FrequencyUnits='GHz', TimeUnits='ns', VoltageUnits='V', CurrentUnits='A', ResistanceUnits='Ohm', ConductanceUnits='Siemens', CapacitanceUnits='PikoF', InductanceUnits='nanoH'):
                                   Opens a session with the CST software. The default project that is opened is the
                                   'Python_Control.cst' project. Also, the method expects two arguments, specifically
                                   the minimum frequency and maximum frequency.
    TimeDomainSolver(SteadyStateLimit=-40):
                                   Initiates a simulation using the time domain solver within the 'Python_Control.cst'
                                   project.
    ConstructAntenna(Model=None):
                                   Constructs the antenna model through the CST software given the model as an argument.
    ConstructWaveguidePort(PortNumber=None, Orientation=None, ExcitationDirection=None, XRange=None, YRange=None, ZRange=None):
                                   Constructs the waveguide port through the CST software given the arguments.
    _get_results():
                                   Retrieves the simulation results, specifically the return loss and gain
                                   responses for this current build.
    _remove_all(__component__=None):
                                   Deletes all the components in the 'Python_Control.cst' project in order for a new
                                   antenna model to be constructed and simulated.

    Notes:
    ------
    None.
    """

    def __init__(self, Debugging=False):
        """
        Description:
        ------------
        The constructor of the ModelGeometry class. Optionally, it expects one parameter as an argument, specifically
        the Debugging, as a bool type.

        Parameters:
        -----------
        Debugging:                  bool
                                    For debugging purposes (developer mode).

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        # COM object(s)
        self.__cst__ = None
        self.__mws__ = None

        # Debugging (developer mode)
        self.__debugging__ = Debugging

    def Initialize(self, FrequencyRangeMin, FrequencyRangeMax, DimensionUnits='mm',
                   TemperatureUnits='Kelvin', FrequencyUnits='GHz', TimeUnits='ns',
                   VoltageUnits='V', CurrentUnits='A', ResistanceUnits='Ohm',
                   ConductanceUnits='Siemens', CapacitanceUnits='PikoF', InductanceUnits='nanoH'):
        """
        Description:
        ------------
        Opens a session with the CST software, then opens the 'Python_Control.cst' project. Finally, the frequency
        range is set for the project. Note that the method expects two arguments, specifically the minimum frequency
        and maximum frequency, both of type float. Optionally, the units of the project may also be changed if the
        user wishes so.

        Parameters:
        -----------
        FrequencyRangeMin:          float
                                    The minimum frequency value for the project to conduct simulations.
        FrequencyRangeMax:          float
                                    The maximum frequency value for the project to conduct simulations.
        DimensionUnits:             str
                                    The dimensional units that the project will be used in. The following units are
                                    possible: 'm' - meters; 'cm' - centimeters; 'mm' - millimeters; 'um' - micrometers;
                                    'nm' - nanometers; 'ft' - feet; 'mil' - thousands of an inch; 'in' - inches.
        TemperatureUnits:           str
                                    The temperature units that the project will be used in. The following units are
                                    possible: 'Celsius'; 'Kelvin'; 'Fahrenheit'.
        FrequencyUnits:             str
                                    The frequency units that the project will be used in. The following units are
                                    possible: 'Hz'; 'kHz'; 'MHz'; 'GHz'; 'THz'; 'PHz'.
        TimeUnits:                  str
                                    The time units that the project will be used in. The following units are
                                    possible: 'fs' - femto seconds; 'ps' - picoseconds; 'ns' - nanoseconds;
                                    'us' - microseconds; 'ms' - milliseconds; 's' - seconds.
        VoltageUnits:               str
                                    The voltage units that the project will be used in. The following units are
                                    possible: 'V' - volts.
        CurrentUnits:               str
                                    The current units that the project will be used in. The following units are
                                    possible: 'A' - amps.
        ResistanceUnits:            str
                                    The resistance units that the project will be used in. The following units are
                                    possible: 'Ohm' - ohms.
        ConductanceUnits:           str
                                    The conductance units that the project will be used in. The following units are
                                    possible: 'S' - siemens.
        CapacitanceUnits:           str
                                    The capacitance units that the project will be used in. The following units are
                                    possible: 'F' - farads.
        InductanceUnits:            str
                                    The inductance units that the project will be used in. The following units are
                                    possible: 'H' - henry.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        # Open the CST Studio Suite software
        self.__cst__ = pycst.connect()
        # Sleep for 6 seconds in order for the CST program to completely open
        time.sleep(6)
        if self.__debugging__:
            print('<simulator: FineModel: Initialize: 1. CST Studio Suite opened>')

        # Disable interactive mode, which enables scripting mode
        pycst.SetQuietMode(cst=self.__cst__)
        # Sleep for 6 seconds
        time.sleep(6)
        if self.__debugging__:
            print('<simulator: FineModel: Initialize: 2. Script mode initiated>')

        # Open the 'Python_Control.cst' CST Studio Suite project.
        pycst.open_project(cst=self.__cst__, path=str(pkg_resources.files('AntennaDesign') /
                                                      'Python_Control\\Python_Control.cst'))
        # Sleep for 6 seconds
        time.sleep(6)
        if self.__debugging__:
            print('<simulator: FineModel: Initialize: 3. Project opened>')

        # Get the active 3D window
        self.__mws__ = pycst.get_active_3d(cst=self.__cst__)
        # Sleep for 6 seconds
        time.sleep(6)
        if self.__debugging__:
            print('<simulator: FineModel: Initialize: 4. Current project assigned>')

        # Set the simulation frequency range
        pycst.frequency_range(mws=self.__mws__, frange1=FrequencyRangeMin, frange2=FrequencyRangeMax)
        # Sleep for 6 seconds
        time.sleep(6)
        if self.__debugging__:
            print(f'<simulator: FineModel: Initialize: 5. Frequency range assigned, f_min = {FrequencyRangeMin}, '
                  f'f_max = {FrequencyRangeMax}>')

        # Set CST Studio Suite units
        pycst.set_units(mws=self.__mws__, dimension=DimensionUnits, frequency=FrequencyUnits,
                        temperature=TemperatureUnits, time=TimeUnits,
                        voltage=VoltageUnits, current=CurrentUnits,
                        resistance=ResistanceUnits, conductance=ConductanceUnits,
                        capacitance=CapacitanceUnits, inductance=InductanceUnits)
        # Sleep for 6 seconds
        time.sleep(6)
        if self.__debugging__:
            print('<simulator: FineModel: Initialize: 6. Units set>')

    def TimeDomainSolver(self, SteadyStateLimit=-40):
        """
        Description:
        ------------
        Executes a simulation given that the antenna model and waveguide port has already been constructed. Note that
        only the time domain solver is used for this current build.

        Parameters:
        -----------
        SteadyStateLimit:           int
                                    The steady state, in dB, of the signal after a successful pulse.

        Returns:
        --------
        Returns both the return loss and gain responses in the form of [[f_range, return loss], [f_range, gain]].

        Notes:
        ------
        None.
        """

        # Simulate the design
        pycst.time_domain_solver(mws=self.__mws__, steadyStateLimit=SteadyStateLimit)

        # Call the _get_results() private method to return the return loss and gain responses
        return self._get_results()

    def ConstructAntenna(self, Model=None):
        """
        Description:
        ------------
        Constructs the antenna model by first removing the old design, including the waveguide port.

        Parameters:
        -----------
        Model:                      list
                                    The complete model of the antenna, excluding the waveguide port. This includes
                                    the actual geometry of the antenna, as well as geometry of the connector (optional).

        Returns:
        --------
        None.

        Notes:
        ------
        The connector is optional, but will be seen as part of the antenna geometry.
        """

        if Model is None:
            raise Exception('<FineModel.ConstructAntenna: Model is of None type>')

        # Remove all components to begin with a new model
        self._remove_all(__component__=Model)

        # Construct layers/sequences
        # Each layer/sequence will be an array where each element is defined as:
        #   index           Element description
        #     0             str, material name
        #     1             str, component/solid name
        #     2             str, type (brick, cylinder)
        #     3             str, operation type
        #     4             list, height range --> [zmin, zmax]
        #     5             list, Model component blocks:
        #     "brick"    --> [x_min, x_max, y_min, y_max],
        #     "cylinder" --> [orientation, inner radius, outer radius, Xcenter, Ycenter, Zcenter, Xrange, Yrange,
        #                                                                                       Zrange, segments]

        __components__ = {'name': [], 'index': [], 'material': []}

        # Layers/sequences
        for __i__ in Model:

            # Create a new material if it has not been seen before
            if not __components__['material'].__contains__(__i__[0]):
                __components__['material'].append(__i__[0])
                pycst.load_material(mws=self.__mws__, name=__i__[0])

            # Check if the component name has already been used. Add the component name, along
            # with a 0 index number if seen for the first time
            if not __components__['name'].__contains__(__i__[1]):
                __components__['name'].append(__i__[1])
                __components__['index'].append(0)

            # Assign the latest index number for the layer/sequence
            __current_index__ = __components__['name'].index(__i__[1])

            # For a brick layer/sequence
            if __i__[2] == 'brick':

                # Geometry components
                for __j__ in __i__[-1]:

                    # Create the brick shape
                    pycst.brick(mws=self.__mws__,
                                material=__i__[0],
                                component=__i__[1],
                                name=f'{__i__[1]}_{__components__["index"][__current_index__]}',
                                xrange=[__j__[0], __j__[1]],
                                yrange=[__j__[2], __j__[3]],
                                zrange=__i__[4])

                    # For 'add' type
                    if __i__[3] == 'add' and __components__['index'][__current_index__] > 0:
                        pycst.add(mws=self.__mws__,
                                  component1=__i__[1],
                                  solid1=f'{__i__[1]}_0',
                                  component2=__i__[1],
                                  solid2=f'{__i__[1]}_{__components__["index"][__current_index__]}')

                    # For 'subtract' type
                    elif __i__[3] == 'subtract' and __components__['index'][__current_index__] > 0:
                        pycst.subtract(mws=self.__mws__,
                                       component1=__i__[1],
                                       solid1=f'{__i__[1]}_0',
                                       component2=__i__[1],
                                       solid2=f'{__i__[1]}_{__components__["index"][__current_index__]}')

                    # For 'None' type
                    else:
                        pass

                    # Increment the index in the __component__ dictionary that is correlated
                    # with the current component name
                    __components__['index'][__current_index__] += 1

            # For a cylinder layer/sequence
            elif __i__[2] == 'cylinder':

                # Geometry components
                for __j__ in __i__[-1]:

                    # Create the cylinder shape
                    pycst.cylinder(mws=self.__mws__,
                                   material=__i__[0],
                                   component=__i__[1],
                                   name=f'{__i__[1]}_{__components__["index"][__current_index__]}',
                                   orientation=__j__[0],
                                   innerRadius=__j__[1],
                                   outerRadius=__j__[2],
                                   Xcenter=__j__[3],
                                   Ycenter=__j__[4],
                                   Zcenter=__j__[5],
                                   Xrange=__j__[6],
                                   Yrange=__j__[7],
                                   Zrange=__j__[8],
                                   segments=__j__[9])

                    # For 'add' type
                    if __i__[3] == 'add' and __components__['index'][__current_index__] > 0:
                        pycst.add(mws=self.__mws__,
                                  component1=__i__[1],
                                  solid1=f'{__i__[1]}_0',
                                  component2=__i__[1],
                                  solid2=f'{__i__[1]}_{__components__["index"][__current_index__]}')

                    # For 'subtract' type
                    elif __i__[3] == 'subtract' and __components__['index'][__current_index__] > 0:
                        pycst.subtract(mws=self.__mws__,
                                       component1=__i__[1],
                                       solid1=f'{__i__[1]}_0',
                                       component2=__i__[1],
                                       solid2=f'{__i__[1]}_{__components__["index"][__current_index__]}')

                    # For 'None' type
                    else:
                        pass

                    # Increment the index in the __component__ dictionary that is correlated
                    # with the current component name
                    __components__['index'][__current_index__] += 1

            else:
                raise Exception('<FineModel: ConstructAntenna: The given type is not brick or cylinder>')

    def ConstructWaveguidePort(self, PortNumber=None, Orientation=None, ExcitationDirection=None, XRange=None,
                               YRange=None, ZRange=None):
        """
        Description:
        ------------
        Constructs the waveguide port before simulation takes place.

        Parameters:
        -----------
        PortNumber:                 int
                                    The number of the waveguide port being constructed (it must be unique).
        Orientation:                str
                                    The orientation of the waveguide port normal to either the x-axis, y-axis, or
                                    z-axis.
        ExcitationDirection:        str
                                    The direction of the signal, where the following are possible:
                                    'Positive', 'Negative'.
        XRange:                     list
                                    A list with two float type elements, specifically the minimum and maximum values.
                                    The minimum and maximum x values that will be used for the waveguide port.
        YRange:                     list
                                    A list with two float type elements, specifically the minimum and maximum values.
                                    The minimum and maximum y values that will be used for the waveguide port.
        ZRange:                     list
                                    A list with two float type elements, specifically the minimum and maximum values.
                                    The minimum and maximum z values that will be used for the waveguide port.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        # Delete the old waveguide port
        pycst.delete_waveguide_port(mws=self.__mws__, port_number=PortNumber)

        # Construct the new waveguide port
        pycst.waveguide_port(mws=self.__mws__,
                             portNumber=PortNumber,
                             normal=Orientation,
                             orientation=ExcitationDirection,
                             xrange=XRange,
                             yrange=YRange,
                             zrange=ZRange)

    def _get_results(self):
        """
        Description:
        ------------
        Retrieves the simulations results from the 'Python_Control.cst' project. Note that only the return loss and
        gain responses are extracted for this current build.

        Parameters:
        -----------
        None.

        Returns:
        --------
        Returns the return loss and gain responses from the latest simulation.

        Notes:
        ------
        None.
        """

        __s11_result_vector__ = []
        __gain_result_vector__ = []

        try:
            # Retrieve the S11 results from the simulation
            __s11_result_vector__ = pycst.result_parameters(mws=self.__mws__)

        except Exception as __error__:
            if self.__debugging__:
                print(__error__)
                raise Exception('<FineModel: _get_results: Failed to retrieve return loss response>')

        try:
            # Retrieve the gain results from the simulation
            __gain_result_vector__ = pycst.result_parameters(mws=self.__mws__, parent_path=r'Tables\1D Results')

        except Exception as __error__:
            if self.__debugging__:
                print(__error__)
                raise Exception('<FineModel: _get_results: Failed to retrieve gain response>')

        return [[__s11_result_vector__[0], __s11_result_vector__[2]],
                [__gain_result_vector__[0], __gain_result_vector__[1]]]

    def _remove_all(self, __component__=None):
        """
        Description:
        ------------
        Deletes all the components of the current antenna model.

        Parameters:
        -----------
        __component__:              list
                                    The model of the antenna, where only the 'name' component, the second index of
                                    layer/sequence n, is used to delete the components of the current antenna model.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        if self.__mws__ is not None and __component__ is not None:

            for __i__ in __component__:
                pycst.delete_component(mws=self.__mws__, component=__i__[1])
