from AntennaDesign.misc import RectangularMicrostripPatch, MicrostripTransmissionLine
from AntennaDesign.filing import Filing
from AntennaDesign.antennaGeometry import ModelGeometry
from AntennaDesign.simulator import FineModel
from AntennaDesign.ga import SearchSpaceOptimizer as GA
from AntennaDesign.surrogate import CoarseModel as surrogate
from AntennaDesign.__init__ import *

# Whether to use genetic algorithm to find an optimal solution or not
__search__ = False
# To initiate training of the two surrogates
__train__ = False
# Whether to use the particle swarm optimizer to optimize the model using the two surrogate models, one for return loss
# and one for the gain
__optimize__ = False
# Whether to get the conventional microstrip antenna dimensions or not (for rectangular shape only)
__get_dimensions__ = False
# The ratio of the test, validate, and test data sets
__train_validate_test_ratio__ = [0.7, 0.15, 0.15]
# The range for the surrogates, in gigahertz, to train on
__train_freq_range__ = [1.0, 7.0]

# Create FineModel (simulator) instance
__simulator__ = FineModel(Debugging=True)

# Create a set of parameters for the project
__parameter__ = [
    ['L1', [12.0, 22.0]],
    ['L2', [6.0, 9.0]],
    ['L3', [3.0, 8.0]],
    ['L', [3.0, 5.0]]
]

# Create the antenna model
__model__ = [
    ['Copper (annealed)', 'Ground', 'brick', 'None',
     [0, 0.035], [[-24 / 2, 24 / 2, -20 / 2, -20 / 2 + 2]]],
    ['Rogers RO4003C (lossy)', 'Substrate', 'brick', 'None',
     [0.035, 0.835], [[-24 / 2, 24 / 2, -20 / 2, 20 / 2]]],
    ['Copper (annealed)', 'Patch', 'brick', 'add',
     [0.835, 0.87], [[-1.8 / 2, 1.8 / 2, -20 / 2 + 0.2, -20 / 2 + 2], [-22.5 / 2, 22.5 / 2, -8.0, 10]]],
    ['Copper (annealed)', 'SMA Ground', 'brick', 'add',
     [-6.35 / 2 + 0.695 + 0.3, 6.35 / 2 + 0.695 + 0.3], [[-6.35 / 2, 6.35 / 2, -20 / 2, -20 / 2 - 1.6]]],
    ['Copper (annealed)', 'SMA Ground', 'cylinder', 'add',
     [0, 0], [['Y', 2.5, 2.5 + 0.1, 0, 0, 0.695 + 0.3, [0, 0], [-20 / 2 - 1.6, -20 / 2 - 9.5], [0, 0], 0]]],
    ['Vacuum', 'SMA Ground', 'cylinder', 'subtract',
     [0, 0], [['Y', 0, 1.3, 0, 0, 0.695 + 0.3, [0, 0], [-20 / 2, -20 / 2 - 1.6], [0, 0], 0]]],
    ['PTFE (lossy)', 'SMA Insulator', 'cylinder', 'add',
     [0, 0], [['Y', 0.39, 1.3, 0, 0, 0.695 + 0.3, [0, 0], [-20 / 2, -20 / 2 - 1.6], [0, 0], 0]]],
    ['PTFE (lossy)', 'SMA Insulator', 'cylinder', 'add',
     [0, 0], [['Y', 0.75, 2.5, 0, 0, 0.695 + 0.3, [0, 0], [-20 / 2 - 1.6, -20 / 2 - 9.5], [0, 0], 0]]],
    ['Copper (annealed)', 'SMA Signal', 'cylinder', 'add',
     [0, 0], [['Y', 0, 0.39, 0, 0, 0.695 + 0.3, [0, 0], [-20 / 2, -20 / 2 - 1.6], [0, 0], 0]]],
    ['Copper (annealed)', 'SMA Signal', 'cylinder', 'add',
     [0, 0], [['Y', 0, 0.75, 0, 0, 0.695 + 0.3, [0, 0], [-20 / 2 - 1.6, -20 / 2 - 9.5], [0, 0], 0]]],
    ['Copper (annealed)', 'SMA Signal', 'brick', 'add',
     [0.695 + 0.3 - 0.25 / 2, 0.695 + 0.3 + 0.25 / 2], [[-0.5 / 2, 0.5 / 2, -20 / 2, -20 / 2 + 2.5]]],
    ['Vacuum', 'Patch', 'brick', 'subtract',
     [0.835, 0.87], [['-L1/2', 'L1/2', 'L2/2 + 2', 'L2/2 + 2 - L'],
                     ['-L1/2', '-L1/2 + L', '-L2/2 + 2 - L', 'L2/2 + 2 - L'],
                     ['-L/2', 'L/2', 'L2/2 + 2 - L', 'L2/2 + 2 - L - L3'],
                     ['L1/2', 'L1/2 - L', '-L2/2 + 2 - L', 'L2/2 + 2 - L']
                     ]]
]

