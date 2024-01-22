# The initialization module for the package AntennaDesign, which will be a list of common public libraries,
# see AntennaDesign.__init__ for more information
from AntennaDesign.__init__ import *


class SearchSpaceOptimizer:
    """
    Description:
    ------------
    Based on the genetic algorithm, this class uses the defined antenna geometry, filing, and simulator to explore for
    the best possible solution.

    Attributes:
    -----------
    __directory__:                  str
                                    A string representing the directory for the instance of this class to store results.
    __files__:                      list
                                    A list that contains file names to create, write, and read from. The following files
                                    are used: 'Temp', 'Explored', 'Best', and 'Fitness'.
    __population_size__:            int
                                    The population size defined by the user.
    __number_of_offspring__:        int
                                    The number of offspring to generate per generation.
    __crossover_rate__:             float
                                    The crossover rate for the crossover operation of the genetic algorithm and is in
                                    the range of 0.0 to 1.0.
    __mutation_rate__:              float
                                    The mutation rate for the mutation operation of the genetic algorithm and is in
                                    the range of 0.0 to 1.0.
    __rounding__:                   int
                                    Used for rounding the parameter values per individual.
    __pool__:                       list
                                    A list that contains all the individuals of the population for the current
                                    generation. Both the parameter values/combination and simulation results are stored
                                    per individual.
    __pool_fitness__:               list
                                    A list that contains the fitness values, after evaluation of each individual, of
                                    the current generation.
    __pool_index__:                 list
                                    A list that contains the indices, from the __pool__ attribute, of the fittest
                                    individuals from the current generation.
    __offspring__:                  list
                                    A list that contains all the children of the offspring generated from the current
                                    generation.
    __offspring_fitness__:          list
                                    A list that contains the fitness values, after evaluation of each child, of the
                                    current generation.
    __individual__:                 ModelGeometry
                                    The geometry of the antenna model defined by the user.
    __filing__:                     Filing
                                    Used for writing, reading, appending, deleting data for later use.
    __debugging__:                  bool
                                    For debugging purposes (developer mode).

    Methods:
    --------
    __init__(PopulationSize=12, NumberOfOffspring=6, CrossoverRate=0.5, MutationRate=0.05,
                 modelGeometry=None, Filing=None, Directory=None, Rounding=None, Debugging=False):
                                    The constructor of the class, where the PopulationSize, NumberOfOffspring,
                                    CrossoverRate, MutationRate, modelGeometry, and Rounding must be given as
                                    arguments. The genetic algorithm is initialized if all required parameters are
                                    correct.
    Search(SearchTimeMinutes=60, Convergence=None):
                                    Used for initiating the genetic algorithm to begin the search for an optimal
                                    solution.
    _generate_offspring():
                                    Generates new offspring given the process of the genetic algorithm
    _populate_simulation_results(Pool=True):
                                    Simulates all the individuals/children in the population/offspring.
    _initialize_population():
                                    Initializes the population given the parameters that have been defined by the user.
    _evaluate_individual(__simulation_result__=None):
                                    The fitness function of the genetic algorithm, which only evaluates the return loss
                                    and gain responses for this current build.
    _get_bands(__simulation_result__=None):
                                    Determines the band(s) of the current simulation result, either from the individual
                                    or the child of concern.
    _select_parents():
                                    Selects the parents for generating offspring. The better the fitness value an
                                    individual has, the better the chance it will be selected for breeding.
    _crossover():
                                    Performs a crossover given the selected parents. Note that the crossover is
                                    dependent of the crossover rate defined by the user.
    _mutation():
                                    Performs a possible mutation per child before each child is simulated and evaluated.

    Notes:
    ------
    None.
    """

    def __init__(self, PopulationSize=12, NumberOfOffspring=6, CrossoverRate=0.5, MutationRate=0.05,
                 modelGeometry=None, Filing=None, Directory=None, Rounding=None, Debugging=False):
        """
        Description:
        ------------
        The constructor of the ModelGeometry class. It expects five parameters as arguments, specifically the
        PopulationSize, NumberOfOffspring, CrossoverRate, MutationRate, modelGeometry, and Rounding. The population
        is then initialized either as a new first generation, if no history has been found in the Filing directory,
        or extracts the individuals from the Best file.

        Parameters:
        -----------
        PopulationSize:             int
                                    The size of the population for the genetic algorithm.
        NumberOfOffspring:          int
                                    The number of offspring to generate per generation.
        CrossoverRate:              float
                                    The crossover rate between two parents and has the range of 0.0 to 1.0.
        MutationRate:               float
                                    The mutation rate that a child will undergo mutation and has the range of 0.0 to
                                    1.0.
        modelGeometry:              ModelGeometry
                                    The geometry of the antenna defined by the user for the genetic algorithm to exploit
                                    given the parameters defined by the user.
        Filing:                     Filing
                                    The results that are stored using the Filing class for reading, writing, appending,
                                    and deleting files.
        Directory:                  str
                                    Should the user wish to define a unique directory for his/her current antenna
                                    geometry, this should be named something meaningful.
        Rounding:                   int
                                    The rounding that needs to be defined by the user. 0 represents no decimal places,
                                    1 represents one decimal place, etcetera. This is used from the ModelGeometry
                                    class.
        Debugging:                  bool
                                    For debugging purposes (developer mode).

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        if modelGeometry is None:
            raise Exception('<SearchSpaceOptimizer: __init__: AntennaGeometry and/or cstSimulation objects are '
                            'of type None>')
        if Filing is None:
            raise Exception('<SearchSpaceOptimizer: __init__: Filing is of None type, it must be of Filing type>')
        if Rounding is None:
            raise Exception('<SearchSpaceOptimizer: __init__: Rounding is of None type, please specify a rounding '
                            'number>')

        # The first element is the directory, where the rest of the elements are the file names that will be used
        # by this class
        if Directory is None:
            self.__directory__ = ['\\SSO\\']
        else:
            self.__directory__ = ['\\SSO\\' + Directory + '\\']

        # Files that will be used by the genetic algorithm
        self.__files__ = [self.__directory__[0] + 'Temp', self.__directory__[0] + 'Explored',
                          self.__directory__[0] + 'Best', self.__directory__[0] + 'Fitness']

        # Genetic algorithm parameters
        self.__population_size__ = PopulationSize
        self.__number_of_offspring__ = NumberOfOffspring
        self.__crossover_rate__ = CrossoverRate
        self.__mutation_rate__ = MutationRate
        self.__rounding__ = Rounding

        # Generation parameters
        self.__pool__ = []
        self.__pool_fitness__ = []
        self.__pool_index__ = []
        self.__offspring__ = []
        self.__offspring_fitness__ = []

        # Class objects
        self.__individual__ = modelGeometry
        self.__filing__ = Filing

        # For debugging (developer mode)
        self.__debugging__ = Debugging

        # Create directories
        self.__filing__.CreateDirectories(Directories=self.__directory__)

        # Create file(s)
        for __i__ in self.__files__:
            self.__filing__.CreateFile(Filename=__i__)

        # Initialize the population
        self._initialize_population()

    def Search(self, SearchTimeMinutes=60, Convergence=None):
        """
        Description:
        ------------
        Begins the genetic algorithm search. The user must define the duration, in minutes, that the genetic algorithm
        will be searching for. Additionally, the user may also define the convergence criteria, which will simply be
        the convergence value of the best fitness from the population.

        Parameters:
        -----------
        SearchTimeMinutes:          float
                                    The amount of time the genetic algorithm is allowed to search (in minutes).
        Convergence:                float
                                    The convergence value that will stop the search if met.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        # Begin timer
        __start__ = time.time() / 60

        # Get simulation results for the pool (if required)
        self._populate_simulation_results(Pool=True)

        # Attempt to retrieve the offspring from the Temp file
        self.__offspring__ = self.__filing__.Read(Filename=self.__files__[0])

        # The temp file does not exist or is corrupt, generate a new set of offspring
        if not isinstance(self.__offspring__, list) or (isinstance(self.__offspring__, list) and
                                                        len(self.__offspring__) != self.__number_of_offspring__):
            self._generate_offspring()

        # Evaluate pool fitness if the list is not the same size as the defined self.__pool__
        if len(self.__pool_fitness__) != len(self.__pool__):
            self.__pool_fitness__ = [self._evaluate_individual(__simulation_result__=__i__[1])
                                     for __i__ in self.__pool__]

        while True:
            # Timer for noting the duration of time taken per generation
            __loop_time__ = time.time() / 60

            # Simulate remaining offspring that require simulation(s)
            self._populate_simulation_results(Pool=False)

            # Evaluate offspring
            self.__offspring_fitness__ = [self._evaluate_individual(__simulation_result__=__i__[1])
                                          for __i__ in self.__offspring__]

            # Select which individuals between the pool and offspring to choose from according to their
            # fitness values; the lower the fitness value the better
            __new_generation__ = []
            __chosen_index__ = []
            __best_minimum__ = self.__pool_fitness__[0]

            for __i__ in range(self.__population_size__):

                __new_individual__ = False
                __j__ = 0

                while __j__ < len(self.__offspring_fitness__) and not __new_individual__:
                    if self.__offspring_fitness__[__j__][0] < self.__pool_fitness__[__i__][0] and \
                            self.__offspring_fitness__[__j__][1] <= self.__pool_fitness__[__i__][1] and \
                            not __chosen_index__.__contains__(__j__):
                        __chosen_index__.append(__j__)
                        __new_generation__.append(copy.deepcopy(self.__offspring__[__j__]))
                        __new_individual__ = True

                        if self.__offspring_fitness__[__j__][0] < __best_minimum__[0] and \
                                self.__offspring_fitness__[__j__][1] <= __best_minimum__[1]:
                            __best_minimum__ = self.__offspring_fitness__[__j__]

                    elif self.__offspring_fitness__[__j__][0] <= self.__pool_fitness__[__i__][0] and \
                            self.__offspring_fitness__[__j__][1] < self.__pool_fitness__[__i__][1] and \
                            not __chosen_index__.__contains__(__j__):
                        __chosen_index__.append(__j__)
                        __new_generation__.append(copy.deepcopy(self.__offspring__[__j__]))
                        __new_individual__ = True

                        if self.__offspring_fitness__[__j__][0] <= __best_minimum__[0] and \
                                self.__offspring_fitness__[__j__][1] < __best_minimum__[1]:
                            __best_minimum__ = self.__offspring_fitness__[__j__]

                    else:
                        pass

                    __j__ += 1

                if not __new_individual__:
                    __new_generation__.append(copy.deepcopy(self.__pool__[__i__]))

                    if (self.__pool_fitness__[__j__][0] < __best_minimum__[0] and
                        self.__pool_fitness__[__j__][1] <= __best_minimum__[1]) or \
                            (self.__pool_fitness__[__j__][0] <= __best_minimum__[0] and
                             self.__pool_fitness__[__j__][1] < __best_minimum__[1]):
                        __best_minimum__ = self.__pool_fitness__[__j__]

            # Save the evaluation results (fitness values) of the population
            self.__filing__.Append(Filename=self.__files__[3], List=self.__pool_fitness__)

            # Update pool to new generation
            self.__pool__ = __new_generation__

            # Save the new generation as the best in Best file
            self.__filing__.Save(Filename=self.__files__[2], Lists=self.__pool__)

            # Generate new offspring
            self._generate_offspring()

            print(f'Sweep completed in {round(time.time() / 60 - __loop_time__, 2)} minutes.', end='')
            if Convergence is None:
                print(f' Remaining time: {round(time.time() / 60 - SearchTimeMinutes, 2)} minutes.')
            else:
                print(f' Current best fitness is {__best_minimum__}, where the defined convergence is {Convergence}.')

            if Convergence is None and (time.time() / 60 - __start__) > SearchTimeMinutes:
                break
            elif Convergence is not None and __best_minimum__ <= Convergence:
                break
            else:
                pass

    def _generate_offspring(self):
        """
        Description:
        ------------
        Generates the offspring of the current generation. The full process is performed within this method,
        specifically selecting the parents, performing the crossover, and then performing the mutation of the
        offspring.

        Parameters:
        -----------
        None.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        # Delete content in Temp file
        self.__filing__.DeleteContent(Filename=self.__files__[0])
        # Evaluate pool
        self.__pool_fitness__ = [self._evaluate_individual(__simulation_result__=__i__[1])
                                 for __i__ in self.__pool__]
        # Select parents
        self._select_parents()
        # Crossover
        self._crossover()
        # Mutation
        self._mutation()
        # Save the offspring in temp file
        self.__filing__.Save(Filename=self.__files__[0], Lists=self.__offspring__)

    def _populate_simulation_results(self, Pool=True):
        """
        Description:
        ------------
        Simulates individuals/children that need simulating. Note that any individuals/children that have already
        been simulated does not get simulated as it is not needed. Also, if the individual/child has a matching
        parameter value set from the Explored file, the simulation result from that specific individual within the
        Explored file gets used for the individual/child. In other words, if the individual/child does not have a
        unique parameter value set, it does not go through the CST simulator.

        Parameters:
        -----------
        Pool:                       bool
                                    If True, the population is simulated, else the offspring is simulated.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        if Pool:
            __pool__ = self.__pool__
            __file__ = self.__files__[2]
        else:
            __pool__ = self.__offspring__
            __file__ = self.__files__[0]

        # Simulate remaining individuals/children
        for __i__ in range(len(__pool__)):
            if not len(__pool__[__i__][1]):
                # Get possible simulation result so that CST is not needed
                __temp__ = self.__filing__.Duplicate(Filename=self.__files__[1], List=__pool__[__i__])

                # Duplicate not found, which means that the current individual/child is unique. Thus, simulate its
                # parameters
                if not isinstance(__temp__, list):
                    __pool__[__i__][1] = \
                        self.__individual__.SimulateModel(Parameters=__pool__[__i__][0], Rounding=self.__rounding__)
                    self.__filing__.Append(Filename=self.__files__[1], List=__pool__[__i__])

                # Duplicate found, assign the __temp__ to the individual/child
                else:
                    __pool__[__i__] = __temp__

                # Update Best/Temp file
                self.__filing__.Save(Filename=__file__, Lists=__pool__)

        # Update pool
        if Pool:
            self.__pool__ = __pool__

        # Update offsprings
        else:
            self.__offspring__ = __pool__

    def _initialize_population(self):
        """
        Description:
        ------------
        Initializes the population by either generating a new set of individuals or by extracting the individuals from 
        the Best file (if present and has the correct number of individuals).s

        Parameters:
        -----------
        None.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        __temp__ = self.__filing__.Read(Filename=self.__files__[2])

        # Create a new initial population if either one has not been created before or the number of individuals
        # does not match the population size
        if (not isinstance(__temp__, list) and __temp__ == -1) or (isinstance(__temp__, list) and
                                                                   len(__temp__) != self.__population_size__):
            self.__pool__ = []

            for __i__ in range(self.__population_size__):
                # Create individual
                self.__pool__.append([[], []])

                # Generate a random set of parameter values
                self.__pool__[-1][0] = self.__individual__.GenerateRandomParameterValue(Rounding=self.__rounding__)

            self.__filing__.Save(Filename=self.__files__[2], Lists=self.__pool__)

        # Assign the pool attribute to the __temp__ variable if there exists a population with the correct
        # number of individuals
        else:
            self.__pool__ = __temp__

    def _evaluate_individual(self, __simulation_result__=None):
        """
        Description:
        ------------
        Evaluates the individual/child by analysing its simulation results. This is the core of the genetic algorithm
        as a bad fitness function deems the genetic algorithm as useless. Only the return loss and gain responses are
        analysed for this current build.

        Parameters:
        -----------
        __simulation_result__:      list
                                    A list that contains two lists, the first list is the return loss responses and
                                    the last list contains the gain responses. Each list has its own frequency range
                                    that correlate to the response.

        Returns:
        --------
        Returns the return loss and gain fitness values, as a list of two elements, of the individual/child.

        Notes:
        ------
        None.
        """

        __s11_fitness__ = 0.0                                   # The total fitness value for s11 result
        __gain_fitness__ = 0.0                                  # The total fitness value for gain result

        # Determine the number of bands in the form of [f_min, f_max, minimum return loss (in linear form), average
        # gain over the band f_min to f_max]
        __bands__ = self._get_bands(__simulation_result__=__simulation_result__)

        # If no bands were found, it is considered as the worst possible solution
        if len(__bands__) == 0:
            for __i__ in self.__individual__.__objective__:
                __s11_fitness__ += abs(__i__[0] + __i__[1]) * 9e9
            __gain_fitness__ = 1 / 10 ** (-80/10)

            return [__s11_fitness__, __gain_fitness__]

        # If at least one band has been found under the condition of self.__individual__.__objective__
        else:

            # Add a possible bias. Note that if the __number_of_bands__ has the same value as
            # len(self.__individual__.__objective__), there will not be any bias to add to the fitness with
            __bias__ = abs(len(self.__individual__.__objective__) - len(__bands__))

            __s11_fitness__ += __bias__
            __gain_fitness__ += __bias__

            # Iterate through the band(s) that were found
            for __i__ in __bands__:

                # Collect all fitness values from current band that was found and choose the fitness value that is
                # the lowest, which is the best fitness value possible for the number of specified bands in
                # self.__individual__.__objective__
                __fitness_temp__ = []
                __objective_met__ = False
                for __j__ in self.__individual__.__objective__:

                    # If the current band is within the objective band, perform a reward
                    if __j__[0] * (1 - __j__[2]) <= __i__[0] <= (__j__[0] * (1 + __j__[2])) and \
                            (__j__[1] * (1 - __j__[2])) <= __i__[1] <= (__j__[1] * (1 + __j__[2])):

                        # The reward is the receptacle of the bandwidth (in Mega Hertz) multiplied by the minimum
                        # return loss
                        if __i__[1] - __i__[0] == 0:
                            __fitness_temp__.append(1 / 1000 * 10 ** (-10 / 20))
                        else:
                            __fitness_temp__.append(1 / (1000 * (__i__[1] - __i__[0])) * 10 ** (-10 / 20))

                        __objective_met__ = True

                    else:
                        # The penalty is the bandwidth (in Mega Hertz) multiplied by the minimum return loss
                        __fitness_temp__.append(1000 * (abs(__i__[0] - __j__[0]) + abs(__i__[1] - __j__[1])))

                # Update fitness value by adding the fitness value with the best possible fitness value from
                # __fitness_temp__ list, where the best fitness value is 0.0.
                __s11_fitness__ += min(__fitness_temp__)
                if __objective_met__ and __bias__ == 0:
                    __gain_fitness__ += __i__[3]
                else:
                    __gain_fitness__ += 1 / 10 ** (-80 / 10)

        # Return the total fitness value from the given individual CST simulation results, in the form of
        # s11 fitness and gain fitness. Remember that the fitness value is best when 0.0.
        return [__s11_fitness__, __gain_fitness__]

    def _get_bands(self, __simulation_result__=None):
        """
        Description:
        ------------
        This function will be of the following format: [f_min, f_max, s11_min, avg_gain], where s11_min and avg_gain
        correlates to the f_min and f_max range (band). The s11_min is transformed into its linear equivalent and the
        average gain is determined as 1 / 10 ^ (avg_gain / 10)

        Parameters:
        -----------
        __simulation_result__:      list
                                    A list that contains two lists, the first list is the return loss responses and
                                    the last list contains the gain responses. Each list has its own frequency range
                                    that correlate to the response.

        Returns:
        --------
        Returns the band(s) determined in the form as explained in the description.

        Notes:
        ------
        None.
        """

        if self.__individual__.__objective__ is None:
            raise Exception('<SearchSpaceOptimizer: _get_bands: self.__individual__.__objective__ is of None type>')

        __index__ = 0                                   # Index for iterating through the individual's results

        # Evaluation of return loss results
        __s11_freq__ = __simulation_result__[0][0]      # List of frequency values, in ascending order
        __s11__ = __simulation_result__[0][1]           # List of |S11|, in dB, values from the __freq__ inputs
        __gain_freq__ = __simulation_result__[1][0]     # Frequency range specified for the gain responses
        __gain__ = __simulation_result__[1][1]          # The gain responses over the specified frequency range

        __number_of_bands__ = []                        # List which will collect multiple bands that are under
                                                        # the specified S11 value from self.__individual__.__objective__
                                                        # Evaluation of gain responses over a specified frequency range

        # Determine the number of actual bands under the specified self.__individual__.__objective__ variable
        while __index__ < len(__s11__):

            # If a lower edge frequency is found that is lower than -10 dB
            if __s11__[__index__] <= -10:
                # Append possible band n
                __number_of_bands__.append([])
                __minimum_return_loss__ = __s11__[__index__]

                # Append lower edge frequency
                __number_of_bands__[-1].append(__s11_freq__[__index__])

                # Determine the upper edge frequency of band n by incrementing __index__ until the upper edge
                # frequency has been found
                while (__index__ + 1) < len(__s11__) and __s11__[__index__ + 1] < -10:
                    if __minimum_return_loss__ > __s11__[__index__]:
                        __minimum_return_loss__ = __s11__[__index__]
                    __index__ += 1

                # Append upper edge frequency and minimum return loss value (mode of operation)
                __number_of_bands__[-1].append(__s11_freq__[__index__])
                __number_of_bands__[-1].append(10 ** (__minimum_return_loss__ / 20))

                # For collecting the gain values over the determined band
                avg_gain = []

                for __i__ in range(len(__gain_freq__)):
                    if __number_of_bands__[-1][0] <= __gain_freq__[__i__] <= __number_of_bands__[-1][1]:
                        avg_gain.append(__gain__[__i__])

                # If there were gain values appended, determine the average gain and use the following formula:
                # 1 / 10 ^ (avg_gain / 10)
                if len(avg_gain) > 0:
                    avg_gain = sum(avg_gain) / len(avg_gain)
                    __number_of_bands__[-1].append(1 / 10 ** (avg_gain / 10))

                # If no gain values were found, append the worst possible gain
                else:
                    __number_of_bands__[-1].append(1 / 10 ** (-80 / 10))

            __index__ += 1

        return __number_of_bands__

    def _select_parents(self):
        """
        Description:
        ------------
        The method uses the self.__pool_fitness__ attribute to determine which parent will be selected for breeding.
        The addition of both the return loss and gain fitness values gives a single fitness value, which is used as
        a probability value. The lower the fitness value, the higher the chance the parent will be selected for
        breeding. A parent is selected by appending the index of the individual from the self.__pool__ attribute to
        the self.__pool_index__ attribute.

        Parameters:
        -----------
        None.

        Returns:
        --------
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

        # Number of parents to insert in the self.__pool_index__ list in for producing offspring. Note that 2 is
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
            # This happens when the user incorrectly configured the attribute(s) or a special case happened.
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
        Performs the crossover operation on the selected parents to generate offspring. The number of offspring to
        generate is defined from the self.__number_of_offspring__ attribute defined by the user.

        Parameters:
        -----------
        None.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        self.__offspring__ = []                     # The offspring list to populate given the
                                                    # self.__number_of_offspring__ variable.

        # Loop for the number of required offspring to generate
        for __i__ in range(self.__number_of_offspring__):

            __index__ = __i__ % len(self.__pool_index__)

            # Append a fresh list, which is a new child that has no chromosomes yet.
            self.__offspring__.append([[], []])

            # Perform crossover
            for __j__ in range(len(self.__pool__[0][0])):
                if np.random.choice([True, False], p=[self.__crossover_rate__, 1 - self.__crossover_rate__]):
                    self.__offspring__[-1][0].append(self.__pool__[self.__pool_index__[__index__]][0][__j__])
                else:
                    self.__offspring__[-1][0].append(
                        self.__pool__[self.__pool_index__[(__index__ + 1) % len(self.__pool_index__)]][0][__j__]
                    )

            __tries__ = 10
            __success__ = False
            while __tries__ >= 0 and not __success__:

                try:
                    self.__individual__.CheckBoundary(Parameters=self.__offspring__[-1][0], Rounding=self.__rounding__)
                    __success__ = True

                except Exception as __error__:
                    if self.__debugging__:
                        print(__error__)

                    if __tries__ == 0:
                        self.__offspring__[-1][0] = self.__individual__.GenerateRandomParameterValue(
                            Rounding=self.__rounding__)
                    else:
                        try:
                            __random_index__ = random.choice(range(len(self.__offspring__[-1][0])))
                            self.__offspring__[-1][0][__random_index__] = \
                                self.__individual__.GenerateRandomParameterValue(Parameters=self.__offspring__[-1][0],
                                                                                 ParameterIndex=__random_index__,
                                                                                 Rounding=self.__rounding__)
                        except Exception as __error__:
                            if self.__debugging__:
                                print(f'<SearchSpaceOptimizer: crossover: {__error__}>')

                            self.__offspring__[-1][0] = \
                                self.__individual__.GenerateRandomParameterValue(Rounding=self.__rounding__)
                            __success__ = True

                __tries__ -= 1

            # Shuffle indices in self.__pool_index__ for fair offspring generation
            random.shuffle(self.__pool_index__)

    def _mutation(self):
        """
        Description:
        ------------
        Performs the mutation operation on the offspring. The type of mutation operators are to either increment a
        parameter value, decrement a parameter value, or generate a random parameter value.

        Parameters:
        -----------
        None.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        # Individual for loop
        for __i__ in range(len(self.__offspring__)):
            for __j__ in range(len(self.__offspring__[__i__][0])):
                if np.random.choice([True, False], p=[self.__mutation_rate__, 1 - self.__mutation_rate__]):
                    __choice__ = [0, 1, 2, 3]
                    random.shuffle(__choice__)

                    if random.choice(__choice__) == 0:
                        self.__individual__.IncrementParameterValue(
                            Parameters=self.__offspring__[__i__][0],
                            Index=__j__,
                            Rounding=self.__rounding__
                        )

                    elif random.choice(__choice__) == 1:
                        self.__individual__.DecrementParameterValue(
                            Parameters=self.__offspring__[__i__][0],
                            Index=__j__,
                            Rounding=self.__rounding__
                        )

                    elif random.choice(__choice__) == 2:

                        __value__ = self.__offspring__[__i__][0][__j__]

                        try:
                            self.__individual__.GenerateRandomParameterValue(
                                Parameters=self.__offspring__[__i__][0],
                                ParameterIndex=__j__,
                                Rounding=self.__rounding__
                            )

                        except Exception as __error__:
                            if self.__debugging__:
                                print(f'<SearchSpaceOptimizer: mutation: {__error__}>')

                            self.__offspring__[__i__][0][__j__] = __value__

                    elif random.choice(__choice__) == 3:
                        self.__offspring__[__i__][0] = \
                            self.__individual__.GenerateRandomParameterValue(Rounding=self.__rounding__)
                    else:
                        pass
