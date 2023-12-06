"""
    Description:
    ------------
    An evolutionary algorithm that has been adapted to work with individuals that are compatible for CST Studio Suite
    simulations. All the typical operators (population initialization, fitness evaluation, selection, crossover,
    and mutation) are used, but how they are executed is not typical.

    Global Variables:
    -----------------
    None.

    Imports:
    --------
    __init__:                   The initialization module for the package.
    __config__:                 Global variables to access from, according to what was configured from the user.

    Notes:
    ------
    None.
"""

from AntennaDesign.__init__ import *


class SearchSpaceOptimizer:
    def __init__(self, PopulationSize=12, NumberOfOffspring=6, CrossoverRate=0.5,
                 MutationRate=0.05, modelGeometry=None, Filing=None, Directory=None, Debugging=False):
        if modelGeometry is None:
            raise Exception('<SearchSpaceOptimizer: __init__: AntennaGeometry and/or cstSimulation objects are '
                            'of type None>')
        # The first element is the directory, where the rest of the elements are the file names that will be used
        # by this class
        if Directory is None:
            self.__directory__ = ['\\SSO\\']
        else:
            self.__directory__ = ['\\SSO\\' + Directory + '\\']
        self.__files__ = [self.__directory__[0] + 'Temp', self.__directory__[0] + 'Explored',
                          self.__directory__[0] + 'Best', self.__directory__[0] + 'Fitness']
        self.__population_size__ = PopulationSize
        self.__number_of_offspring__ = NumberOfOffspring
        self.__crossover_rate__ = CrossoverRate
        self.__mutation_rate__ = MutationRate
        self.__debugging__ = Debugging
        self.__pool__ = []
        self.__pool_fitness__ = []
        self.__pool_index__ = []
        self.__offspring__ = []
        self.__offspring_fitness__ = []

        # Class objects
        self.__individual__ = modelGeometry
        self.__filing__ = Filing

        # Create directories
        self.__filing__.CreateDirectories(Directories=self.__directory__)

        # Initialize the population
        self._initialize_population()

    def Search(self, SearchTimeMinutes=60, GainFitness=False, Convergence=None):

        # Begin timer
        __start__ = time.time() / 60

        for __i__ in self.__files__:
            self.__filing__.CreateFile(Filename=__i__)

        # Initializing generation n's pool
        self._populate_simulation_results(Pool=True)

        # Attempt to retrieve the offspring from the Temp file
        self.__offspring__ = self.__filing__.Read(Filename=self.__files__[0])

        # The temp file does not exist or is corrupt
        if isinstance(self.__offspring__, int) and self.__offspring__ == -1 or \
                isinstance(self.__offspring__, list) and len(self.__offspring__) != self.__number_of_offspring__:
            self._generate_offspring()

        if len(self.__pool_fitness__) == 0:
            self.__pool_fitness__ = [self._evaluate_individual(__simulation_result__=__i__[1])
                                     for __i__ in self.__pool__]

        while True:
            __loop_time__ = time.time() / 60

            # Simulate remaining offspring to simulate
            self._populate_simulation_results(Pool=False)

            # Evaluate offspring
            self.__offspring_fitness__ = [self._evaluate_individual(__simulation_result__=__i__[1])
                                          for __i__ in self.__offspring__]

            # Select which individuals between the pool and offspring to choose from according to their
            # fitness values. The selection will be based on the strength of their fitness values in the
            # form of a probability value
            __new_generation__ = []
            if GainFitness:
                __pool_fitness__ = [__i__[0] + __i__[1] for __i__ in self.__pool_fitness__]
                __offspring_fitness__ = [__i__[0] + __i__[0] for __i__ in self.__offspring_fitness__]
            else:
                __pool_fitness__ = [__i__[0] for __i__ in self.__pool_fitness__]
                __offspring_fitness__ = [__i__[0] for __i__ in self.__offspring_fitness__]

            for __i__ in range(self.__population_size__):

                __min_at_pool__ = True

                if min(__pool_fitness__) < min(__offspring_fitness__):
                    __min__ = __pool_fitness__.index(min(__pool_fitness__))
                elif min(__offspring_fitness__) < min(__pool_fitness__):
                    __min__ = __offspring_fitness__.index(min(__offspring_fitness__))
                    __min_at_pool__ = False
                else:
                    __pool__ = np.random.choice([True, False])
                    if __pool__:
                        __min__ = __pool_fitness__.index(min(__pool_fitness__))
                    else:
                        __min__ = __offspring_fitness__.index(min(__pool_fitness__))
                        __min_at_pool__ = False

                if __min_at_pool__:
                    __new_generation__.append(self.__pool__[__min__])
                    __pool_fitness__[__min__] = 9e12

                else:
                    __new_generation__.append(self.__offspring__[__min__])
                    __offspring_fitness__[__min__] = 9e12

            # Update pool to new generation
            self.__pool__ = __new_generation__

            # Save the new generation as the best in Best file
            self.__filing__.Save(Filename=self.__files__[2], Lists=self.__pool__)

            # Generate new offspring
            self._generate_offspring()

            print(f'Sweep completed in {round(time.time() / 60 - __loop_time__, 2)} minutes')

            if Convergence is None and (time.time() / 60 - __start__) < SearchTimeMinutes:
                break
            elif Convergence is not None and GainFitness is True and \
                    self.__offspring_fitness__[0][0] + self.__offspring_fitness__[0][1] <= Convergence:
                break
            elif Convergence is not None and GainFitness is False and \
                    self.__offspring_fitness__[0][0] <= Convergence:
                break
            else:
                pass

    def _generate_offspring(self):
        # Delete content in Temp file
        self.__filing__.DeleteContent(Filename=self.__files__[0])
        # Evaluate pool
        self.__pool_fitness__ = [self._evaluate_individual(__simulation_result__=__i__[1])
                                 for __i__ in self.__pool__]
        # Save the evaluation results (fitness values)
        self.__filing__.Append(Filename=self.__files__[3], List=self.__pool_fitness__)
        # Select parents
        self._select_parents()
        # Crossover
        self._crossover()
        # Mutation
        self._mutation()
        # Save the offspring in temp file
        self.__filing__.Save(Filename=self.__files__[0], Lists=self.__offspring__)

    def _populate_simulation_results(self, Pool=True):
        if Pool:
            __pool__ = self.__pool__
            __file__ = self.__files__[2]
        else:
            __pool__ = self.__offspring__
            __file__ = self.__files__[0]

        # Simulate remaining offspring to simulate
        for __i__ in range(len(__pool__)):
            if not len(__pool__[__i__][1]):
                __temp__ = self.__filing__.Duplicate(Filename=self.__files__[1], List=__pool__[__i__][0])
                if not isinstance(__temp__, list):
                    self.__pool__[__i__][1] = \
                        self.__individual__.SimulateModel(Parameters=__pool__[__i__][0][0],
                                                          XYOffset=__pool__[__i__][0][1])
                    self.__filing__.Append(Filename=self.__files__[1], List=__pool__[__i__])
                else:
                    __pool__[__i__][1] = __temp__
                self.__filing__.Save(Filename=__file__, Lists=__pool__)

        if Pool:
            self.__pool__ = __pool__
        else:
            self.__offspring__ = __pool__

    def _initialize_population(self):

        """
        Description:
        ------------
        Generates a population from the given rules and information provided from the __config__ module.

        Parameters:
        -----------
        None.

        Return:
        -------
        None.

        Notes:
        ------
        Chromosome format\n
        Type: list

        Individual layout:      list
                                [layer0, layer1, layer2].
        layer_n:                list
                                [material_name, solid_name, component_name, height_range/z_range, geometry_list].
        material_name:          str
                                Name of material from CST Studio Suite material library.
        solid_name:             str
                                Name of solid that will inherit the component_name variable.
        component_name:         str
                                Name of component that solid_name belongs to.
        height_range/z_range:   list
                                A 1-D array with only two elements, the height minimum and the height maximum of
                                layer_n.
        geometry_list:          list
                                A 2-D array, where each element contains a 1-D array of the [x_min, x_max, y_min, y_max]
                                values per solid. In other words, each element of xy_range contains a 1-D array of solid
                                dimensions information, which are the xrange and yrange values in the form as
                                [x_min, x_max, y_min, y_max].

        """

        __temp__ = self.__filing__.Read(Filename=self.__files__[2])

        if not isinstance(__temp__, list) and __temp__ == -1 or isinstance(__temp__, list) and \
                len(__temp__) != self.__population_size__:
            self.__pool__ = []

            for __i__ in range(self.__population_size__):
                # Create individual.
                self.__pool__.append([[[], []], []])

                # Populate initial parameters
                for __j__ in self.__individual__.__parameter__['value']:
                    self.__pool__[-1][0][0].append(__j__)

                # Get random x/y offset
                self.__pool__[-1][0][1] = self.__individual__.GenerateRandomOffsets()

            self.__filing__.Save(Filename=self.__files__[2], Lists=self.__pool__)

        else:
            self.__pool__ = __temp__

    def _evaluate_individual(self, __simulation_result__=None):
        """
        Description:
        ------------
        THE FUNCTIONS EXPECTS A LIST OF LISTS, WHERE THE FIRST LIST IS THE S11 RESPONSES AND THE LAST LIST IS THE
        GAIN RESPONSES. BOTH LISTS HAVE THEIR OWN FREQUENCY RANGES
        Calculates the fitness value of a given individual with the configured self.__individual__.__objective__ variable. The
        desired fitness function is to allow for the individual's fitness value to ideally be 0.0. This happens when the
        edge bands are subtracted by the desired band edges, which will guide the evolutionary algorithm to converge to
        0.0. This can be almost described as a 'gradient descent'. Thus, the 'sweet' spot for the fitness value is  0.0.
        A bias value will be added for the condition where the fitness value appears good, but has one or more bands than
        the desired number of band(s). Thus, the bias will simply be the difference between the actual number of bands with
        the desired number of bands.

        Parameters:
        -----------
        __S11_result__:     list
                            A list with a format of [[freq elements], [S11 elements]] and is from the CST simulation
                            results.

        Return:
        -------
        Returns a fitness value of type float that is calculated from the given individual's __S11_result__ list and is
        always positive.

        Notes:
        ------
        None.
        """

        __s11_fitness__ = 0.0                                   # The total fitness value for s11 result
        __gain_fitness__ = 0.0                                  # The total fitness value for gain result
        __index__ = 0                                           # Index for iterating through the individual's results

        # Evaluation of return loss results
        __s11_freq__ = __simulation_result__[0][0]              # List of frequency values, in ascending order
        __s11__ = __simulation_result__[0][1]                   # List of |S11|, in dB, values from the __freq__ inputs
        __number_of_bands__ = []                                # List which will collect multiple bands that are under
                                                                # the specified S11 value from
                                                                # self.__individual__.__objective__[1]
        # Evaluation of gain responses over a specified frequency range
        __gain_freq__ = __simulation_result__[1][0]             # Frequency range specified for the gain responses
        __gain__ = __simulation_result__[1][1]                  # The gain responses over the specified frequency range
        __target_gain__ = self.__individual__.__objective__[4]  # The gain that should be met, or higher

        # Determine the number of actual bands under the specified self.__individual__.__objective__[1] variable
        while __index__ < len(__s11__):

            # If a lower edge frequency is found that is lower than the specified
            # self.__individual__.__objective__[1] variable
            if __s11__[__index__] <= self.__individual__.__objective__[1]:
                # Append possible band n
                __number_of_bands__.append([])

                # Append lower edge frequency and S11 value associated with the lower edge frequency of band n
                __number_of_bands__[-1].append(__s11_freq__[__index__])
                __number_of_bands__[-1].append(__s11__[__index__])

                # Determine the upper edge frequency of band n by incrementing __index__ until the upper edge
                # frequency has been found
                while (__index__ + 1) < len(__s11__) and __s11__[__index__ + 1] < \
                        self.__individual__.__objective__[1]:
                    __index__ += 1

                # Append upper edge frequency and S11 value associated with the upper edge frequency
                __number_of_bands__[-1].append(__s11_freq__[__index__])
                __number_of_bands__[-1].append(__s11__[__index__])
            __index__ += 1

        # If no bands were found under the condition of self.__individual__.__objective__[1] variable. This is
        # considered as a solution which is the worst solution
        if len(__number_of_bands__) == 0:
            for __i__ in self.__individual__.__objective__[2]:
                __s11_fitness__ += abs(__i__[0] + __i__[1]) * 9e9

        # If at least one band has been found under the condition of self.__individual__.__objective__[1]
        else:
            # Iterate through the band(s) that were found
            for __i__ in range(len(__number_of_bands__)):

                # Collect all fitness values from current band that was found and choose the fitness value that is
                # the lowest, which is the best fitness value possible for the number of specified bands in
                # self.__individual__.__objective__[0]
                __fitness_temp__ = []
                for __j__ in range(len(self.__individual__.__objective__[2])):
                    __fitness_temp__.append(
                        abs(__number_of_bands__[__i__][0] - self.__individual__.__objective__[2][__j__][0]) +
                        abs(__number_of_bands__[__i__][2] - self.__individual__.__objective__[2][__j__][1])
                    )

                    # If any of the band edges are within the self.__individual__.__objective__[2] band(s) edges
                    # (+/- the allowed band edge tolerance from self.__individual__.__objective__[3]), divide the
                    # current band's minimum S11 value, which is the band's resonant frequency, with the above
                    # append operation. All is checked with the tolerance element from
                    # self.__individual__.__objective__[3][__j__]. For the __S11_min__ value, the absolute value
                    # will be taken
                    __lower_freq__ = __number_of_bands__[__i__][0]
                    __upper_freq__ = __number_of_bands__[__i__][2]

                    if (self.__individual__.__objective__[2][__j__][0] *
                        (1 - self.__individual__.__objective__[3][__j__])) <= __lower_freq__ <= \
                            (self.__individual__.__objective__[2][__j__][0] *
                             (1 + self.__individual__.__objective__[3][__j__])) and \
                            (self.__individual__.__objective__[2][__j__][1] *
                             (1 - self.__individual__.__objective__[3][__j__])) <= \
                            __upper_freq__ <= (self.__individual__.__objective__[2][__j__][1] *
                                               (1 + self.__individual__.__objective__[3][__j__])):

                        __S11_min__ = \
                            abs(min(__s11__[__s11_freq__.index(__lower_freq__): __s11_freq__.index(__upper_freq__)]))
                        __fitness_temp__[-1] /= __S11_min__

                    else:
                        continue

                # Update fitness value by adding the fitness value with the best possible fitness value from
                # fitness_temp list, where the best fitness value is 0.0.
                __s11_fitness__ += min(__fitness_temp__)

        # Add a possible bias. Note that if the __number_of_bands__ has the same value as
        # self.__individual__.__objective__[0], there will not be any bias to add to the fitness with
        __s11_fitness__ += abs(self.__individual__.__objective__[0] - len(__number_of_bands__))

        # Evaluation of gain results
        # The more positive and larger the __gain_fitness__ value is, the better
        for __i__ in range(len(self.__individual__.__objective__[2])):
            __temp__ = []
            for __j__ in range(len(__gain_freq__)):
                if self.__individual__.__objective__[2][__i__][0] <= __gain_freq__[__j__] <= \
                        self.__individual__.__objective__[2][__i__][1]:
                    __temp__.append(__gain__[__j__])
            if len(__temp__) > 1:
                __average_gain__ = sum(__temp__) / len(__temp__)
                __sigma__ = [(__j__ - __average_gain__) ** 2 for __j__ in __temp__]
                __sd__ = (sum(__sigma__) / len(__temp__)) ** 0.5
                __lowest_gain__ = __average_gain__ - 5 * __sd__
                if (__lowest_gain__ - __target_gain__[__i__]) > 0:
                    __gain_fitness__ += 1 / __lowest_gain__
                elif (__lowest_gain__ - __target_gain__[__i__]) < 0:
                    __gain_fitness__ += abs(__lowest_gain__)
                else:
                    __gain_fitness__ += 1
        # [1, -10, [[2.33, 2.44]], [0.023], [g0, g1]]

        # Return the total fitness value from the given individual CST simulation results, in the form of
        # s11 fitness and gain fitness. Remember that the fitness value is best when 0.0.
        return __s11_fitness__, __gain_fitness__

    def _select_parents(self):
        """
        Description:
        ------------
        Selects parent pairs for producing offspring. The fitter the parent, the more likely that parent will be
        selected for breeding.

        Parameters:
        ----------
        None.

        Return:
        ------
        None.

        Notes:
        ------
        None.
        """

        # Remember, the closer the fitness result is to 0.0, the better. Thus, the probability should be such that:
        # p[True, False] = [1 - fitness_result[n]], fitness_result[n]]
        # The above is true since a small fitness value is, in this case, better than a large fitness value. The 'True'
        # and 'False' values are to portray if the individual is going to be selected (True) or not (False).

        # Get the sum of the __config__.__pool_fitness__ list.
        __total_fitness__ = 0.0
        for __i__ in self.__pool_fitness__:
            __total_fitness__ += (__i__[0] + __i__[1])
        if __total_fitness__ == 0.0:
            __total_fitness__ = 1.0
        self.__pool_index__ = []                                    # A list that will contain all the indices of the
                                                                    # selected parents.
        __tries__ = 999                                             # Number of tries set for selecting a parent. This is
                                                                    # when there are fewer parents than there are number
                                                                    # of desired offspring.
        __index_select_parents__ = 0                                # An index used to iterate through the
                                                                    # __config__.__pool_fitness__ list.

        # Number of parents to insert in the __config__.__pool_index__ list in for producing offspring. Note that 2 is
        # multiplied with the __config__.__number_of_offspring_per_generation__ variable to make up a pair per offspring.
        __number_of_parents__ = self.__number_of_offspring__ * 2

        while __number_of_parents__ > 0:
            __value__ = (self.__pool_fitness__[__index_select_parents__][0] +
                         self.__pool_fitness__[__index_select_parents__][1]) / __total_fitness__

            __select__ = np.random.choice([True, False], p=[1 - __value__, __value__])

            # All selections must be unique. No parent, in this process, is able to mate with itself
            if __select__ and not self.__pool_index__.__contains__(__index_select_parents__):
                self.__pool_index__.append(__index_select_parents__)
                __number_of_parents__ -= 1

            # If there are fewer parents to choose from than there are number of desired offspring, clone the same parent.
            # This happens when the user incorrectly configured the __config__ variable(s) or a special case happened.
            else:
                __tries__ -= 1

                # If the number of __tries__ are exhausted, append the same parent
                if __tries__ < 1:

                    self.__pool_index__.append(__index_select_parents__)
                    __number_of_parents__ -= 1
                    __tries__ = 999

            # Increment __index__ and mod it with the number of elements in __config__.__pool_fitness__
            __index_select_parents__ = (__index_select_parents__ + 1) % len(self.__pool_fitness__)

    def _crossover(self):
        """
        Description:
        ------------
        Performs a crossover on the pool of selected parents. This is the initial stage of producing offspring.

        Parameters:
        ----------
        None.

        Return:
        ------
        None.

        Notes:
        ----
        Every element in the __config__.__pool_index__ variable is an individual (parent).
        """

        self.__offspring__ = []                     # The offspring list to populate given the
                                                    # self.__number_of_offspring__ variable.

        # Loop for the number of required offspring to generate
        for __i__ in range(self.__number_of_offspring__):

            __index__ = __i__ % len(self.__pool__)

            # Append a fresh list, which is a new child that has no chromosomes yet.
            self.__offspring__.append([[[__j__ for __j__ in self.__pool__[__index__][0][0]], []], []])

            # Loop until x and y offsets are gathered (this is the core to the crossover function)
            __offset__ = [None, None]
            while __offset__[0] is None or __offset__[1] is None:
                __choose__ = np.random.choice(self.__pool_index__)
                if np.random.choice([True, False]) and __offset__[0] is None:
                    __offset__[0] = self.__pool__[__choose__][0][1][0]
                __choose__ = np.random.choice(self.__pool_index__)
                if np.random.choice([True, False]) and __offset__[1] is None:
                    __offset__[1] = self.__pool__[__choose__][0][1][1]

            self.__offspring__[-1][0][1] = __offset__

            # Shuffle indices in self.__pool_index__ for fair offspring generation
            random.shuffle(self.__pool_index__)

    def _mutation(self):
        """
        Description:
        ------------
        Performs mutation(s) on the received offspring. The mutation is able to increase/decrease a child's substrate
        width and/or length, swap a child's geometry component, shift a child's geometry component, remove a geometry
        component if the geometry component is out of bounds of the child's substrate, or add a geometry component. The
        __config__.__boundaries__[3] list is strictly avoided from any mutations.

        Parameters:
        -----------
        None.

        Return:
        -------
        Returns the offspring with possible mutation(s).

        Notes:
        ------
        None.
        """

        # Individual for loop
        for __i__ in range(len(self.__offspring__)):
            for __j__ in range(len(self.__offspring__[__i__][0][1])):
                if np.random.choice([True, False], p=[self.__mutation_rate__, 1 - self.__mutation_rate__]):
                    __choice__ = [True, False]
                    np.random.shuffle(__choice__)

                    if np.random.choice(__choice__):
                        self.__individual__.IncrementParameterValue(
                            Parameters=self.__offspring__[__i__][0][0],
                            XYOffsets=self.__offspring__[__i__][0][1],
                            Index=__j__,
                            FocusOnParameters=False
                        )

                    else:
                        self.__individual__.DecrementParameterValue(
                            Parameters=self.__offspring__[__i__][0][0],
                            XYOffsets=self.__offspring__[__i__][0][1],
                            Index=__j__,
                            FocusOnParameters=False
                        )
