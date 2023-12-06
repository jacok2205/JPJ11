"""
    Description:
    ------------
    A module containing all variables that the package will use. Configure only the variables
    that does not contain a comment of 'leave alone'.

    CST Simulator Variable(s):
    --------------------------
    __freq_min__:                           float
                                            A positive float value that defines the minimum frequency for the CST Studio
                                            Suite to simulate in and is in Hertz. Default is 1.0 GHz.
    __freq_max__:                           float
                                            A positive float value that defines the maximum frequency for the CST Studio
                                            Suite to simulate in and is in Hertz. Default is 6.0 GHz.
                                            A positive float value that defines the height/thickness of the substrate
                                            and is in meters. Default is 0.5 x 10^(-3) mm or 0.5e-3 mm.
    __use_SMA_connector__:                  bool
                                            If True, the SMA connector will be used instead of the traditional
                                            rectangular waveguide port. If False, the traditional rectangular waveguide
                                            port will be used. Default is False.
    __normal__:                             str
                                            Sets the SMA cylinder/waveguide port perpendicular to a particular plane.
                                            Default is 'Y'.
    __port_number__:                        int
                                            The number of the SMA waveguide port. Default is 1.
    __orientation__:                        str
                                            The direction of propagation of the SMA waveguide port, and can either be
                                            'Positive' or 'Negative'. Default is 'Positive'.
    __coordinates__:                        str
                                            The method used to set the SMA waveguide port, and can either be 'Free',
                                            'Full Plane', or 'Use Picks'. Default is 'Free'.
    __material__:                           list
                                            For the SMA connector; a list of str type elements, where each element
                                            represents the name of the material that is going to be used for the
                                            construction of the SMA connector. Default is ['Copper (annealed)',
                                            'PTFE (loss free)'].
    __component__:                          str
                                            The component name of the SMA connector. Default is 'SMA_Connector'.

    Coarse Modeling Variable(s):
    ----------------------------
    __fr__:                                 float
                                            A positive float value that defines the resonant frequency and is in Hertz.
                                            Default is 2.40.
    __er__:                                 float
                                            A positive float value that defines the electrical permittivity of the
                                            substrate. Default is 3.55.
    __resolution__:                         float
                                            The size of each block within the grid, in millimeters. Default is 1.00.
    __Wm__:                                 float
                                            The maximum width of the antenna, excluding the connector and/or waveguide
                                            port. Default is 24.00.
    __Lm__:                                 float
                                            The maximum length of the antenna, excluding the connector and/or waveguide
                                            port. Default is 20.00.
    __Hs__:                                 float
                                            The height of the substrate. Default is 0.50.
    __Ct__:                                 float
                                            The thickness of the conductor. Default is 0.035 mm.
    __layers__:                             list
                                            A list of str type elements that describe what each layer is called.
                                            Default is ['Ground', 'Substrate', 'Patch'].
    __materials__:                          list
                                            A list of str type elements that describe the material used per layer.
                                            Default is ['Copper (annealed)', 'Rogers RO4003C (lossy)',
                                            'Copper (annealed)'].
    __Z_range_list__:                       list
                                            Each list element represents a list, where each element is the height
                                            minimum and height maximum per layer. Each tuple element must contain two
                                            elements of type str. Default is [[0.000, __Ct__],
                                            [__Ct__, __Ct__ + __Hs__], [__Ct__ + __Hs__, 2*__Ct__ + __Hs__]].
    __layer_modes__:                        list
                                            A list of str type elements that describe what mode the @func
                                            generate_layer() should execute for generating a layer. Default is
                                            ['random', 'solid', 'random'].
    __bias__:                               None or list
                                            A list that contains one of two formats, namely three lists as elements that
                                            define the range of conductive blocks to be added to the layer, where each
                                            element is represented as [[x1_min, x1_max, y1_min, y1_max],
                                            ..., [xn_min, xn_max, yn_min, yn_max]]. The default number of layers is
                                            three, where this variable is initialized as [[-Wm / 2, Wm / 2, -Lm / 2,
                                            -Lm / 2], None, [-1.10 / 2, 1.10 / 2, -Lm / 2, -Lm / 2 + 16.575]]. The
                                            second format are three "drawings" as elements, where a drawing should
                                            match the length and width of the desired dimensions of the antenna given
                                            that the resolution (block width and length) is 1.00 mm. The character use
                                            as a block must be a "@" character and a 'void' character, i.e. no block to
                                            be placed/added, must be a "-" character. For example, if Wm = 24 mm and
                                            resolution = 1.00 mm, then there should be 24 columns; if Lm = 20 mm and
                                            the resolution is the same as for Wm, then there should be 20 rows. This
                                            recommendation is needed for an accurate "drawing" as it is transferred
                                            into a set of geometry components, which will be used in CST Studio Suite.
                                            An example of a "drawing" is presented below, where each character
                                            represents one block and resolution is 1.00 mm. The example has 18 columns
                                            and 20 rows given that the resolution is 1.00 mm. The example can also be
                                            copied to experiment with. Note that pyhon docs does not display the example
                                            well.\n
    draw = [                                                # Width (x-axis)\n
                      ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],\n
                      ['-', '-', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '-', '-'],\n
                      ['-', '-', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '-', '-'],\n
                      ['-', '-', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '-', '-'],\n
                      ['-', '-', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '-', '-'],\n
                      ['-', '-', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '-', '-'],\n
                      ['-', '-', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '-', '-'],\n
                      ['-', '-', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '-', '-'],\n
                      ['-', '-', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '-', '-'],\n
                      ['-', '-', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '-', '-'],\n
                      ['-', '-', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '-', '-'], # Length (y-axis)\n
                      ['-', '-', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '-', '-'],\n
                      ['-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-'],\n
                      ['-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-'],\n
                      ['-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-'],\n
                      ['-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-'],\n
                      ['-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-'],\n
                      ['-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-'],\n
                      ['-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-'],\n
                      ['-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-']\n
            ]\n
    __exclude__:                            None or list
                                            Has the same concept as the __bias__ variable, except for the "drawing"
                                            concept. This list has a lower priority than the __bias__ variable, and
                                            ensures that the given range does not include any blocks given that the
                                            block exclusion is intentional and the  __bias__ variable is set up
                                            correctly. Each element is a layer, the default number of layers is three,
                                            where each element is represented as [[x1_min, x1_max, y1_min, y1_max], ...,
                                            [xn_min, xn_max, yn_min, yn_max]]. Default is [[None, None, [-5 * 1.10 / 2,
                                            5 * 1.10 / 2, -Lm / 2, -Lm / 2]]].
    __occurrence__:                         float
                                            A value between 0.0 and 1.0 that is used for the 'random' layer mode, to
                                            generate conductive blocks based on the @func numpy.random.choice()
                                            function. Default is [0.5, 0.5].

    Evolutionary Algorithm Variable(s) for Coarse Modeling:
    -----------------------------------
    __number_of_generations__:              int
                                            Performs the simulations for n number of generations. Default is 100.
    __population_size__:                    int
                                            The number of individuals that is required for the population pool.
    __number_of_offspring_per_generation__: int
                                            Defines the number of offspring to produce from selected parents. Default is
                                            6.
    __crossover_rate__:                     float
                                            A float value between 0.0 and 1.0 and is used to decide which parent pair
                                            will be used for the geometry list.
    __mutation_rate__:                      float
                                            A float value between 0.0 and 1.0, which defines the rate of mutation.
    __criteria__:                           list
                                            The list has the following structure:\n
                                            criteria = [int: number_of_bands, float: S11_minimum, list: band(s), list:
                                            tolerance(s)], where\n
                                            number_of_bands -  The number of desired bands from the CST simulation
                                                               results.\n
                                            S11_minimum     -  The number when a band is considered, when below this
                                                               value, which is typically -10 dB.\n
                                            band(s)         -  A list that contains the lower and upper frequency band
                                                               edges. For example, band(s) = [[f1_min, f1_max],
                                                               [f2_min, f2_max], ..., [fn_min, fn_max]].\n
                                            tolerance(s)    -  A list that must have the same number of elements as the
                                                               band(s) variable. It describes how much band tolerance
                                                               is allowed per defined band.1
    __boundaries__:                         list
                                            This defines the width and length of the antenna geometry, and are the
                                            absolute maximum values, in the x-direction and the y-direction. The height
                                            will be fixed as one cannot realize a unique height practically. Thus, the
                                            first element is the maximum width of the antenna substrate, the second
                                            element is the maximum length of the antenna substrate, the third element
                                            is the resolution to expand/contract the substrate with, and
                                            the 4th element is the port boundary list(s), which will be a simple x and
                                            y range in order for the conductive geometry not to be placed within this x
                                            and y range. All elements are positive float values. The format is:
                                            [max_substrate_width, max_substrate_length, resolution,
                                            [[x1_min, x2_min, y1_min, y1_max], ..., [xn_min, xn_max, yn_min, yn_max]]].
    __bricks_stay_connected__:              bool
                                            Used to activate the __brick_connected__() function from the SearchSpaceOptimizer.py module.
                                            Default is False.

    Coarse Modeling Variables Not To Be Manipulated:
    ------------------------------------------------
    __debugging__:                          bool
                                            A global variable used for debugging purposes. Leave alone.
    __pool__:                               list
                                            A list that contains all population individuals.
    __pool_index__:                         list
                                            Contains the indices of the fittest individuals.
    __offspring__:                          list
                                            A list that contains all offspring generated from SearchSpaceOptimizer.py.
    __pool_simulation__:                    list
                                            A list that contains all simulation results of population.
    __offspring_simulation__:               list
                                            A list that contains all the simulation results of each child in the
                                            offspring.
    __pool_fitness__:                       list
                                            A list that contains the fitness value results based on the
                                            __pool_simulation__ list.
    __offspring_fitness__:                  list
                                            A list that contains the fitness value results based on the
                                            __offspring_simulation__ list.
    __fig_path__:                           str
                                            The path to the figure file. Leave alone.
    __fig__:                                pyplot Figure Object
                                            Used to plot and save results as figures in .pdf format. Leave alone.
    __log_file__:                           file Object
                                            Used to log execution progress information about the package. Leave alone.
    __date_time__:                          datetime Object
                                            Used to keep and update the date and time stamp for various executions.
                                            Leave alone.
    __misc__:                               list
                                            Each element contains a message to log depending where in the execution path
                                            the package is. Leave alone.
    __generation_number__:                  str
                                            Keeps track of the latest generation and must be a digit str such as '0',
                                            '1', ..., 'n', where n is a positive natural number.
    __files__:                              list
                                            Each element is a path to a specific directory and file with a postfix of
                                            generation_number parameter.
    __File__:                               list
                                            A list that keeps all simulated individuals, which are unique, from the
                                            'explored_designs' file.

    Global Variables Not To Be Manipulated:
    ---------------------------------------
    __cst_project_path__:                   str
                                            The path to the Python_Control.cst project file.
    __cst__:                                None
                                            The variable is used when initialized to a CST Studio Suite instance.
    __mws__:                                None
                                            The variable is used when initialized to an active 3D instance from __cst__
                                            global variable.

    Imports:
    --------
    __init__:                               The initialization module for the package.

    Notes:
    ------
    None.
"""

