from AntennaDesign.__init__ import *


class ModelGeometry:
    def __init__(self, ParameterStepSize, Objectives=None, Simulator=None, ExploreSpace=None,
                 FrequencyRangeMin=1, FrequencyRangeMax=7, Debugging=False):

        if Simulator is None or ExploreSpace is None:
            raise Exception('<ModelGeometry: __init__: A simulator and an explore space are required to proceed>')

        self.__parameter__ = {'name': [], 'range': []}
        self.__model__ = {'material': [], 'name': [], 'type': [], 'operation': [], 'z': [], 'geometry': []}

        # Format is [port number, xrange, yrange, zrange]
        self.__waveguide_port__ = None
        self.__parameter_step_size__ = ParameterStepSize
        self.__objective__ = Objectives
        self.__debugging__ = Debugging
        self.__simulator__ = Simulator
        self.__rounding__ = 9

        # [[z-range, [Xmin, Xmax, Ymin, Ymax]], [z-range, [Xmin, Xmax, Ymin, Ymax]], ..., [z-range, [Xmin, Xmax, Ymin, Ymax]]]
        # If the z-range element matches to the geometry component's z-range and a parameter exists, check if it is
        # within the explore space.
        self.__explore_space__ = ExploreSpace

        self.__simulator__.Initialize(FrequencyRangeMin, FrequencyRangeMax, DimensionUnits='mm',
                                      TemperatureUnits='Kelvin', FrequencyUnits='GHz', TimeUnits='ns',
                                      VoltageUnits='V', CurrentUnits='A', ResistanceUnits='Ohm',
                                      ConductanceUnits='Siemens', CapacitanceUnits='PikoF', InductanceUnits='nanoH')

    # The objective has the following standard format:
    # [[[f_min1, f_max1], [f_min2, f_max2], ..., [f_min_n, f_max_n]], [tolerance1, tolerance2, ..., tolerance_n]]
    def SetObjectives(self, Objectives=None):
        if Objectives is None:
            raise Exception('<ModelGeometry: SetObjectives: Argument is of None type>')
        self.__objective__ = Objectives

    # This function is used to store all parameters of the dynamic portion of the model
    def AddParameter(self, Name=None, Range=None):
        if Name is None or Range is None:
            raise Exception('<AntennaGeometry: AddParameter: One or more parameters are of None type>')
        self.__parameter__['name'].append(Name)
        self.__parameter__['range'].append(Range)

    # Type is either a brick or a cylinder
    def AddSequence(self, Material=None, ComponentName=None, Type=None, Operation=None, Z=None, Geometry=None):
        if Material is None or ComponentName is None or Type is None or Operation is None or Z is None or Geometry is None:
            raise Exception('<AntennaGeometry: AddSequence: One or more parameters are of None type>')
        self.__model__['material'].append(Material)
        self.__model__['name'].append(ComponentName)
        self.__model__['type'].append(Type)
        self.__model__['operation'].append(Operation)
        self.__model__['z'].append(Z)
        self.__model__['geometry'].append(Geometry)

    def SetWaveguidePort(self, PortNumber=None, XRange=None, YRange=None, ZRange=None):
        if PortNumber is None or XRange is None or YRange is None or ZRange is None:
            self.__waveguide_port__ = None
            raise Exception('<ModelGeometry: SetWaveguidePort: One or more parameters is of type None>')
        self.__waveguide_port__ = [PortNumber, XRange, YRange, ZRange]

    def SimulateModel(self, Parameters=None):
        if Parameters is None:
            raise Exception('<ModelGeometry: SimulateModel: Parameters is of None type>')
        if self.__waveguide_port__ is None:
            raise Exception('<ModelGeometry: SimulateModel: Waveguide port has not been set up>')

        __model__ = []
        for __i__ in range(len(self.__model__['material'])):

            __model__.append([self.__model__['material'][__i__],
                              self.__model__['name'][__i__],
                              self.__model__['type'][__i__],
                              self.__model__['operation'][__i__],
                              self.__model__['z'][__i__],
                              self.__model__['geometry'][__i__]])

            for __j__ in range(len(self.__model__['geometry'][__i__])):

                for __k__ in range(len(self.__parameter__['name'])):
                    if isinstance(__model__[-1][-1][__j__][0], str):
                        __model__[-1][-1][__j__][0] = __model__[-1][-1][__j__][0].replace(
                            self.__parameter__['name'][__k__], str(Parameters[__k__]))
                    if isinstance(__model__[-1][-1][__j__][1], str):
                        __model__[-1][-1][__j__][1] = __model__[-1][-1][__j__][1].replace(
                            self.__parameter__['name'][__k__], str(Parameters[__k__]))
                    if isinstance(__model__[-1][-1][__j__][2], str):
                        __model__[-1][-1][__j__][2] = __model__[-1][-1][__j__][2].replace(
                            self.__parameter__['name'][__k__], str(Parameters[__k__]))
                    if isinstance(__model__[-1][-1][__j__][3], str):
                        __model__[-1][-1][__j__][3] = __model__[-1][-1][__j__][3].replace(
                            self.__parameter__['name'][__k__], str(Parameters[__k__]))

                if isinstance(__model__[-1][-1][__j__][0], str):
                    __model__[-1][-1][__j__][0] = eval(__model__[-1][-1][__j__][0])
                if isinstance(__model__[-1][-1][__j__][1], str):
                    __model__[-1][-1][__j__][1] = eval(__model__[-1][-1][__j__][1])
                if isinstance(__model__[-1][-1][__j__][2], str):
                    __model__[-1][-1][__j__][2] = eval(__model__[-1][-1][__j__][2])
                if isinstance(__model__[-1][-1][__j__][3], str):
                    __model__[-1][-1][__j__][3] = eval(__model__[-1][-1][__j__][3])

        self.__simulator__.ConstructAntenna(Model=__model__)
        self.__simulator__.ConstructWaveguidePort(PortNumber=self.__waveguide_port__[0],
                                                  XRange=self.__waveguide_port__[1],
                                                  YRange=self.__waveguide_port__[2],
                                                  ZRange=self.__waveguide_port__[3])

        return self.__simulator__.TimeDomainSolver(SteadyStateLimit=-47)

    def GenerateRandomParameterValue(self, ParameterIndex=None):
        if ParameterIndex is None:
            __parameter__ = []
            for __i__ in self.__parameter__['range']:
                __parameter__.append(
                    np.random.choice(np.arange(__i__[0],
                                               __i__[1] + self.__parameter_step_size__,
                                               self.__parameter_step_size__))
                )
        else:
            __parameter__ = np.random.choice(np.arange(
                self.__parameter__['range'][ParameterIndex][0],
                self.__parameter__['range'][ParameterIndex][1] + self.__parameter_step_size__,
                self.__parameter_step_size__)
            )

        return __parameter__

    # This function will merely limit the value according to the rules defined by the user, i.e. it will cap the
    # value if it is violating the defined rules.
    def IncrementParameterValue(self, Parameters=None, Index=None):

        Parameters[Index] = Parameters[Index] + self.__parameter_step_size__
        try:
            self.CheckBoundary(Parameters=Parameters)
        except Exception as __error__:
            if self.__debugging__:
                print(__error__)
            Parameters[Index] = Parameters[Index] - self.__parameter_step_size__

    # This function will merely limit the value according to the rules defined by the user, i.e. it will cap the
    # value if it is violating the defined rules.
    def DecrementParameterValue(self, Parameters=None, Index=None):
        Parameters[Index] = Parameters[Index] - self.__parameter_step_size__
        try:
            self.CheckBoundary(Parameters=Parameters)
        except Exception as __error__:
            if self.__debugging__:
                print(__error__)
            Parameters[Index] = Parameters[Index] + self.__parameter_step_size__

    def CheckBoundary(self, Parameters):
        __geometry__ = []
        for __i__ in range(len(self.__model__['geometry'])):
            # If any of the geometry component components are of str type, proceed for boundary checks
            if isinstance(self.__model__['geometry'][__i__][0], str) or \
                    isinstance(self.__model__['geometry'][__i__][1], str) or \
                    isinstance(self.__model__['geometry'][__i__][2], str) or \
                    isinstance(self.__model__['geometry'][__i__][3], str):
                __temp__ = [self.__model__['geometry'][__i__][0],
                            self.__model__['geometry'][__i__][1],
                            self.__model__['geometry'][__i__][2],
                            self.__model__['geometry'][__i__][3]]

                # Replace any parameter names with Parameter[__j__] value
                for __j__ in self.__parameter__:
                    if isinstance(__temp__[0], str):
                        __temp__[0] = __temp__[0].replace(__j__['name'][__j__], Parameters[__j__])
                    if isinstance(__temp__[1], str):
                        __temp__[1] = __temp__[1].replace(__j__['name'][__j__], Parameters[__j__])
                    if isinstance(__temp__[2], str):
                        __temp__[2] = __temp__[2].replace(__j__['name'][__j__], Parameters[__j__])
                    if isinstance(__temp__[3], str):
                        __temp__[3] = __temp__[3].replace(__j__['name'][__j__], Parameters[__j__])

                if isinstance(__temp__[0], str):
                    __temp__[0] = eval(__temp__[0])
                if isinstance(__temp__[1], str):
                    __temp__[1] = eval(__temp__[1])
                if isinstance(__temp__[2], str):
                    __temp__[2] = eval(__temp__[2])
                if isinstance(__temp__[3], str):
                    __temp__[3] = eval(__temp__[3])

                # Compare the limits found from __temp__ with self.__explore_space__ variable
                for __j__ in self.__explore_space__:
                    # If a z range match has been found, proceed
                    if self.__model__['z'][__i__][0] == __j__[0][0] and self.__model__['z'][__i__][1] == __j__[0][1]:
                        if __temp__[0] < __j__[1][0] or __temp__[1] > __j__[1][1] or __temp__[2] < __j__[1][2] or \
                                __temp__[3] > __j__[1][3]:
                            raise Exception(f'<ModelGeometry: CheckBoundary: A geometry component with parameters, '
                                            f'specifically {self.__model__["geometry"][__i__]}, is out of bounds for '
                                            f'explore space {__j__}>')
