from AntennaDesign.misc import RectangularMicrostripPatch, MicrostripTransmissionLine
from AntennaDesign.filing import Filing
from AntennaDesign.antennaGeometry import ModelGeometry
from AntennaDesign.simulator import FineModel
from AntennaDesign.ga import SearchSpaceOptimizer as GA
from AntennaDesign.surrogate import CoarseModel as surrogate
from AntennaDesign.__init__ import *

__search__ = False
__get_dimensions__ = False
__train_validate_test_ratio__ = [0.8, 0.1, 0.1]
__train_freq_range__ = [2.3, 2.5]

if __name__ == '__main__':
    __freq_min__ = 1.0
    __freq_max__ = 7.0

    if __get_dimensions__:
        # Conventional antenna design dimensions
        RMSP = RectangularMicrostripPatch.RMPA(fr=2.4e9, er=3.55)
        RMSPDimensions = RMSP.get_rmsp_dimensions(__sub_h__=0.5e-3)
        MicrostripTransmissionLine.get_microstrip_transmission_dimensions(__freq__=2.4e9, __er__=3.55,
                                                                          __sub_h__=0.5e-3, __Zo__=50)

    simulator = FineModel(Debugging=True)

    parameter = [
        ['h1', [0.5, 21.5]],
        ['h2', [0.5, 21.5]],
        ['h3', [0.5, 21.5]],
        ['h4', [0.5, 23.5]],
        ['h5', [0.5, 23.5]],
        ['y1', [0, 14]],
        ['y2', [0, 14]],
        ['y3', [0, 14]],
        ['y4', [0, 16.5]],
        ['y5', [0, 16.5]],
        ['T', [0.5, 2.0]]
    ]

    model = [
        ['Copper (annealed)', 'Ground', 'brick', 'None',
         [0, 0.035], [[-24/2, 24/2, -20/2, -20/2 + 18]]],
        ['Rogers RO4003C (lossy)', 'Substrate', 'brick', 'None',
         [0.035, 0.035 + 0.5], [[-24/2, 24/2, -20/2, 20/2]]],
        ['Copper (annealed)', 'Patch', 'brick', 'add',
         [0.535, 0.57], [[-1.1/2, 1.1/2, -20/2, -20/2 + 6], [-22/2, 22/2, -5.0, 10]]],
        ['Copper (annealed)', 'SMA Ground', 'brick', 'add',
         [-6.35/2 + 0.695, 6.35/2 + 0.695], [[-6.35/2, 6.35/2, -20/2, -20/2 - 1.6]]],
        ['Copper (annealed)', 'SMA Ground', 'brick', 'add',
         [-6.35/2 + 0.695, -6.35/2 + 2.48 + 0.695], [[-6.35/2, -6.35/2 + 1, -20/2, -20/2 + 4.7],
                                                     [6.35/2, 6.35/2 - 1, -20/2, -20/2 + 4.7]]],
        ['Copper (annealed)', 'SMA Ground', 'cylinder', 'add',
         [0, 0], [['Y', 2.5, 2.5 + 0.1, 0, 0, 0.695, [0, 0], [-20/2 - 1.6, -20 / 2 - 9.5], [0, 0], 0]]],
        ['Vacuum', 'SMA Ground', 'cylinder', 'subtract',
         [0, 0], [['Y', 0, 1.3, 0, 0, 0.695, [0, 0], [-20/2, -20/2 - 1.6], [0, 0], 0]]],
        ['PTFE (lossy)', 'SMA Insulator', 'cylinder', 'add',
         [0, 0], [['Y', 0.39, 1.3, 0, 0, 0.695, [0, 0], [-20/2, -20/2 - 1.6], [0, 0], 0]]],
        ['PTFE (lossy)', 'SMA Insulator', 'cylinder', 'add',
         [0, 0], [['Y', 0.75, 2.5, 0, 0, 0.695, [0, 0], [-20/2 - 1.6, -20 / 2 - 9.5], [0, 0], 0]]],
        ['Copper (annealed)', 'SMA Signal', 'cylinder', 'add',
         [0, 0], [['Y', 0, 0.39, 0, 0, 0.695, [0, 0], [-20 / 2, -20 / 2 - 1.6], [0, 0], 0]]],
        ['Copper (annealed)', 'SMA Signal', 'cylinder', 'add',
         [0, 0], [['Y', 0, 0.75, 0, 0, 0.695, [0, 0], [-20 / 2 - 1.6, -20 / 2 - 9.5], [0, 0], 0]]],
        ['Copper (annealed)', 'SMA Signal', 'brick', 'add',
         [0.695 - 0.25/2, 0.695 + 0.25/2], [[-0.5/2, 0.5/2, -20/2, -20/2 + 2.5]]],
        ['Vacuum', 'Ground', 'brick', 'subtract',
         [0, 0.035], [['12 - h5', 12, '-9 + y5 - T/2', '-9 + y5 + T/2'],
                      [-12, '-12 + h4', '-9 + y4 - T/2', '-9 + y4 + T/2']]],
        ['Vacuum', 'Patch', 'brick', 'subtract',
         [0.535, 0.57], [[-11, '-11 + h1', '-4 + y1 - T/2', '-4 + y1 + T/2'],
                         ['11 - h2', 11, '-4 + y2 - T/2', '-4 + y2 + T/2'],
                         [-11, '-11 + h3', '-4 + y3 - T/2', '-4 + y3 + T/2']]]
    ]
    waveguide = [1, 'Y', 'Positive', [-2.5 - 0.1, 2.5 + 0.1],
                 [-20/2 - 9.5, -20/2 - 9.5],
                 [-2.5 - 0.1 + 0.695, 2.5 + 0.1 + 0.695]]

    filing = Filing(Debugging=True)

    antenna = ModelGeometry(ParameterStepSize=1.0,
                            Objectives=[[2.36, 2.44, 0.023]],
                            Simulator=simulator,
                            ExploreSpace=[[-11, 11, -5, 10, 0.535, 0.57], [-12, 12, -9.5, 8, 0, 0.035]],
                            FrequencyRangeMin=__freq_min__,
                            FrequencyRangeMax=__freq_max__,
                            Debugging=True)

    for __i__ in parameter:
        antenna.AddParameter(Name=__i__[0], Range=__i__[1])

    for __i__ in model:
        antenna.AddSequence(Material=__i__[0],
                            ComponentName=__i__[1],
                            Type=__i__[2],
                            Operation=__i__[3],
                            Z=__i__[4],
                            Geometry=__i__[5])
    antenna.SetWaveguidePort(PortNumber=waveguide[0], Orientation=waveguide[1], ExcitationDirection=waveguide[2],
                             XRange=waveguide[3], YRange=waveguide[4], ZRange=waveguide[5])

    if __search__:

        SSO = GA(PopulationSize=12,
                 NumberOfOffspring=6,
                 CrossoverRate=0.5,
                 MutationRate=0.1,
                 modelGeometry=antenna,
                 Filing=filing,
                 Directory='Test',
                 Rounding=6,
                 Debugging=False)

        SSO.Search(SearchTimeMinutes=60 * 24 * 4)

    else:
        # Surrogate modeling
        __raw_data__ = filing.Read(Filename='\\SSO\\Test\\Best')[0]

        __parameters__ = __raw_data__[0]
        __return_loss__ = __raw_data__[1][0]
        __gain__ = __raw_data__[1][1]

        # Initialize return loss and gain surrogates
        __nn__ = surrogate(NumberOfInputChannels=len(__parameters__), NumberOfHiddenLayers=3,
                           NumberOfOutputChannels=len(__return_loss__[0]), Directory=None,
                           Debugging=True, Filing=filing)

        # Generate dataset
        __data__ = __nn__.BuildDataset(Model=antenna,
                                       Parameters=[[__i__ - 0.2, __i__ + 0.2] for __i__ in __parameters__],
                                       NumberOfSamples=100, Rounding=12)

        # Create training, validation, and testing data sub-sets
        __s1_train__ = []
        __s1_validate__ = []
        __s1_test__ = []
        __s2_train__ = []
        __s2_validate__ = []
        __s2_test__ = []
        __not_full__ = True
        while __not_full__:
            for __i__ in __data__:

                if len(__s1_train__) < len(__i__) * __train_validate_test_ratio__[0] and \
                    np.random.choice([True, False],
                                     p=[__train_validate_test_ratio__[0], 1 - __train_validate_test_ratio__[0]]):

                    __s1_train__.append([copy.deepcopy(__i__[0]), []])
                    for __j__ in range(len(__i__[1][0][0])):
                        if __train_freq_range__[0] <= __i__[1][0][0][__j__] <= __train_freq_range__[1]:
                            __s1_train__[-1][1].append(10 ** (__i__[1][0][1][__j__] / 20))
                    __s2_train__.append([copy.deepcopy(__i__[0]), []])
                    for __j__ in range(len(__i__[1][1][0])):
                        if __train_freq_range__[0] <= __i__[1][1][0][__j__] <= __train_freq_range__[1]:
                            __s2_train__[-1][1].append(1 / (1 + np.exp(10 ** (__i__[1][1][1][__j__] / 10))))

                elif len(__s1_validate__) < len(__i__) * __train_validate_test_ratio__[1] and \
                        np.random.choice([True, False],
                                         p=[__train_validate_test_ratio__[1], 1 - __train_validate_test_ratio__[1]]):

                    __s1_validate__.append([copy.deepcopy(__i__[0]), []])
                    for __j__ in range(len(__i__[1][0][0])):
                        if __train_freq_range__[0] <= __i__[1][0][0][__j__] <= __train_freq_range__[1]:
                            __s1_validate__[-1][1].append(10 ** (__i__[1][0][1][__j__] / 20))
                    __s2_validate__.append([copy.deepcopy(__i__[0]), []])
                    for __j__ in range(len(__i__[1][1][0])):
                        if __train_freq_range__[0] <= __i__[1][1][0][__j__] <= __train_freq_range__[1]:
                            __s2_validate__[-1][1].append(1 / (1 + np.exp(10 ** (__i__[1][1][1][__j__] / 10))))

                elif len(__s1_test__) < len(__i__) * __train_validate_test_ratio__[2] and \
                        np.random.choice([True, False],
                                         p=[__train_validate_test_ratio__[2], 1 - __train_validate_test_ratio__[2]]):

                    __s1_test__.append([copy.deepcopy(__i__[0]), []])
                    for __j__ in range(len(__i__[1][0][0])):
                        if __train_freq_range__[0] <= __i__[1][0][0][__j__] <= __train_freq_range__[1]:
                            __s1_test__[-1][1].append(10 ** (__i__[1][0][1][__j__] / 20))
                    __s2_test__.append([copy.deepcopy(__i__[0]), []])
                    for __j__ in range(len(__i__[1][1][0])):
                        if __train_freq_range__[0] <= __i__[1][1][0][__j__] <= __train_freq_range__[1]:
                            __s2_test__[-1][1].append(1 / (1 + np.exp(10 ** (__i__[1][1][1][__j__] / 10))))

            if len(__data__) == (len(__s1_train__) + len(__s1_validate__) + len(__s1_test__)):
                __not_full__ = False

        # Initialize the surrogates (return loss surrogate and gain surrogate)
        __surrogate_1__ = surrogate(NumberOfHiddenLayers=3, NumberOfInputChannels=len(__data__[0][0]),
                                    NumberOfOutputChannels=len(__s1_train__[0][1]), Filing=filing,
                                    Directory='return loss', Debugging=True)
        __surrogate_2__ = surrogate(NumberOfHiddenLayers=3, NumberOfInputChannels=len(__data__[0][0]),
                                    NumberOfOutputChannels=len(__s2_train__[0][1]), Filing=filing,
                                    Directory='gain', Debugging=True)

        # Train the surrogates
        __surrogate_1__.Train(TrainingData=__s1_train__, ValidationData=__s1_validate__, TestingData=__s1_test__,
                              LearningRate=1e-3, NumberOfEpochs=None, TrainDurationMinutes=10, NRMSEConvergence=0.05)
        __surrogate_2__.Train(TrainingData=__s2_train__, ValidationData=__s2_validate__, TestingData=__s2_test__,
                              LearningRate=1e-3, NumberOfEpochs=None, TrainDurationMinutes=10, NRMSEConvergence=0.05)