from AntennaDesign.__init__ import *

"""----------------------------------- CST Simulator Variable(s) to Manipulate --------------------------------------"""
# Minimum frequency for CST Studio Suite to simulate in (in giga Hertz)
__freq_min__ = 1.0
# Maximum frequency for CST Studio Suite to simulate in (in giga Hertz)
__freq_max__ = 6.0
# If true, the SMA connector will be used as the waveguide, else a standard waveguide port will be used that is
# normal to the yz plane
__use_SMA_connector__ = True
__use_sma_connector__ = True
# The orientation of the SMA connector that is normal to an axis or plane, in this case the yz axis
__normal__ = 'Y'
__waveguide_axis_normal__ = 'Y'
# The number of the SMA waveguide port that is inserted at the end of the SMA connector
__port_number__ = 1
# The direction of the SMA signal to propagate
__waveguide_excitation_direction__ = 'Positive'
__orientation__ = 'Positive'
# The type of coordinates to configure on SMA connector as stipulated in CST Studio Suite
__coordinates__ = 'Free'
# A list of material that is to be used for the SMA connector
__material__ = ['Copper (annealed)', 'PTFE (loss free)']
# The component name of the SMA connector
__component__ = 'SMA_Connector'
__waveguide_name__ = 'SMA_Connector'
# Minimum frequency for CST Studio Suite to simulate in (in giga Hertz)

