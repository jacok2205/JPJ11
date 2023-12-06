from AntennaDesign.misc import RectangularMicrostripPatch
from AntennaDesign.misc import MicrostripTransmissionLine
from AntennaDesign.AntennaGeometry import ModelGeometry
from AntennaDesign.Simulator import FineModel
from AntennaDesign.Filing import Filing
from AntennaDesign.GA import SearchSpaceOptimizer
from AntennaDesign.Surrogate import CoarseModel


if __name__ == '__main__':
    # Conventional antenna design dimensions
    RMSP = RectangularMicrostripPatch.RMPA(fr=5.5e9, er=3.55)
    RMSPDimensions = RMSP.get_rmsp_dimensions(__sub_h__=0.5e-3)
    MicrostripTransmissionLine.get_microstrip_transmission_dimensions(__freq__=5.5e9, __er__=3.55,
                                                                      __sub_h__=0.5e-3, __Zo__=50)

    # Antenna model parameters with initial values
    Parameter = [
        ['x1', 5.5],
        ['x2', 5.5],
        ['y1', 5.5],
        ['T', 1.0]
    ]

    # Static portion will always use the 'add' function to merge all components in layer n
    StaticPortion = [
        ['Copper (annealed)', 'Ground', [0, 0.035], [[-12, 12, -10, -4]]],
        ['Rogers RO4003C (lossy)', 'Substrate', [0.035, 0.535], [[-12, 12, -10, 10]]],
        ['Copper (annealed)', 'Patch', [0.535, 0.57], [[-11, 11, -4.3, 10], [-0.55, 0.55, -10, -4.3]]],
        ['Vacuum', 'Patch', [0.535, 0.57], [
            ['-x1 - T/2', '-T/2', '-y1/2 - T/2', '-y1/2 + T/2'],
            ['-T/2', 'T/2', '-y1/2 - T/2', 'y1/2 + T/2'],
            ['T/2', 'T/2 + x2', 'y1/2 - T/2', 'y1/2 + T/2']]]
    ]

    # [y location, microstrip transmission line width minimum, microstrip transmission line maximum,
    # Z minimum position (substrate min location), Z maximum position (substrate max location), extension
    # coefficient]
    # Waveguide model
    Waveguide = [-10, -0.55, 0.55, 0.035, 0.535, 7.14]

    # Objectives to search for.
    # Objectives = [number of bands, maximum return loss (in dB) to be accepted as a band, band ranges,
    # band edge tolerance, minimum band gain]
    Objectives = [1, -10, [[2.36, 2.44]], [0.023], [2]]

    # Parametric sweep resolution (mm)
    ParameterStepSize = 0.5

    # Create simulator instance
    Simulator = FineModel(S11Results=True, GainResults=True, Debugging=False)

    # Simulator.Initialize(FrequencyRangeMin=1.0, FrequencyRangeMax=7.0)

    Model = ModelGeometry(ParameterStepSize=ParameterStepSize, Objectives=Objectives, Simulator=Simulator,
                          Debugging=False, ExploreSpace=[[-11, 11, -4.3, 10]], FrequencyRangeMin=1,
                          FrequencyRangeMax=7)

    # Initialize waveguide port
    Model.SetWaveguidePort(WaveguidePortPosition=Waveguide[0], TransmissionLineWidthMin=Waveguide[1],
                           TransmissionLineWidthMax=Waveguide[2], SubstrateThicknessMin=Waveguide[3],
                           SubstrateThicknessMax=Waveguide[4], ExtensionCoefficient=Waveguide[5])

    # Populate model parameters that will be dynamically changing
    for __i__ in Parameter:
        Model.AddParameter(Name=__i__[0], Value=__i__[1])

    # Populate model
    for __i__ in StaticPortion:
        Model.AddLayer(Material=__i__[0], LayerName=__i__[1], Z=__i__[2], Geometry=__i__[3])

    # Create a file handler instance
    Filing = Filing(Directories=None, Debugging=False)

    # Create SSO object
    SSO = SearchSpaceOptimizer(PopulationSize=36, NumberOfOffspring=6, CrossoverRate=0.5, MutationRate=0.05,
                               modelGeometry=Model, Filing=Filing, Directory='S-Slotted',
                               Logging=None, Debugging=False)

    Surrogate = CoarseModel(NumberOfHiddenLayers=6, NumberOfInputChannels=28, NumberOfOutputChannels=3, Learn=True,
                            BatchSize=10, LearningRate=1e-3, LeakageRatio=0.01, ValidationAccuracy=0.9,
                            Filing=Filing, Directory='S-Slotted', Logging=None, Debugging=False)

    # Begin search process of defined model
    SSO.Search(SearchTimeMinutes=(96 * 60), GainFitness=False, Convergence=0.01)

    # Model.SimulateModel(Parameters=[5.5, 5.5, 5.5, 1.0])
    # lst = [[5.5, 5.5, 5.5, 1.0], [0, 0]]
    # Model.IncrementParameterValue(Parameters=lst[0], XYOffsets=lst[1], Index=0, FocusOnParameters=False)
    # print(lst[1])
    # Model.DecrementParameterValue(Parameters=lst[0], XYOffsets=lst[1], Index=0, FocusOnParameters=False)
    # print(lst[1])
    # while True:
        # print(Model.GenerateRandomOffsets())
        # Model.GenerateRandomOffsets()
    # Model.ConstructDynamicPortion(Parameters=[5.5, 5.5, 5.5, 1.0])

    #         temp = Geometry[0][0]
    #         print(temp)
    #         print(self.__parameter__)
    #         for i in range(len(self.__parameter__['name'])):
    #             temp = temp.replace(self.__parameter__['name'][i], str(self.__parameter__['value'][i]))
    #
    # def CalculateStringExpression(self, String):
    #     return eval(String)