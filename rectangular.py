from AntennaDesign.misc import RectangularMicrostripPatch, MicrostripTransmissionLine
from AntennaDesign.filing import Filing
from AntennaDesign.antennaGeometry import ModelGeometry
from AntennaDesign.simulator import FineModel
from AntennaDesign.ga import SearchSpaceOptimizer as GA

if __name__ == '__main__':
    # Conventional antenna design dimensions
    RMSP = RectangularMicrostripPatch.RMPA(fr=2.4e9, er=3.55)
    RMSPDimensions = RMSP.get_rmsp_dimensions(__sub_h__=0.5e-3)
    MicrostripTransmissionLine.get_microstrip_transmission_dimensions(__freq__=2.4e9, __er__=3.55,
                                                                      __sub_h__=0.5e-3, __Zo__=50)
    # filing = Filing(Directories=None, Debugging=True)
    #
    # filing.CreateDirectories(Directories=['\\root'])
    # filing.CreateFile(Filename='\\root\\test1')
    # filing.CreateFile(Filename='\\root\\test2')
    # filing.DeleteFile(Filename='\\root\\test2')
    #
    # lists = [[[1, 2, 3], []], [[4, 5, 6], []], [[7, 8, 9], []]]
    # filing.Save(Filename='\\root\\test1', Lists=lists)
    # print(filing.Duplicate(Filename='\\root\\test1', List=[[1, 2, 3], []]))

    simulator = FineModel(Debugging=True)
    # simulator.Initialize(FrequencyRangeMin=1, FrequencyRangeMax=7)

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

    # simulator.ConstructAntenna(Model=model)
    # simulator.ConstructWaveguidePort(PortNumber=waveguide[0], Orientation=waveguide[1], ExcitationDirection=waveguide[2], XRange=waveguide[3],
    #                                  YRange=waveguide[4], ZRange=waveguide[5])
    # print(simulator.TimeDomainSolver(SteadyStateLimit=-40))

    antenna = ModelGeometry(ParameterStepSize=1.0,
                            Objectives=[[2.36, 2.44, 0.023]],
                            Simulator=simulator,
                            ExploreSpace=[[-11, 11, -5, 10, 0.535, 0.57], [-12, 12, -9.5, 8, 0, 0.035]],
                            FrequencyRangeMin=1.0,
                            FrequencyRangeMax=7.0,
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
    antenna.SetWaveguidePort(PortNumber=waveguide[0], Orientation=waveguide[1], ExcitationDirection=waveguide[2], XRange=waveguide[3],
                             YRange=waveguide[4], ZRange=waveguide[5])

    filing = Filing(Debugging=True)

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

    # params = antenna.GenerateRandomParameterValue(Parameters=None, ParameterIndex=None, Rounding=6)
    # num = 0
    # while True:
    #     num += 1
    #     params = antenna.GenerateRandomParameterValue(Parameters=None, ParameterIndex=None, Rounding=6)
    #     print(f'\r{params} \t {num}')
    #     temp = antenna.GenerateRandomParameterValue(Parameters=params, ParameterIndex=np.random.choice(range(len(params))), Rounding=6)
    #     antenna.SimulateModel(Parameters=params, Rounding=6)
    #     time.sleep(10)
    #     print(temp)
    # END
