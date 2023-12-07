from AntennaDesign.misc import RectangularMicrostripPatch, MicrostripTransmissionLine

if __name__ == '__main__':
    # Conventional antenna design dimensions
    RMSP = RectangularMicrostripPatch.RMPA(fr=2.4e9, er=3.55)
    RMSPDimensions = RMSP.get_rmsp_dimensions(__sub_h__=1.5e-3)
    MicrostripTransmissionLine.get_microstrip_transmission_dimensions(__freq__=2.4e9, __er__=3.55,
                                                                      __sub_h__=1.5e-3, __Zo__=50)
