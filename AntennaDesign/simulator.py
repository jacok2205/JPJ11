"""
    Description:
    ------------
    Facilitates the bridge between python and CST Studio Suite; This module is a manager between python and CST Studio
    Suite.

    Global Variables:
    -----------------
    None.

    Imports:
    --------
    AntennaDesign.__init__:           The initialization module for the package.

    Notes:
    ------
    None.
"""

from AntennaDesign.__init__ import *

# The antenna format per layer is the following:
# [material name; component name; type (brick, cylinder); operation (add, subtract, none); z-range; geometry components]


class FineModel:
    def __init__(self, Debugging=False):

        # COM object(s)
        self.__cst__ = None
        self.__mws__ = None

        # Debugging (developer mode)
        self.__debugging__ = Debugging

    def Initialize(self, FrequencyRangeMin, FrequencyRangeMax, DimensionUnits='mm',
                   TemperatureUnits='Kelvin', FrequencyUnits='GHz', TimeUnits='ns',
                   VoltageUnits='V', CurrentUnits='A', ResistanceUnits='Ohm',
                   ConductanceUnits='Siemens', CapacitanceUnits='PikoF', InductanceUnits='nanoH'):
        # Open the CST Studio Suite software
        self.__cst__ = pycst.connect()
        # Open the 'Python_Control.cst' CST Studio Suite project.
        pycst.open_project(cst=self.__cst__, path=str(pkg_resources.files('AntennaDesign') /
                                                      'Python_Control\\Python_Control.cst'))
        # Get the active 3D window
        self.__mws__ = pycst.get_active_3d(cst=self.__cst__)
        # Set the simulation frequency range
        pycst.frequency_range(mws=self.__mws__, frange1=FrequencyRangeMin, frange2=FrequencyRangeMax)
        # Disable interactive mode, which enables scripting mode
        pycst.SetQuietMode(cst=self.__cst__)
        # Set CST Studio Suite units
        pycst.set_units(mws=self.__mws__, dimension=DimensionUnits, frequency=FrequencyUnits,
                        temperature=TemperatureUnits, time=TimeUnits,
                        voltage=VoltageUnits, current=CurrentUnits,
                        resistance=ResistanceUnits, conductance=ConductanceUnits,
                        capacitance=CapacitanceUnits, inductance=InductanceUnits)

    def TimeDomainSolver(self, SteadyStateLimit=-40):
        # Simulate the design
        pycst.time_domain_solver(mws=self.__mws__, steadyStateLimit=SteadyStateLimit)

        return self._get_results()

    def ConstructAntenna(self, Model=None):
        """
        Description:
        ------------
        Conducts a simulation given the Model parameter. Firstly, the geometry component list (last element of
        __layer__) is constructed in CST Studio Suite.

        Parameters:
        -----------
        __layer__:              list
                                A list of data of one individual. The format of the list is as follows:\n
                                [material name, solid name, component name, [z_min, z_max],
                                [[x1_min, x1_max, y1_min, y1_max], [x2_min, x2_max, y2_min, y2_max], ...,
                                [xn_min, xn_max, yn_min, yn_max]]].

        Return:
        -------
        Returns the S11 simulation results, in the form of [[freq_range], [S11_responses]], where the freq_range and
        S11_responses have the same number of elements.

        Notes:
        ------
        With regards to the xn, yn, and zn variables, xn is on the x-axis, yn is on the y-axis and zn is on the z-axis.
        [z_min, z_max] is the height range of the __layer__ parameter. The following __init__.py variable(s) are used:\n
        __mws__:    Active3D() Object
                    A reference to the current active project in CST Studio Suite.
        """

        if Model is None:
            raise Exception('<FineModel.ConstructAntenna: Model is of None type>')

        # Remove all components to begin with a new model
        self._remove_all(__component__=Model)

        # Construct layers
        # Each layer will be an array where each element is defined as:
        #   index           Element description
        #     0             str, layer material name
        #     1             str, layer component/solid name
        #     1             str, type (brick, cylinder)
        #     3             str, layer operation type
        #     4             list, layer height range --> [zmin, zmax]
        #     5             list, layer Model component blocks --> [x_min, x_max, y_min, y_max]
        # Layers
        __solid_names__ = []
        for __i__ in Model:
            if not __solid_names__.__contains__(__i__[0]):
                __solid_names__.append(__i__[1])
            pycst.load_material(mws=self.__mws__, name=__i__[0])

            if __i__[0] == 'Vacuum':
                __n__ = 'Slot'
                __from__ = 0
            else:
                __n__ = __i__[1]
                __from__ = 1
                pycst.brick(mws=self.__mws__, material=__i__[0], name=__n__, component=__i__[1],
                            xrange=__i__[-1][0][0: 2], yrange=__i__[-1][0][2: 4], zrange=__i__[2])

            for __j__ in range(__from__, len(__i__[-1])):

                pycst.brick(mws=self.__mws__, material=__i__[0], name=f'{__n__}_{__j__}', component=__i__[1],
                            xrange=__i__[-1][__j__][0: 2], yrange=__i__[-1][__j__][2: 4], zrange=__i__[2])

                if __i__[0] == 'Vacuum':
                    pycst.subtract(mws=self.__mws__, component1=f'{__i__[1]}', solid1=__i__[1],
                                       component2=f'{__i__[1]}', solid2=f'Slot_{__j__}')
                else:
                    pycst.add(mws=self.__mws__, component1=f'{__i__[1]}', solid1=f'{__i__[1]}',
                                  component2=f'{__i__[1]}', solid2=f'{__i__[1]}_{__j__}')

    def ConstructWaveguidePort(self, WaveguidePortPosition=None, TransmissionLineWidthMin=None,
                               TransmissionLineWidthMax=None, SubstrateThicknessMin=None,
                               SubstrateThicknessMax=None, AxisNormal='Y', ExcitationDirection='Positive',
                               ExtensionCoefficient=None):
        SubstrateThickness = abs(SubstrateThicknessMax - SubstrateThicknessMin)
        pycst.waveguide_port(mws=self.__mws__,
                             portNumber=1,
                             normal=AxisNormal,
                             xrange=[-ExtensionCoefficient * SubstrateThickness + TransmissionLineWidthMin,
                                     ExtensionCoefficient * SubstrateThickness + TransmissionLineWidthMax],
                             yrange=[WaveguidePortPosition, WaveguidePortPosition],
                             zrange=[SubstrateThicknessMin, SubstrateThicknessMax +
                                     ExtensionCoefficient * SubstrateThickness],
                             orientation=ExcitationDirection)

    def _get_results(self):

            __s11_result_vector__ = []
            __gain_result_vector__ = []

            try:
                # Retrieve the S11 results from the simulation
                __s11_result_vector__ = pycst.result_parameters(mws=self.__mws__)

            except Exception as __error__:
                if self.__debugging__:
                    print(__error__)

            try:
                # Retrieve the gain results from the simulation
                __gain_result_vector__ = pycst.result_parameters(mws=self.__mws__, parent_path=r'Tables\1D Results')

            except Exception as __error__:
                if self.__debugging__:
                    print(__error__)

            return [[__s11_result_vector__[0], __s11_result_vector__[2]],
                    [__gain_result_vector__[0], __gain_result_vector__[1]]]

    def _remove_all(self, __component__=None):
        """
        Description:
        ------------
        Deletes all solids that have a component name of __component__; This also deletes the component itself.

        Parameters:
        -----------
        __component__:      str
                            The individual to delete from the project. Only the third element is of interest as it
                            contains the component name per layer within the individual. Default is None.

        Return:
        -------
        None.

        Notes:
        ------
        The waveguide port is also deleted to accommodate for the next individual for CST Studio Suite simulation.
        The following __init__.py variable(s) are used:\n
        __mws__:    Active3D() Object
                    A reference to the current active project in CST Studio Suite.
        """

        if self.__mws__ is not None and __component__ is not None:

            for __i__ in __component__:
                pycst.delete_component(mws=self.__mws__, component=__i__[1])

            pycst.delete_waveguide_port(mws=self.__mws__, port_number='1')
