from AntennaDesign.misc import RectangularMicrostripPatch, MicrostripTransmissionLine
from AntennaDesign.filing import Filing
from AntennaDesign.antennaGeometry import ModelGeometry
from AntennaDesign.simulator import FineModel

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
    simulator.Initialize(FrequencyRangeMin=1, FrequencyRangeMax=7)

    model = [
        ['Copper (annealed)', 'Ground', 'brick', 'None', [0, 0.035], [[-24/2, 24/2, -20/2, -20/2 + 18]]],
        ['Rogers RO4003C (lossy)', 'Substrate', 'brick', 'None', [0.035, 0.035 + 0.5], [[-24/2, 24/2, -20/2, 20/2]]],
        ['Copper (annealed)', 'Patch', 'brick', 'add', [0.535, 0.57], [[-1.1/2, 1.1/2, -20/2, -20/2 + 6], [-22/2, 22/2, -5.0, 10]]],
        ['Copper (annealed)', 'SMA Ground', 'brick', 'add', [-6.35/2 + 0.695, 6.35/2 + 0.695], [[-6.35/2, 6.35/2, -20/2, -20/2 - 1.6]]],
        ['Copper (annealed)', 'SMA Ground', 'brick', 'add', [-6.35/2 + 0.695, -6.35/2 + 2.48 + 0.695], [[-6.35/2, -6.35/2 + 1, -20/2, -20/2 + 4.7], [6.35/2, 6.35/2 - 1, -20/2, -20/2 + 4.7]]],
        ['Copper (annealed)', 'SMA Ground', 'cylinder', 'add', [0, 0], [['Y', 2.5, 2.5 + 0.1, 0, 0, 0.695, [0, 0], [-20/2 - 1.6, -20 / 2 - 9.5], [0, 0], 0]]],
        ['Vacuum', 'SMA Ground', 'cylinder', 'subtract', [0, 0], [['Y', 0, 1.3, 0, 0, 0.695, [0, 0], [-20/2, -20/2 - 1.6], [0, 0], 0]]],
        ['PTFE (lossy)', 'SMA Insulator', 'cylinder', 'add', [0, 0], [['Y', 0.39, 1.3, 0, 0, 0.695, [0, 0], [-20/2, -20/2 - 1.6], [0, 0], 0]]],
        ['PTFE (lossy)', 'SMA Insulator', 'cylinder', 'add', [0, 0], [['Y', 0.75, 2.5, 0, 0, 0.695, [0, 0], [-20/2 - 1.6, -20 / 2 - 9.5], [0, 0], 0]]],
        ['Copper (annealed)', 'SMA Signal', 'cylinder', 'add', [0, 0], [['Y', 0, 0.39, 0, 0, 0.695, [0, 0], [-20 / 2, -20 / 2 - 1.6], [0, 0], 0]]],
        ['Copper (annealed)', 'SMA Signal', 'cylinder', 'add', [0, 0], [['Y', 0, 0.75, 0, 0, 0.695, [0, 0], [-20 / 2 - 1.6, -20 / 2 - 9.5], [0, 0], 0]]],
        ['Copper (annealed)', 'SMA Signal', 'brick', 'add', [0.695 - 0.25/2, 0.695 + 0.25/2], [[-0.5/2, 0.5/2, -20/2, -20/2 + 2.5]]],
        ['Vacuum', 'Ground', 'brick', 'subtract', [0, 0.035], [[2, 12, 2.25, 3.75], [-12, -2, 0.25, 1.75]]],
        ['Vacuum', 'Patch', 'brick', 'subtract', [0.535, 0.57], [[-11, 4, -3.6, -2.1], [11, -5, 2.1, 3.6], [-11, 10, 7.2, 8.7]]]
    ]
    waveguide = [1, 'Y', 'Positive', [-2.5 - 0.1, 2.5 + 0.1], [-20/2 - 9.5, -20/2 - 9.5], [-2.5 - 0.1 + 0.695, 2.5 + 0.1 + 0.695]]
    simulator.ConstructAntenna(Model=model)
    simulator.ConstructWaveguidePort(PortNumber=waveguide[0], Orientation=waveguide[1], ExcitationDirection=waveguide[2], XRange=waveguide[3],
                                     YRange=waveguide[4], ZRange=waveguide[5])
    print(simulator.TimeDomainSolver(SteadyStateLimit=-40))

    # END