"""----------------------------------- Coarse Modeling Variable(s) to Manipulate ------------------------------------"""
# Antenna resonant frequency (in giga Hertz)
__fr__ = 2.4
# # Relative permittivity of antenna substrate
# __er__ = 3.55
# Grid resolution
__resolution__ = 1.0
__axis_step_size__ = 1.0
# Width of the antenna substrate
__Wm__ = 24.00
# Length of the antenna substrate
__Lm__ = 20.00
# Height of the antenna substrate
__Hs__ = 0.50
# Conductor thickness of the laminate (a substrate that has a conductive layer, typically copper).
__Ct__ = 0.035
# Names for each layer
__layers__ = ['Ground', 'Substrate', 'Patch']
# Materials to use for each layer
__materials__ = ['Copper (annealed)', 'Rogers RO4003C (lossy)', 'Copper (annealed)']
# Height ranges to use for each layer
__Z_range_list__ = [[0.00, __Ct__],
                    [__Ct__, __Hs__],
                    [__Ct__ + __Hs__, 2 * __Ct__ + __Hs__]]
# Layer construction modes to use for each layer
__layer_modes__ = ['custom', 'solid', 'custom']
# A list that ensures that conductive blocks are inserted according to the configured variable (__bias__)
__bias__ = [
        [                                                      # Width (x-axis)
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # Length
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],  # (y-axis)
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@'],
            ['@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@'],
            ['@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@'],
            ['@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@']
            ],
        None,
        [                                                      # Width (x-axis)
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '@', '-', '-', '-'],  # Length
            ['-', '-', '-', '@', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '@', '-', '-', '-'],  # (y-axis)
            ['-', '-', '-', '@', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '-', '-', '@', '@', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '@', '@', '-', '-', '-', '@', '@', '-', '-', '-', '@', '@', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '@', '@', '@', '@', '@', '-', '-', '-', '@', '@', '-', '-', '-', '@', '@', '@', '@', '@', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '@', '@', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
            ]
    ]