# Create the waveguide port dimensions and location for simulations
waveguide = [1, 'Y', 'Positive', [-2.5 - 0.1, 2.5 + 0.1],
             [-20 / 2 - 9.5, -20 / 2 - 9.5],
             [-2.5 - 0.1 + 0.695 + 0.3, 2.5 + 0.1 + 0.695 + 0.3]]

# Create a Filing instance for reading, writing, and appending data
filing = Filing(Debugging=True)

if __search__ or not __train__:
    # Create the ModelGeometry instance (a class that stores the information and geometry of the antenna)
    __antenna__ = ModelGeometry(ParameterStepSize=0.5,
                                Objectives=[[2.36, 2.44, 0.023]],
                                Simulator=__simulator__,
                                ExploreSpace=[[-11.25, 11.25, -8, 10, 0.835, 0.87]],
                                FrequencyRangeMin=__train_freq_range__[0],
                                FrequencyRangeMax=__train_freq_range__[1],
                                Debugging=True)

    # Populate the parameters into the ModelGeometry instance (__antenna__)
    for __i__ in __parameter__:
        __antenna__.AddParameter(Name=__i__[0], Range=__i__[1])

    # Populate the build sequence of the antenna into the ModelGeometry instance (__antenna__)
    for __i__ in __model__:
        __antenna__.AddSequence(Material=__i__[0],
                                ComponentName=__i__[1],
                                Type=__i__[2],
                                Operation=__i__[3],
                                Z=__i__[4],
                                Geometry=__i__[5])

    # Set the waveguide port in the ModelGeometry instance (__antenna__)
    __antenna__.SetWaveguidePort(PortNumber=waveguide[0], Orientation=waveguide[1], ExcitationDirection=waveguide[2],
                                 XRange=waveguide[3], YRange=waveguide[4], ZRange=waveguide[5])
else:
    __antenna__ = None

