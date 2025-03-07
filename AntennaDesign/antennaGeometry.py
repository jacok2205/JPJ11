# The initialization module for the package AntennaDesign, which will be a list of common public libraries,
# see AntennaDesign.__init__ for more information
from AntennaDesign.__init__ import *


class ModelGeometry:
    """
    Description:
    ------------
    Stores all the building blocks for the antenna geometry, the waveguide port, and the SMA connector (being part
    of the antenna geometry).

    Attributes:
    -----------
    __parameter__:                  dict
                                    A dictionary that keeps all parameters for algorithms to explore with. The format
                                    of the dictionary is: [name, range]. name is the name of the parameter; range is
                                    a positive float value range for the parameter to be.
    __model__:                      dict
                                    A dictionary that keeps all the layers of the antenna model. The format of the
                                    dictionary is: [material, name, type, operation, z-range, geometry components].
                                    material is the name of the material used; the name is the name for the component;
                                    type is either None, brick, or cylinder; operation is either None, add, or subtract;
                                    z-range is the height of the geometry; geometry components describe the geometry
                                    of the nth layer/sequence.
    __waveguide_port__:             list
                                    A list that contains the position and dimensions of the waveguide port. The format
                                    of the list is: [port number, orientation, excitation direction, xrange,
                                    yrange, zrange]. port number is the number of the waveguide port; orientation is
                                    the plane of the waveguide port normal to the x, y, or z axis; excitation direction
                                    can either be positive or negative; xrange is the position/dimension of the port
                                    in the x direction; yrange is the position/dimension of the port in the y direction;
                                    zrange is the position/dimension of the port in the z direction.
    __simulator__:                  Simulator
                                    An instance of the Simulator class within the AntennaDesign package, see
                                    simulator.py for more information.
    __parameter_step_size__:        float
                                    The size a parameter is allowed to step.
    __objective__:                  list
                                    The objectives of the antenna model, which has the format: [[band1, tolerance1],
                                    [band2, tolerance2], ..., [band_n, tolerance_n]].
    __explore_space__:              list
                                    A list that contains the boundaries of a geometry component that contains at least
                                    one parameter. The format is: [[x_min1, x_max1, y_min1, y_max1, z_min1, z_max1],
                                    ..., [x_min_n, x_max_n, y_min_n, y_max_n, z_min_n, z_max_n]].
    __debugging__:                  bool
                                    For debugging purposes (developer mode).

    Methods:
    --------
    __init__(ParameterStepSize, Objectives=None, Simulator=None, ExploreSpace=None, FrequencyRangeMin=1,
                FrequencyRangeMax=7, Debugging=False):
                                    The constructor of the class, where the ParameterStepSize and ExploreSpace
                                    parameters are required from the user. It also initializes the CST program
                                    by opening the project called 'Python_Control.cst' and awaits further instructions.
    SetObjectives(Objectives=None):
                                    Only used from the user if he/she either forgot to include the objectives in the
                                    constructor or the user wishes to add the objectives after the constructor.
    AddParameter(Name=None, Range=None):
                                    Adds a parameter to the model.
    AddSequence(Material=None, ComponentName=None, Type=None, Operation=None, Z=None, Geometry=None):
                                    Adds a layer/sequence to the model.
    SetWaveguidePort(PortNumber=None, XRange=None, YRange=None, ZRange=None):
                                    Sets a single waveguide port to the model. Note that this is required for a
                                    successful simulation to occur.
    SimulateModel(Parameters=None, Rounding=None):
                                    Simulates the model through the Simulator instance and returns the simulation
                                    results.
    GenerateRandomParameterValue(Parameters=None, ParameterIndex=None, Rounding=None):
                                    Initializes a new set of parameter values given their ranges and returns them, or
                                    returns a new random value within the indexed parameter.
    IncrementParameterValue(Parameters=None, Index=None, Rounding=None):
                                    Increments the indexed parameter value if and only if the increment results for
                                    the parameter to be within its defined range. Note that the increment is the size
                                    of the defined parameter step size.
    DecrementParameterValue(Parameters=None, Index=None, Rounding=None):
                                    Decrements the indexed parameter value if and only if the decrement results for
                                    the parameter to be within its defined range. Note that the increment is the size
                                    of the defined parameter step size.
    CheckBoundary(Parameters, Rounding=None):
                                    Checks whether a geometry component, that contains at least one parameter, is within
                                    the defined explore space.

    Notes:
    ------
    None.
    """

    def __init__(self, ParameterStepSize=None, Objectives=None, Simulator=None, ExploreSpace=None,
                 FrequencyRangeMin=1, FrequencyRangeMax=7, Debugging=False):
        """
        Description:
        ------------
        The constructor of the ModelGeometry class. It expects two parameters as arguments, specifically the
        ParameterStepSize, as a float type, and a Simulator, an instance of Simulator.

        Parameters:
        -----------
        ParameterStepSize:          list
                                    The size of the parameter is allowed.
        Objectives:                 list
                                    Each element is a frequency range (along with a band edge tolerance). The format
                                    is: [[f1_min, f1_max, tolerance1], [f2_min, f2_max, tolerance2], ..., [fn_min,
                                    fn_max, tolerance_n]].
        Simulator:                  Simulator
                                    A simulator instance that is used for simulating the geometry of the antenna model.
        ExploreSpace:               list
                                    Each element is a set of boundary's, and has the following format: [[x1_min, x1_max,
                                    y1_min, y1_max, z1_min, z2_max], ..., [xn_min, xn_max, yn_min, yn_max, zn_min,
                                    zn_max]].
        FrequencyRangeMin:          float
                                    The minimum frequency that the simulator uses for simulation results.
        FrequencyRangeMax:          float
                                    The maximum frequency that the simulator uses for simulation results.
        Debugging:                  bool
                                    For debugging purposes (developer mode).

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        if Simulator is None or ExploreSpace is None:
            raise Exception('<ModelGeometry: __init__: A simulator and an explore space are required to proceed>')
        if ParameterStepSize is None:
            raise Exception('<ModelGeometry: __init__: The parameter step size must be set to some positive '
                            'float value>')

        self.__parameter__ = {'name': [], 'range': []}
        self.__model__ = {'material': [], 'name': [], 'type': [], 'operation': [], 'z': [], 'geometry': []}
        self.__waveguide_port__ = None
        self.__simulator__ = Simulator

        self.__parameter_step_size__ = ParameterStepSize
        self.__objective__ = Objectives
        self.__debugging__ = Debugging
        self.__explore_space__ = ExploreSpace

        # Initialize the simulator by connecting to the CST program and opening the project 'Python_Control.cst'
        self.__simulator__.Initialize(FrequencyRangeMin, FrequencyRangeMax, DimensionUnits='mm',
                                      TemperatureUnits='Kelvin', FrequencyUnits='GHz', TimeUnits='ns',
                                      VoltageUnits='V', CurrentUnits='A', ResistanceUnits='Ohm',
                                      ConductanceUnits='Siemens', CapacitanceUnits='PikoF', InductanceUnits='nanoH')

    def SetObjectives(self, Objectives=None):
        """
        Description:
        ------------
        Used when the user wishes to set the objectives after creating an instance of this class. Note again that
        the format of the objectives is: [[f1_min, f1_max, tolerance1], ..., [fn_min, fn_max, tolerance_n]]. Each
        frequency range is of type float and the tolerance is a float that is less than 1. For example, 0.023 represents
        2.3 % for band edge tolerances. If more than one list is in the objectives parameter, it means that more than
        one band is desired.

        Parameters:
        -----------
        Objectives:                 list
                                    A list of lists, where each element is a list that contains the minimum frequency,
                                    maximum frequency, and band edge tolerance per band.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        if Objectives is None:
            raise Exception('<ModelGeometry: SetObjectives: Objectives is of None type>')

        self.__objective__ = Objectives

    def AddParameter(self, Name=None, Range=None):
        """
        Description:
        ------------
        Adds a parameter to the model of the antenna that can be manipulated given its range.

        Parameters:
        -----------
        Name:                       str
                                    The name of the parameter.
        Range:                      list
                                    A list that contains two elements of type float, where the first element must
                                    be the minimum value and the second/last element must be the maximum value.

        Returns:
        --------
        None.

        Notes:
        ------
        The name is must match to the model of the antenna, otherwise a crash is inevitable.
        """

        if Name is None or Range is None:
            raise Exception('<ModelGeometry: AddParameter: One or more parameters are of None type>')

        self.__parameter__['name'].append(copy.deepcopy(Name))
        self.__parameter__['range'].append(copy.deepcopy(Range))

    def AddSequence(self, Material=None, ComponentName=None, Type=None, Operation=None, Z=None, Geometry=None):
        """
        Description:
        ------------
        Adds a layer/sequence to the model of the antenna. Note that the first call to this function will be executed
        first and the last call to this function will be executed last. Thus, it is imperative that the user plans
        the design of the model first before attempting.

        Parameters:
        -----------
        Material:                   str
                                    The material name used for the layer/sequence. Note that the material must match
                                    the CST material name exactly.
        ComponentName:              str
                                    The name of the layer defined by the user.
        Type:                       str
                                    The type of shape for the layer/sequence. Only two types are possible with this
                                    build, specifically the 'brick' and 'cylinder' shapes. The brick shape expects
                                    the material, name, xrange, yrange, and zrange values. The cylinder shape expects
                                    the material name, the orientation (normal to either the x-axis, y-axis, or z-axis),
                                    outer radius, inner radius, the x center, the y center, the z center, and the
                                    number of segments.
        Operation:                  str
                                    The operation for the layer/sequence. Three types are possible with this build,
                                    either an 'add', 'subtract', or 'None'.
        Z:                          list
                                    A list that contains only two float type elements. This is used for the height of
                                    the layer/sequence.
        Geometry:                   list
                                    A list of lists that contain the geometry components of the layer/sequence.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        if Material is None or ComponentName is None or Type is None or Operation is None or Z is None or \
                Geometry is None:
            raise Exception('<ModelGeometry: AddSequence: One or more parameters are of None type>')

        self.__model__['material'].append(copy.deepcopy(Material))
        self.__model__['name'].append(copy.deepcopy(ComponentName))
        self.__model__['type'].append(copy.deepcopy(Type))
        self.__model__['operation'].append(copy.deepcopy(Operation))
        self.__model__['z'].append(copy.deepcopy(Z))
        self.__model__['geometry'].append(copy.deepcopy(Geometry))

    def SetWaveguidePort(self, PortNumber=None, Orientation=None, ExcitationDirection=None, XRange=None,
                         YRange=None, ZRange=None):
        """
        Description:
        ------------
        Initializes the position and dimensions of the waveguide port.

        Parameters:
        -----------
        PortNumber:                 str
                                    The number of the waveguide port.
        Orientation:                str
                                    The orientation of the waveguide port normal to either the x-axis, y-axis, or
                                    z-axis.
        ExcitationDirection:        str
                                    Describes the direction of excitation, either 'Positive' or 'Negative'.
        XRange:                     list
                                    A list that contains two elements, specifically the minimum x value and the
                                    maximum x value.
        YRange:                     list
                                    A list that contains two elements, specifically the minimum y value and the
                                    maximum y value.
        ZRange:                     list
                                    A list that contains two elements, specifically the minimum z value and the
                                    maximum z value.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        if PortNumber is None or Orientation is None or ExcitationDirection is None or XRange is None or \
                YRange is None or ZRange is None:

            self.__waveguide_port__ = None
            raise Exception('<ModelGeometry: SetWaveguidePort: One or more parameters is of None type>')

        self.__waveguide_port__ = [PortNumber, Orientation, ExcitationDirection, XRange, YRange, ZRange]

    def SimulateModel(self, Parameters=None, Rounding=None):
        """
        Description:
        ------------
        Once the antenna model and waveguide port have been correctly defined, the model is simulated on the
        'Python_Control.cst' project through the CST simulator.

        Parameters:
        -----------
        Parameters:                 list
                                    A list of parameters, where each element is of type float.
        Rounding:                   int
                                    The rounding for the float value(s) of the Parameter(s)
                                    (attribute self.__parameter__).

        Returns:
        --------
        The simulation results, in this current build, only the return loss response and gain response lists are
        returned.

        Notes:
        ------
        This function is used from an automation process defined by the user. The default process is ga.py.
        """

        if Parameters is None:
            raise Exception('<ModelGeometry: SimulateModel: Parameters is of None type>')
        if self.__waveguide_port__ is None:
            raise Exception('<ModelGeometry: SimulateModel: Waveguide port has not been defined by user>')
        if Rounding is None:
            raise Exception('<ModelGeometry: SimulateModel: Rounding is of None type. '
                            'Please specify a rounding number>')

        # Create a temporary model that will contain only float values for the defined parameters
        __model__ = []
        for __i__ in range(len(self.__model__['material'])):

            # Append the current layer/sequence
            __model__.append([copy.deepcopy(self.__model__['material'][__i__]),
                              copy.deepcopy(self.__model__['name'][__i__]),
                              copy.deepcopy(self.__model__['type'][__i__]),
                              copy.deepcopy(self.__model__['operation'][__i__]),
                              copy.deepcopy(self.__model__['z'][__i__]),
                              copy.deepcopy(self.__model__['geometry'][__i__])])

            for __j__ in range(len(self.__model__['geometry'][__i__])):

                for __k__ in range(len(self.__parameter__['name'])):

                    # Replace any parameter with a string float value
                    if __model__[-1][2] == 'brick' and isinstance(__model__[-1][-1][__j__][0], str):
                        __model__[-1][-1][__j__][0] = __model__[-1][-1][__j__][0].replace(
                            self.__parameter__['name'][__k__], str(Parameters[__k__]))
                    if __model__[-1][2] == 'brick' and isinstance(__model__[-1][-1][__j__][1], str):
                        __model__[-1][-1][__j__][1] = __model__[-1][-1][__j__][1].replace(
                            self.__parameter__['name'][__k__], str(Parameters[__k__]))
                    if __model__[-1][2] == 'brick' and isinstance(__model__[-1][-1][__j__][2], str):
                        __model__[-1][-1][__j__][2] = __model__[-1][-1][__j__][2].replace(
                            self.__parameter__['name'][__k__], str(Parameters[__k__]))
                    if __model__[-1][2] == 'brick' and isinstance(__model__[-1][-1][__j__][3], str):
                        __model__[-1][-1][__j__][3] = __model__[-1][-1][__j__][3].replace(
                            self.__parameter__['name'][__k__], str(Parameters[__k__]))

                # Evaluate the geometry component if it is required
                if __model__[-1][2] == 'brick' and isinstance(__model__[-1][-1][__j__][0], str):
                    __model__[-1][-1][__j__][0] = round(eval(__model__[-1][-1][__j__][0]), Rounding)
                if __model__[-1][2] == 'brick' and isinstance(__model__[-1][-1][__j__][1], str):
                    __model__[-1][-1][__j__][1] = round(eval(__model__[-1][-1][__j__][1]), Rounding)
                if __model__[-1][2] == 'brick' and isinstance(__model__[-1][-1][__j__][2], str):
                    __model__[-1][-1][__j__][2] = round(eval(__model__[-1][-1][__j__][2]), Rounding)
                if __model__[-1][2] == 'brick' and isinstance(__model__[-1][-1][__j__][3], str):
                    __model__[-1][-1][__j__][3] = round(eval(__model__[-1][-1][__j__][3]), Rounding)

        # Construct the antenna and waveguide port
        self.__simulator__.ConstructAntenna(Model=__model__)
        self.__simulator__.ConstructWaveguidePort(PortNumber=self.__waveguide_port__[0],
                                                  Orientation=self.__waveguide_port__[1],
                                                  ExcitationDirection=self.__waveguide_port__[2],
                                                  XRange=self.__waveguide_port__[3],
                                                  YRange=self.__waveguide_port__[4],
                                                  ZRange=self.__waveguide_port__[5])

        # Simulate and return the results
        return self.__simulator__.TimeDomainSolver(SteadyStateLimit=-40)

    def GenerateRandomParameterValue(self, Parameters=None, ParameterIndex=None, Rounding=None):
        """
        Description:
        ------------
        Generates a random value of step size self.__parameter_step_size__ (defined by the user). Either a full
        list of parameters is returned, if ParameterIndex is of None type, or a single random value is returned if
        ParameterIndex is not of None type. Note that the value is within the defined range of the parameter that was
        defined by the user.

        Parameters:
        -----------
        Parameters:                 list
                                    A list of float elements that represent the parameters defined by the user.
        ParameterIndex:             int
                                    The index of the parameter to generate a random value from.
        Rounding:                   int
                                    The rounding for the float value(s) of the Parameter(s)
                                    (attribute self.__parameter__).

        Returns:
        --------
        Returns either a list of float values (if ParameterIndex is of None type), or a single random float value (if
        ParameterIndex is not of None type).

        Notes:
        ------
        None.
        """

        if Rounding is None:
            raise Exception('<ModelGeometry: GenerateRandomParameterValue: Rounding is of None type. '
                            'Please specify a rounding number>')

        __tries__ = 100

        # If a full set of random values are required (usually used for initialization)
        if ParameterIndex is None:
            while __tries__ > 0:
                try:
                    __parameter__ = []

                    # Generate random parameter value list
                    for __i__ in self.__parameter__['range']:
                        __parameter__.append(
                            round(random.choice(np.arange(__i__[0],
                                                          __i__[1] + self.__parameter_step_size__,
                                                          self.__parameter_step_size__)), Rounding)
                        )

                    # Check if the boundary is met
                    self.CheckBoundary(Parameters=__parameter__, Rounding=Rounding)

                    return __parameter__

                except Exception as __error__:
                    if self.__debugging__:
                        print(f'<ModelGeometry: GenerateRandomParameterValue: {__error__}>')
                    __tries__ -= 1

                if __tries__ == 0:
                    raise Exception('<ModelGeometry: GenerateRandomParameterValue: The maximum number of tries to '
                                    'generate random parameter values have been exceeded, check defined antenna model>')

        # If a single parameter random float value is required
        else:
            if Parameters is None:
                raise Exception('<ModelGeometry: GenerateRandomParameterValue: Parameters is of type None, which '
                                'is not allowed when a random value is generated for a single parameter>')

            while __tries__ > 0:
                try:
                    # Generate a random parameter value
                    __parameter__ = round(random.choice(np.arange(
                        self.__parameter__['range'][ParameterIndex][0],
                        self.__parameter__['range'][ParameterIndex][1] + self.__parameter_step_size__,
                        self.__parameter_step_size__)
                    ), Rounding)

                    # Set a temporary parameter list
                    __temp__ = [__i__ for __i__ in Parameters]
                    # Replace the parameter index with the randomly generated parameter value
                    __temp__[ParameterIndex] = __parameter__

                    # Check if the boundary is met
                    self.CheckBoundary(Parameters=__temp__, Rounding=Rounding)

                    return __parameter__

                except Exception as __error__:
                    if self.__debugging__:
                        print(f'<ModelGeometry: GenerateRandomParameterValue: {__error__}>')
                    __tries__ -= 1

                if __tries__ == 0:
                    raise Exception('<ModelGeometry: GenerateRandomParameterValue: The maximum number of tries to '
                                    'generate a random parameter value has been exceeded, check defined antenna model>')

    def IncrementParameterValue(self, Parameters=None, Index=None, Rounding=None):
        """
        Description:
        ------------
        Increments the parameter given the index. An increment of self.__parameter_step_size__ is only applied if and
        only if the result is within the parameter's defined range.

        Parameters:
        -----------
        Parameters:                 list
                                    A list of float values that corresponds to the parameters defined by the user.
        Index:                      int
                                    The index of the parameter Parameters to increment.
        Rounding:                   int
                                    The rounding for the float value of the Parameter given the Index parameter.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        if Rounding is None:
            raise Exception('<ModelGeometry: IncrementParameterValue: Rounding is of type None. '
                            'Please specify a rounding number>')

        # Increment the parameter if not out of its defined range
        if Parameters[Index] + self.__parameter_step_size__ <= self.__parameter__['range'][Index][1]:
            Parameters[Index] = round(Parameters[Index] + self.__parameter_step_size__, Rounding)

            # Horizontal to see if it is within its range
            try:
                self.CheckBoundary(Parameters=Parameters, Rounding=Rounding)

            # Decrement the parameter if it violates its range
            except Exception as __error__:
                if self.__debugging__:
                    print(f'<ModelGeometry: IncrementParameterValue: {__error__}>')

                Parameters[Index] = round(Parameters[Index] - self.__parameter_step_size__, Rounding)

    def DecrementParameterValue(self, Parameters=None, Index=None, Rounding=None):
        """
        Description:
        ------------
        Decrements the parameter given the index. A decrement of self.__parameter_step_size__ is only applied if and
        only if the result is within the parameter's defined range.

        Parameters:
        -----------
        Parameters:                 list
                                    A list of float values that corresponds to the parameters defined by the user.
        Index:                      int
                                    The index of the parameter Parameters to decrement.
        Rounding:                   int
                                    The rounding for the float value of the Parameter given the Index parameter.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        if Rounding is None:
            raise Exception('<ModelGeometry: DecrementParameterValue: Rounding is of None type. '
                            'Please specify a rounding number>')

        # Decrement the parameter if not out of its defined range
        if Parameters[Index] - self.__parameter_step_size__ >= self.__parameter__['range'][Index][0]:
            Parameters[Index] = round(Parameters[Index] - self.__parameter_step_size__, Rounding)

            # Horizontal to see if it is within its range
            try:
                self.CheckBoundary(Parameters=Parameters, Rounding=Rounding)

            # Increment the parameter if it violates its range
            except Exception as __error__:
                if self.__debugging__:
                    print(f'<ModelGeometry: DecrementParameterValue: {__error__}>')

                Parameters[Index] = round(Parameters[Index] + self.__parameter_step_size__, Rounding)

    def CheckBoundary(self, Parameters, Rounding=None):
        """
        Description:
        ------------
        Checks whether the given parameters violate the defined explore space lists.

        Parameters:
        -----------
        Parameters:                 list
                                    A list of float values that corresponds to the parameters defined by the user.
        Rounding:                   int
                                    The rounding for the float values of the Parameters parameter.

        Returns:
        --------
        Nothing is returned if the check was successful (all the parameters do not violate the explore space), else
        a raise is made with a message (if no handle is made, the program will simply crash with a message).

        Notes:
        ------
        None.
        """

        if Rounding is None:
            raise Exception('<ModelGeometry: CheckBoundary: Rounding is of type None. '
                            'Please specify a rounding number>')

        __geometry__ = []

        for __i__ in range(len(self.__model__['geometry'])):

            # Proceed if and only if the layer/sequence is a 'brick' type
            if self.__model__['type'][__i__] == 'brick':
                for __j__ in range(len(self.__model__['geometry'][__i__])):

                    # If any of the geometry component components are of str type, proceed for boundary checks
                    if (isinstance(self.__model__['geometry'][__i__][__j__][0], str) or
                            isinstance(self.__model__['geometry'][__i__][__j__][1], str) or
                            isinstance(self.__model__['geometry'][__i__][__j__][2], str) or
                            isinstance(self.__model__['geometry'][__i__][__j__][3], str)):

                        __temp__ = [self.__model__['geometry'][__i__][__j__][0],
                                    self.__model__['geometry'][__i__][__j__][1],
                                    self.__model__['geometry'][__i__][__j__][2],
                                    self.__model__['geometry'][__i__][__j__][3]]

                        # Replace any parameter names with Parameter[__k__] value
                        for __k__ in range(len(self.__parameter__['name'])):
                            if isinstance(__temp__[0], str):
                                __temp__[0] = __temp__[0].replace(self.__parameter__['name'][__k__],
                                                                  str(Parameters[__k__]))
                            if isinstance(__temp__[1], str):
                                __temp__[1] = __temp__[1].replace(self.__parameter__['name'][__k__],
                                                                  str(Parameters[__k__]))
                            if isinstance(__temp__[2], str):
                                __temp__[2] = __temp__[2].replace(self.__parameter__['name'][__k__],
                                                                  str(Parameters[__k__]))
                            if isinstance(__temp__[3], str):
                                __temp__[3] = __temp__[3].replace(self.__parameter__['name'][__k__],
                                                                  str(Parameters[__k__]))

                        # If the element within __temp__ is a string, evaluate it
                        if isinstance(__temp__[0], str):
                            __temp__[0] = eval(__temp__[0])
                        if isinstance(__temp__[1], str):
                            __temp__[1] = eval(__temp__[1])
                        if isinstance(__temp__[2], str):
                            __temp__[2] = eval(__temp__[2])
                        if isinstance(__temp__[3], str):
                            __temp__[3] = eval(__temp__[3])

                        # Round the geometry component values to Rounding decimals
                        __temp__[0] = round(__temp__[0], Rounding)
                        __temp__[1] = round(__temp__[1], Rounding)
                        __temp__[2] = round(__temp__[2], Rounding)
                        __temp__[3] = round(__temp__[3], Rounding)

                        # Compare the limits found from __temp__ with self.__explore_space__ variable
                        for __k__ in self.__explore_space__:

                            # Round the current explore space and z-range to Rounding decimals
                            __explore_space__ = [round(__l__, Rounding) for __l__ in __k__]
                            __z__ = [round(self.__model__['z'][__i__][0], Rounding),
                                     round(self.__model__['z'][__i__][1], Rounding)]

                            # If a z range match has been found, proceed
                            if __z__[0] == __explore_space__[4] and __z__[1] == __explore_space__[5]:
                                # If __temp__[0] is less than x minimum or __temp__[1] is greater than x maximum,
                                # or __temp__[2] is less than y minimum or __temp__[3] is greater than y maximum, raise
                                # an exception
                                if __temp__[0] < __explore_space__[0] or __temp__[1] > __explore_space__[1] or \
                                        __temp__[2] < __explore_space__[2] or __temp__[3] > __explore_space__[3]:
                                    raise Exception(f'<ModelGeometry: CheckBoundary: A geometry component with '
                                                    f'parameters, specifically {self.__model__["geometry"][__i__]}, '
                                                    f'is out of bounds for explore space {__explore_space__}>')