# A list to ensure that no conductive blocks are inserted, but will be overriden if the __bias__ is configured in
# such a way that is overlapping the __exclude__ variable.
__exclude__ = [
        None,
        None,
        None
    ]
# This is only valid for 'random' mode, but should still be initialized as a list of two elements that are probability
# values and must sum up to 1.0. This is used whether to insert a conductive block or not.
__occurrence__ = [0.5, 0.5]

"""------------------------------- Evolutionary Algorithm Variable(s) to Manipulate ---------------------------------"""
# Number of iterations to fulfil the number of desired generations
__number_of_generations__ = 100
# The desired number of individuals in the population
__population_size__ = 12
# The desired number of offspring to generate from the population
__number_of_offspring_per_generation__ = 6
# The crossover rate of the evolutionary algorithm and is a probability value from 0.0 to 1.0
__crossover_rate__ = 0.50
# The mutation rate of the evolutionary algorithm and is a probability value from 0.0 to 0.9999999. If 1.0 is
# inserted, the package will loop endlessly
__mutation_rate__ = 0.05
# The criteria (objective functions) for the evolutionary algorithm to determine a fitness value per individual.
# The formate is the following:
# [int: number of desired bands, list: [[freq1_min, freq1_max], ..., [freqn_min, freqn_max],
# [band_tolerance1, ..., band_tolerancen]]. Note that the number of lists in the third element must match the
# first element, as well as the fourth element must match the first element.
__criteria__ = [1, -10, [[2.33, 2.44]], [0.023]]
# Used for defining what space is not allowed to be mutated regardless. The format is the following:
# [float: maximum antenna width, float: maximum antenna length, float: grid resolution, list: [layer1, layer2, layer3]].
# Note that the last element has three lists, where each element within the list is a list of desired areas for the
# evolutionary algorithm not to mutate.
__boundaries__ = [__Wm__, __Lm__, __resolution__,
                  [
                      [
                          [-__resolution__, __resolution__, -__Lm__ / 2,
                           -__Lm__ / 2 + __resolution__]
                      ],
                      None,
                      [
                          [-1.1 / 2, 1.1 / 2, -__Lm__ / 2 + 5 * __resolution__,
                           -__Lm__ / 2 + 5 * __resolution__ + 10],
                          [-4 * __resolution__, 4 * __resolution__,
                           -__Lm__ / 2, -__Lm__ / 2 + 5 * __resolution__]
                      ]
                  ]]
