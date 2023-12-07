from AntennaDesign.misc import RectangularMicrostripPatch, MicrostripTransmissionLine
from AntennaDesign.filing import Filing

if __name__ == '__main__':
    # Conventional antenna design dimensions
    RMSP = RectangularMicrostripPatch.RMPA(fr=2.4e9, er=3.55)
    RMSPDimensions = RMSP.get_rmsp_dimensions(__sub_h__=0.8e-3)
    MicrostripTransmissionLine.get_microstrip_transmission_dimensions(__freq__=2.4e9, __er__=3.55,
                                                                      __sub_h__=0.8e-3, __Zo__=50)
    filing = Filing(Directories=None, Debugging=True)

    filing.CreateDirectories(Directories=['\\root'])
    filing.CreateFile(Filename='\\root\\test1')
    filing.CreateFile(Filename='\\root\\test2')
    filing.DeleteFile(Filename='\\root\\test2')

    lists = [[[1, 2, 3], []], [[4, 5, 6], []], [[7, 8, 9], []]]
    filing.Save(Filename='\\root\\test1', Lists=lists)
    print(filing.Duplicate(Filename='\\root\\test1', List=[[1, 2, 3], []]))
