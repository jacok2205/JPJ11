from AntennaDesign.__init__ import *


class ModelGeometry:
    def __init__(self, ParameterStepSize, Objectives=None, Simulator=None, ExploreSpace=None,
                 FrequencyRangeMin=1, FrequencyRangeMax=7, Debugging=False):

        if Simulator is None or ExploreSpace is None:
            raise Exception('<ModelGeometry: __init__: A simulator and an explore space are required to proceed>')

        # The __parameter__ variable is the core for all three phases (space exploration, fine modeling, and
        # optimization phases), where only the 'name' and 'value' portions are considered for a single datapoint.
        # 'value' is the initial design made manually by the user.
        self.__parameter__ = {'name': [], 'range': []}
        # The __static__/__dynamic__ variable will be stored in the first part of the logging/filing of results for
        # a reference. The sole objective of the __skeleton__ variable is purely for CST simulations. 'geometry'
        # is a list of geometry components, where each element within a component is a string.
        self.__model__ = {'material': [], 'name': [], 'type': [], 'operation': [], 'z': [], 'geometry': []}

        self.__waveguide_port__ = None
        self.__parameter_step_size__ = ParameterStepSize
        # Objective = [1, -10, [[2.33, 2.44]], [0.023]], where 1 is number of bands, -10 is the maximum return loss
        # for a band, 2.33 - 2.44 is a band's band, 0.023 is the band edge tolerances.
        self.__objective__ = Objectives
        self.__debugging__ = Debugging
        self.__rounding__ = 9
        self.__simulator__ = Simulator

        # [layer name, [Xmin, Xmax, Ymin, Ymax]]
        self.__explore_space__ = ExploreSpace

        self.__simulator__.Initialize(FrequencyRangeMin, FrequencyRangeMax, DimensionUnits='mm',
                                      TemperatureUnits='Kelvin', FrequencyUnits='GHz', TimeUnits='ns',
                                      VoltageUnits='V', CurrentUnits='A', ResistanceUnits='Ohm',
                                      ConductanceUnits='Siemens', CapacitanceUnits='PikoF', InductanceUnits='nanoH')

    def SetObjectives(self, Objectives=None):
        if Objectives is None:
            raise Exception('<ModelGeometry: SetObjectives: Argument is of None type>')
        self.__objective__ = Objectives

    def SetDebugging(self, Value=None):
        if Value is None:
            raise Exception('<ModelGeometry: SetDebugging: Argument is of None type>')
        self.__debugging__ = Value

    def GetDebuggingStatus(self):
        return self.__debugging__

    # This function is used to store all parameters of the dynamic portion of the model
    def AddParameter(self, Name=None, Value=None):
        if Name is None or Value is None:
            raise Exception('<AntennaGeometry: AddParameter: One or more parameters are of None type>')

        # Remember, __parameter__ needs to be in the following format:
        # __parameter__ = ['name', 'initial value', range]
        # range = [min, max], where min/max are of type string or of type float (only if a boundary)
        self.__parameter__['name'].append(Name)
        self.__parameter__['value'].append(Value)

    def AddLayer(self, Material=None, LayerName=None, Z=None, Geometry=None):
        if Material is None or LayerName is None or Z is None or Geometry is None:
            raise Exception('<AntennaGeometry: AddLayer: One or more parameters are of None type>')

        # Remember, __layer__ needs to be in the following format:
        # __layer__ = ['CST material name', 'layer name', 'type of operation such as add or subtract',
        # 'z range', 'geometry component list']
        self.__model__['material'].append(Material)
        self.__model__['name'].append(LayerName)
        self.__model__['z'].append(Z)
        self.__model__['geometry'].append(Geometry)

    # WaveguidePortPosition = [xpos, ypos, zpos]
    # TransmissionLineWidth = value[parameter] - value[parameter]
    # SubstrateThickness = value[parameter]
    def SetWaveguidePort(self, WaveguidePortPosition=None, TransmissionLineWidthMin=None,
                         TransmissionLineWidthMax=None, SubstrateThicknessMin=None, SubstrateThicknessMax=None,
                         ExtensionCoefficient=5.0):
        if WaveguidePortPosition is None or TransmissionLineWidthMin is None or \
                TransmissionLineWidthMax is None or SubstrateThicknessMin is None or \
                SubstrateThicknessMax is None:
            self.__waveguide_port__ = None
            raise Exception('<ModelGeometry: SetWaveguidePort: One or more parameters is of type None>')
        self.__waveguide_port__ = [WaveguidePortPosition, TransmissionLineWidthMin,
                                   TransmissionLineWidthMax, SubstrateThicknessMin,
                                   SubstrateThicknessMax, ExtensionCoefficient]

    def SimulateModel(self, Parameters=None, XYOffset=None):
        if Parameters is None:
            raise Exception('<ModelGeometry: SimulateModel: Parameters is of None type>')
        if XYOffset is None:
            raise Exception('<ModelGeometry: SimulateModel: XYOffset is of None type>')
        if self.__waveguide_port__ is None:
            raise Exception('<ModelGeometry: SimulateModel: Waveguide port has not been set up>')

        __model__ = []
        for __i__ in range(len(self.__model__['material'])):

            __model__.append([self.__model__['material'][__i__],
                              self.__model__['name'][__i__],
                              self.__model__['z'][__i__], self.__model__['geometry'][__i__]])

            if self.__model__['material'][__i__] == 'Vacuum':
                for __j__ in range(len(self.__model__['geometry'][__i__])):

                    for __k__ in range(len(self.__parameter__['name'])):
                        __model__[-1][-1][__j__][0] = __model__[-1][-1][__j__][0].replace(
                            self.__parameter__['name'][__k__], str(Parameters[__k__]))
                        __model__[-1][-1][__j__][1] = __model__[-1][-1][__j__][1].replace(
                            self.__parameter__['name'][__k__], str(Parameters[__k__]))
                        __model__[-1][-1][__j__][2] = __model__[-1][-1][__j__][2].replace(
                            self.__parameter__['name'][__k__], str(Parameters[__k__]))
                        __model__[-1][-1][__j__][3] = __model__[-1][-1][__j__][3].replace(
                            self.__parameter__['name'][__k__], str(Parameters[__k__]))

                    __model__[-1][-1][__j__][0] = eval(__model__[-1][-1][__j__][0]) + XYOffset[0]
                    __model__[-1][-1][__j__][1] = eval(__model__[-1][-1][__j__][1]) + XYOffset[0]
                    __model__[-1][-1][__j__][2] = eval(__model__[-1][-1][__j__][2]) + XYOffset[1]
                    __model__[-1][-1][__j__][3] = eval(__model__[-1][-1][__j__][3]) + XYOffset[1]

        self.__simulator__.ConstructAntenna(Model=__model__)
        self.__simulator__.ConstructWaveguidePort(WaveguidePortPosition=self.__waveguide_port__[0],
                                                  TransmissionLineWidthMin=self.__waveguide_port__[1],
                                                  TransmissionLineWidthMax=self.__waveguide_port__[2],
                                                  SubstrateThicknessMin=self.__waveguide_port__[3],
                                                  SubstrateThicknessMax=self.__waveguide_port__[4],
                                                  ExtensionCoefficient=self.__waveguide_port__[5])

        return self.__simulator__.TimeDomainSolver(SteadyStateLimit=-47)

    # Gets called at GA initialization
    def GenerateRandomOffsets(self):
        __geometry__ = []
        for __i__ in range(len(self.__model__['geometry'])):
            if self.__model__['material'][__i__] == 'Vacuum':
                for __j__ in self.__model__['geometry'][__i__]:
                    __temp__ = [__j__[0], __j__[1], __j__[2], __j__[3]]
                    for __k__ in range(len(self.__parameter__['name'])):
                        __temp__[0] = \
                            __temp__[0].replace(self.__parameter__['name'][__k__], str(self.__parameter__['value'][__k__]))
                        __temp__[1] = \
                            __temp__[1].replace(self.__parameter__['name'][__k__], str(self.__parameter__['value'][__k__]))
                        __temp__[2] = \
                            __temp__[2].replace(self.__parameter__['name'][__k__], str(self.__parameter__['value'][__k__]))
                        __temp__[3] = \
                            __temp__[3].replace(self.__parameter__['name'][__k__], str(self.__parameter__['value'][__k__]))
                    __temp__[0] = eval(__temp__[0])
                    __temp__[1] = eval(__temp__[1])
                    __temp__[2] = eval(__temp__[2])
                    __temp__[3] = eval(__temp__[3])
                    __geometry__.append(__temp__)

        # Get slot extreme minimum and maximum slot x/y values
        __slot_x_min__ = __geometry__[0][0]
        __slot_x_max__ = __geometry__[0][1]
        __slot_y_min__ = __geometry__[0][2]
        __slot_y_max__ = __geometry__[0][3]
        for __i__ in __geometry__:
            if __i__[0] < __slot_x_min__:
                __slot_x_min__ = __i__[0]
            if __i__[1] > __slot_x_max__:
                __slot_x_max__ = __i__[1]
            if __i__[2] < __slot_y_min__:
                __slot_y_min__ = __i__[2]
            if __i__[3] > __slot_y_max__:
                __slot_y_max__ = __i__[3]

        # Check if the min/max x/y values conform to the explore space boundaries, in other words does not exceed
        # the explore space boundaries
        __x_range__ = [0, 0]
        __y_range__ = [0, 0]
        for __i__ in self.__explore_space__:
            if __slot_x_min__ < __i__[0] or __slot_x_max__ > __i__[1] \
                    or __slot_y_min__ < __i__[2] or __slot_y_max__ > __i__[3]:
                raise Exception('<ModelGeometry: GenerateRandomOffsets: '
                                'Initial slot is too large for given explore space>')
            if round(__i__[0] - __slot_x_min__, self.__rounding__) < __x_range__[0]:
                __x_range__[0] = round(__i__[0] - __slot_x_min__, self.__rounding__)
            if round(__i__[1] - __slot_x_max__, self.__rounding__) > __x_range__[1]:
                __x_range__[1] = round(__i__[1] - __slot_x_max__, self.__rounding__)
            if round(__i__[2] - __slot_y_min__, self.__rounding__) < __y_range__[0]:
                __y_range__[0] = round(__i__[2] - __slot_y_min__, self.__rounding__)
            if round(__i__[3] - __slot_y_max__, self.__rounding__) > __y_range__[1]:
                __y_range__[1] = round(__i__[3] - __slot_y_max__, self.__rounding__)

        __x_arange__ = np.arange(__x_range__[0],
                                 __x_range__[1] + self.__parameter_step_size__,
                                 self.__parameter_step_size__).tolist()
        __y_arange__ = np.arange(__y_range__[0],
                                 __y_range__[1] + self.__parameter_step_size__,
                                 self.__parameter_step_size__).tolist()

        __index__ = 0
        while __index__ < len(__x_arange__):
            __x_arange__[__index__] = round(__x_arange__[__index__], self.__rounding__)
            if __x_arange__[__index__] < __x_range__[0] or __x_arange__[__index__] > __x_range__[1]:
                __x_arange__.pop(__index__)
            else:
                __index__ += 1

        __index__ = 0
        while __index__ < len(__y_arange__):
            __y_arange__[__index__] = round(__y_arange__[__index__], self.__rounding__)
            if __y_arange__[__index__] < __y_range__[0] or __y_arange__[__index__] > __y_range__[1]:
                __y_arange__.pop(__index__)
            else:
                __index__ += 1

        # Generate random x offset
        __x_offset__ = np.random.choice(__x_arange__)

        # Generate random y offset
        __y_offset__ = np.random.choice(__y_arange__)

        return [round(__x_offset__, self.__rounding__), round(__y_offset__, self.__rounding__)]

    # This function will merely limit the value according to the rules defined by the user, i.e. it will cap the
    # value if it is violating the defined rules.
    def IncrementParameterValue(self, Parameters=None, XYOffsets=None, Index=None, FocusOnParameters=True):
        if FocusOnParameters:
            Parameters[Index] = Parameters[Index] + self.__parameter_step_size__
            try:
                self.CheckBoundary(Parameters=Parameters, XYOffsets=XYOffsets)
            except Exception as __error__:
                if self.__debugging__:
                    print(__error__)
                Parameters[Index] = Parameters[Index] - self.__parameter_step_size__

        else:
            XYOffsets[Index] = XYOffsets[Index] + self.__parameter_step_size__
            try:
                self.CheckBoundary(Parameters=Parameters, XYOffsets=XYOffsets)
            except Exception as __error__:
                if self.__debugging__:
                    print(__error__)
                XYOffsets[Index] = XYOffsets[Index] - self.__parameter_step_size__

    # This function will merely limit the value according to the rules defined by the user, i.e. it will cap the
    # value if it is violating the defined rules.
    def DecrementParameterValue(self, Parameters=None, XYOffsets=None, Index=None, FocusOnParameters=True):
        if FocusOnParameters:
            Parameters[Index] = Parameters[Index] - self.__parameter_step_size__
            try:
                self.CheckBoundary(Parameters=Parameters, XYOffsets=XYOffsets)
            except Exception as __error__:
                if self.__debugging__:
                    print(__error__)
                Parameters[Index] = Parameters[Index] + self.__parameter_step_size__

        else:
            XYOffsets[Index] = XYOffsets[Index] - self.__parameter_step_size__
            try:
                self.CheckBoundary(Parameters=Parameters, XYOffsets=XYOffsets)
            except Exception as __error__:
                if self.__debugging__:
                    print(__error__)
                XYOffsets[Index] = XYOffsets[Index] + self.__parameter_step_size__

    def CheckBoundary(self, Parameters, XYOffsets):
        __geometry__ = []
        for __i__ in range(len(self.__model__['geometry'])):
            if self.__model__['material'][__i__] == 'Vacuum':
                for __j__ in self.__model__['geometry'][__i__]:
                    __temp__ = [__j__[0], __j__[1], __j__[2], __j__[3]]
                    for __k__ in range(len(self.__parameter__['name'])):
                        __temp__[0] = \
                            __temp__[0].replace(self.__parameter__['name'][__k__], str(Parameters[__k__]))
                        __temp__[1] = \
                            __temp__[1].replace(self.__parameter__['name'][__k__], str(Parameters[__k__]))
                        __temp__[2] = \
                            __temp__[2].replace(self.__parameter__['name'][__k__], str(Parameters[__k__]))
                        __temp__[3] = \
                            __temp__[3].replace(self.__parameter__['name'][__k__], str(Parameters[__k__]))
                    __temp__[0] = eval(__temp__[0]) + XYOffsets[0]
                    __temp__[1] = eval(__temp__[1]) + XYOffsets[0]
                    __temp__[2] = eval(__temp__[2]) + XYOffsets[1]
                    __temp__[3] = eval(__temp__[3]) + XYOffsets[1]
                    __geometry__.append(__temp__)

        # Get slot extreme minimum and maximum slot x/y values
        __slot_x_min__ = __geometry__[0][0]
        __slot_x_max__ = __geometry__[0][1]
        __slot_y_min__ = __geometry__[0][2]
        __slot_y_max__ = __geometry__[0][3]
        for __i__ in __geometry__:
            if __i__[0] < __slot_x_min__:
                __slot_x_min__ = __i__[0]
            if __i__[1] > __slot_x_max__:
                __slot_x_max__ = __i__[1]
            if __i__[2] < __slot_y_min__:
                __slot_y_min__ = __i__[2]
            if __i__[3] > __slot_y_max__:
                __slot_y_max__ = __i__[3]

        # Check if the min/max x/y values conform to the explore space boundaries, in other words does not exceed
        # the explore space boundaries
        for __i__ in self.__explore_space__:
            if __slot_x_min__ < __i__[0] or __slot_x_max__ > __i__[1] \
                    or __slot_y_min__ < __i__[2] or __slot_y_max__ > __i__[3]:
                raise Exception('<ModelGeometry: CheckBoundary: '
                                'Parameter is out of bounds for given explore space>')