# If the user wishes for the design to remain 'intact' or connected (in other words, for no conductive to have no
# neighbors), set the variable to True, else set it to False.
__bricks_stay_connected__ = True

"""---------------------------------- Coarse Modeling Variable(s) Not to Manipulate ---------------------------------"""
# For debugging the package
__debugging__ = False
# The generation population (leave alone)
__pool__ = []
# A list containing the indices of fittest individuals (leave alone)
__pool_index__ = []
# The offspring list (leave alone)
__offspring__ = []
# Generation simulation results (leave alone)
__pool_simulation__ = []
# Offspring simulation results (leave alone)
__offspring_simulation__ = []
# Generation fitness values based on __pool_simulation__ results (leave alone)
__pool_fitness__ = []
# Offspring fitness values based on __offspring_simulation__ results (leave alone)
__offspring_fitness__ = []
# Path(s) of file(s) (leave alone)
__coarse_model_fig_path__ = str(pkg_resources.files('AntennaDesign') /
                                'file_system\\coarse_model\\Generation Results In Figure Form\\fig_generation')
# pyplot figure (leave alone)
__fig__ = plt.figure(1)
# A file object for logging (leave alone)
__log_file__ = None
# To keep the time stamp (leave alone)
__date_time__ = None
# A list to log from (leave alone)
__misc__ = [
    f'"%d/%m/%Y %H:%M:%S"',                                                                                  # 0
    f'{__date_time__}',                                                                                      # 1
    f'Calling ',                                                                                             # 2
    f' called successfully',                                                                                 # 3
    f'file_system.generation_file() with mode = "new file"',                                                 # 4
    f'file_system.generation_file() with mode = "read"',                                                     # 5
    f'file_system.generation_file() with mode = "append"',                                                   # 6
    f'file_system.generation_file() with mode = "save"',                                                     # 7
    f'file_system.generation_file() with mode = "delete"',                                                   # 8
    f'cst_simulation.initialize()',                                                                          # 9
    f'__initialize_population__()',                                                                          # 10
    f'__get_parent_sim_results__()',                                                                         # 11
    f'__get_parent_fitness_results__()',                                                                     # 12
    f'__save_s11_as_figure__()',                                                                             # 13
    f'__initialize_offspring__()',                                                                           # 14
    f'__simulate_offspring__()',                                                                             # 15
    f'ga.evaluate_individual() {__number_of_offspring_per_generation__} times',                              # 16
    f'Selecting fittest individuals',                                                                        # 17
    f'Fittest individuals successfully selected',                                                            # 18
    f'file_system.generation_file() with increment_generation_number = True',                                # 19
    'Next generation number is {}\n\n',                                                                      # 20
    f'Fittest individuals successfully selected',                                                            # 21
    f'cst_simulation.set_boundaries()',                                                                      # 22
    f'cst_simulation.initialize()',                                                                          # 23
    f'MicrostripTransmissionLine.get_microstrip_transmission_dimensions()',                                  # 24
    f'Rounding the microstrip transmission line dimensions',                                                 # 25
    f'Microstrip transmission line successfully rounded',                                                    # 26
    f'file_system.generation_file() with mode = "get latest generation"',                                    # 27
    ' Updated file_system.generation_number to {}',                                                          # 28
    f'ga.initialize_population()',                                                                           # 29
    'Saving generation {} figure',                                                                           # 30
    'Generation {} figure saved successfully',                                                               # 31
    f'ga.select_parents()',                                                                                  # 32
    f'ga.crossover()',                                                                                       # 33
    f'ga.mutation()',                                                                                        # 34
    f'ga.evaluate_individual()',                                                                             # 35
    f'\t\t',                                                                                                 # 36
    f'\n\n',                                                                                                 # 37
    f'Deleted any files in "Generation Fitness Results" Directory',                                          # 38
    f'Deleted any files in "Generation Geometry" Directory',                                                 # 39
    f'Deleted any files in "Generation S11 Results" Directory',                                              # 40
    f'Done deleting any |S11| result files in "temp" Directory',                                             # 41
    f'Done Deleting any geometry files in "temp" Directory'                                                  # 42
]
# Keeps track of the latest generation number (leave alone)
__generation_number__ = '0'
# List that contains paths of directories (leave alone)
__files__ = [
    str(pkg_resources.files('AntennaDesign') /
        'file_system\\coarse_model\\Generation Geometry\\generation_geometry'),                              # 0
    str(pkg_resources.files('AntennaDesign') /
        'file_system\\coarse_model\\Generation S11 Results\\generation_S11_results'),                        # 1
    str(pkg_resources.files('AntennaDesign') /
        'file_system\\coarse_model\\Generation Fitness Results\\fitness_generation'),                        # 2
    str(pkg_resources.files('AntennaDesign')
        / 'file_system\\coarse_model\\temp\\temp_generation_geometry'),                                      # 3
    str(pkg_resources.files('AntennaDesign') /
        'file_system\\coarse_model\\temp\\temp_S11_results'),                                                # 4
    str(pkg_resources.files('AntennaDesign') /
        'file_system\\coarse_model\\log_file'),                                                              # 5
    str(pkg_resources.files('AntennaDesign') /
        'file_system\\coarse_model\\explored_designs'),                                                      # 6
    str(pkg_resources.files('AntennaDesign') /
        'file_system\\fine_model\\Epoch_Analysis'),                                                          # 7
    str(pkg_resources.files('AntennaDesign') /
        'file_system\\fine_model\\Datasets')
]
# Get all the explored designs from the 'explored_designs' file (leave alone)
__File__ = None