if __name__ == '__main__':

    # Conventional antenna design dimensions
    if __get_dimensions__:
        RMSP = RectangularMicrostripPatch.RMPA(fr=4.5e9, er=3.55)
        RMSPDimensions = RMSP.get_rmsp_dimensions(__sub_h__=1.5e-3)
        MicrostripTransmissionLine.get_microstrip_transmission_dimensions(__freq__=4.5e9, __er__=3.55,
                                                                          __sub_h__=1.5e-3, __Zo__=50)

    # Genetic algorithm
    if __search__:

        SSO = GA(PopulationSize=12,
                 NumberOfOffspring=6,
                 CrossoverRate=0.5,
                 MutationRate=0.1,
                 modelGeometry=__antenna__,
                 Filing=filing,
                 Directory='E-Shape',
                 Rounding=6,
                 Debugging=False)

        SSO.Search(SearchTimeMinutes=60 * 24 * 4)

    if __train__:
        __data__ = filing.Read(Filename='\\Surrogate\\lhs0')

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
                if len(__s1_train__) < len(__data__) * __train_validate_test_ratio__[0]:
                    __s1_train__.append([copy.deepcopy(__i__[0]), []])
                    for __j__ in range(len(__i__[1][0][0])):
                        if __train_freq_range__[0] <= __i__[1][0][0][__j__] <= __train_freq_range__[1]:
                            __s1_train__[-1][1].append(10 ** (__i__[1][0][1][__j__] / 20))
                    __s2_train__.append([copy.deepcopy(__i__[0]), []])
                    for __j__ in range(len(__i__[1][1][0])):
                        if __train_freq_range__[0] <= __i__[1][1][0][__j__] <= __train_freq_range__[1]:
                            __s2_train__[-1][1].append(1 / (1 + np.exp(10 ** (__i__[1][1][1][__j__] / 10))))
                elif len(__s1_validate__) < len(__data__) * __train_validate_test_ratio__[1]:
                    __s1_validate__.append([copy.deepcopy(__i__[0]), []])
                    for __j__ in range(len(__i__[1][0][0])):
                        if __train_freq_range__[0] <= __i__[1][0][0][__j__] <= __train_freq_range__[1]:
                            __s1_validate__[-1][1].append(10 ** (__i__[1][0][1][__j__] / 20))
                    __s2_validate__.append([copy.deepcopy(__i__[0]), []])
                    for __j__ in range(len(__i__[1][1][0])):
                        if __train_freq_range__[0] <= __i__[1][1][0][__j__] <= __train_freq_range__[1]:
                            __s2_validate__[-1][1].append(1 / (1 + np.exp(10 ** (__i__[1][1][1][__j__] / 10))))
                else:
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
        # __result1__ = None
        __result1__ = \
            __surrogate_1__.Train(BatchSize=4, TrainingData=__s1_train__, ValidationData=__s1_validate__,
                                  TestingData=__s1_test__, LearningRate=1e-3, NumberOfEpochs=None,
                                  TrainDurationMinutes=10, NRMSEConvergence=0.05)
        __result2__ = \
            __surrogate_2__.Train(BatchSize=4, TrainingData=__s2_train__, ValidationData=__s2_validate__,
                                  TestingData=__s2_test__, LearningRate=1e-3, NumberOfEpochs=None,
                                  TrainDurationMinutes=10, NRMSEConvergence=0.05)

        # Plot/Print the results
        plt.figure(1)
        plt.plot(np.linspace(__train_freq_range__[0], __train_freq_range__[1],
                             len(__result1__[0])), __result1__[0], 'r', label='Train')
        plt.plot(np.linspace(__train_freq_range__[0], __train_freq_range__[1],
                             len(__result1__[1])), __result1__[1], 'k', label='Validation')
        plt.title('Return Loss Surrogate')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.grid()
        plt.legend()
        __train_loss__ = sum(__result1__[2]) / len(__result1__[2])
        print(f'Return loss surrogate test loss = {round(__train_loss__, 6)}')

        plt.figure(2)
        plt.plot(np.linspace(__train_freq_range__[0], __train_freq_range__[1],
                             len(__result2__[0])), __result2__[0], 'r', label='Train')
        plt.plot(np.linspace(__train_freq_range__[0], __train_freq_range__[1],
                             len(__result2__[1])), __result2__[1], 'k', label='Validation')
        plt.title('Gain Surrogate')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.grid()
        plt.legend()
        __train_loss__ = sum(__result2__[2]) / len(__result2__[2])
        print(f'Gain surrogate test loss = {round(__train_loss__, 6)}')

        plt.show()

    if not __train__:
        # Surrogate modeling
        __raw_data__ = filing.Read(Filename='\\SSO\\E-Shape\\Best')[0]

        __parameters__ = [[21.5 - 0.5, 21.5 + 0.5], [11 - 0.5, 11 + 0.5], [9 - 0.5, 9 + 0.5], [4 - 0.5, 4 + 0.5]]
        __return_loss__ = __raw_data__[1][0]
        __gain__ = __raw_data__[1][1]

        # Initialize return loss and gain surrogates
        __nn__ = surrogate(NumberOfInputChannels=len(__parameters__), NumberOfHiddenLayers=3,
                           NumberOfOutputChannels=len(__return_loss__[0]), Directory=None,
                           Debugging=True, Filing=filing)

        # Generate dataset
        __data__ = __nn__.BuildDataset(Model=__antenna__,
                                       Parameters=__parameters__,
                                       NumberOfSamples=100, Rounding=12)

    # Particle swarm optimizer
    if __optimize__:
        pass
########################################################################################################################