"""----------------------------------- Global Variables Not To Be Manipulated ---------------------------------------"""
# The file path to the 'Python_Control.cst' CST Studio Suite project (leave alone)
__cst_project_path__ = str(pkg_resources.files('AntennaDesign') / 'cst_interface\\Python_Control\\Python_Control.cst')
# A COM object that is referenced to the CST Studio Suite software (leave alone)
__cst__ = None
# An Active3D object that is referenced to the current active CST Studio Suite project (leave alone)
__mws__ = None

"""--------------------------------- Fine Modeling Variables Not To Be Manipulated ----------------------------------"""
# An array that will contain the input/output values of the neural network
__neuron_array__ = None
# An array with three dimensions that contains the weight values per neuron per link. The neural network is a
# fully connected neural network
__weights_array__ = None
# An array with 1 dimension that contains the average error made between the target and predictive values with the
# use of the derivative error function
__error_k__ = None
# An array with 2 dimensions that contains the average input realized by a layer neuron
__in_j__ = None
# An array with 2 dimensions that contains the average output realized by a layer neuron
__out_j__ = None
# The depth of the neural network structure, in other words the number of hidden layers between the input and output
# vectors
__d_s__ = 3    # 6
# The number of output neurons
__phi_k__ = 1   # 7
# A scaling factor that governs the architecture shape of the neural network, in this case it is a trapezoidal shape
__s_c__ = 1.5    # 1.3
# The alpha value, known as the leakage ratio for the LReLU activation function, and has the range of (0, 1)
__leakage_ratio__ = 0.3
# Batch size before learning
__N__ = 300
# Delta array
__delta__ = None
# Gradient array
__grad__ = None
# Mean array
__mean__ = None
# Variance array
__variance__ = None
# Loss array
__loss__ = None
# Beta 1
__Beta_1__ = 0.900
# Beta 2
__Beta_2__ = 0.999
# Epsilon
__epsilon__ = 1e-8
# Learning rate
__alpha__ = 0.1e-5    # 1e-4
