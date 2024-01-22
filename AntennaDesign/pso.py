# The initialization module for the package AntennaDesign, which will be a list of common public libraries,
# see AntennaDesign.__init__ for more information
from AntennaDesign.__init__ import *


class PSO:
    """
    Description:
    ------------
    Based on particle swarm optimizer, this class determines the optimal solution given the trained surrogates as its
    objectives.

    Attributes:
    -----------
    __boundary__:                   list
                                    A list of parameter boundaries per parameter in the form of
                                    [[lower bound 0, upper bound 0], [lower bound 1, upper bound 1], ...,
                                    [lower bound n, upper bound n]].
    __surrogate__:                  list
                                    A list with two surrogates of type CoarseModel. Each surrogate is assumed to be
                                    trained and ready for predictions.
    __particle__:                   list
                                    A list of particles for exploration. Each particle has the form of
                                    [position, velocity, current fitness, personal best fitness, personal best
                                    position].
    __global_best__:                list
                                    The particle with the best solution in the form of [position, fitness].
    __w__:                          float
                                    The inertia weight for the particle swarm optimizer.
    __c1__:                         float
                                    The personal influence of a particle.
    __c2__:                         float
                                    The social influence of a particle.

    Methods:
    --------
    __init__(NumberOfParticles=None, ParameterRanges=None, Objective=None):
                                    The constructor of the class, where the NumberOfParticles, ParameterRanges, and
                                    Objective must be given as arguments.
    Optimize(NumberOfIterations=None, Convergence=None, W=0.9, C1=1.5, C2=1.5):
                                    Begins the optimization process, where the NumberOfIterations and/or Convergence
                                    arguments are required before beginning.
    _objective():
                                    The fitness evaluation of the particles, where the two surrogates are used for
                                    determining the fitness of the return loss and gain responses.
    _update_personal_best():
                                    Updates the personal best per particle.
    _update_global_best():
                                    Updates the global best amongst the particles for the nth iteration.
    _update_velocity():
                                    Updates the velocities of each parameter within each particle.
    _update_position():
                                    Updates the position of each parameter within each particle.

    Notes:
    ------
    None.
    """

    def __init__(self, NumberOfParticles=None, ParameterRanges=None, Objective=None):
        """
        Description:
        ------------
        The constructor of the PSO class. It expects three parameters as arguments, specifically the
        NumberOfParticles, ParameterRanges, and Objective. The particles are then initialized with random parameter
        values within their defined ranges (Parameter Ranges n). Their velocities are initialized to a random value
        between 0 and 1. Finally, the global best is found by first determining the fitness values of each parameter
        per particle, which is considered as the 0th iteration.

        Parameters:
        -----------
        NumberOfParticles:          int
                                    Defined by the user, this is used  to initialize the number of particles for the
                                    class.
        ParameterRanges:            list
                                    A list of lists, where each parameter is a list of the form [lower bound,
                                    upper bound], which is used to describe the bounds per parameter of concern.
        Objective:                  list
                                    A list that contains two elements of CoarseModel type. This is used for finding/
                                    determining the fitness's of the return loss and gain responses from the trained
                                    surrogates.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        if NumberOfParticles is None or ParameterRanges is None or Objective is None:
            raise Exception('<PSO: One or more arguments are of None type>')

        # ParameterRanges is in the form: [[l0, u0], [l1, u1], ..., [l_n, u_n]]
        self.__boundary__ = ParameterRanges
        self.__surrogate__ = Objective
        self.__particle__ = []
        self.__global_best__ = [[], [0.0, 0.0]]
        self.__w__ = None
        self.__c1__ = None
        self.__c2__ = None

        # Initialize particles
        for __i__ in range(NumberOfParticles):
            # Append particle n with following format: [position, velocity, fitness, best fitness, personal best]
            self.__particle__.append([[], [], [0.0, 0.0], [0.0, 0.0], []])

            for __j__ in ParameterRanges:
                # Initialize particle position with following formula:
                # Parameter n = Lower bound + rand(1, 0) * (Upper bound - Lower bound)
                self.__particle__[-1][0].append(__j__[0] + random.uniform(a=1, b=0) * (__j__[1] - __j__[0]))

                # Initialize particle velocity with a uniform number between 0 and 1
                self.__particle__[-1][1].append(random.uniform(a=0, b=1))

        # Update fitness values of particles
        self._objective()

        # Initialize personal best
        for __i__ in range(len(self.__particle__)):
            self.__particle__[__i__][3] = copy.deepcopy(self.__particle__[__i__][2])
            self.__particle__[__i__][4] = copy.deepcopy(self.__particle__[__i__][0])

        # Initialize global best
        self.__global_best__[0] = copy.deepcopy(self.__particle__[0][4])
        self.__global_best__[1] = copy.deepcopy(self.__particle__[0][3])
        for __i__ in range(1, len(self.__particle__), 1):
            if (self.__particle__[__i__][3][0] < self.__global_best__[1][0] and
                self.__particle__[__i__][3][1] <= self.__global_best__[1][1]) or \
                    (self.__particle__[__i__][3][0] <= self.__global_best__[1][0] and
                     self.__particle__[__i__][3][1] < self.__global_best__[1][1]):
                self.__global_best__[0] = copy.deepcopy(self.__particle__[__i__][4])
                self.__global_best__[1] = copy.deepcopy(self.__particle__[__i__][3])

    def Optimize(self, NumberOfIterations=None, Convergence=None, W=0.9, C1=1.5, C2=1.5):
        """
        Description:
        ------------
        Iterates through the explore space (the parameter ranges) in order to find the optimal solution (global best).

        Parameters:
        -----------
        NumberOfIterations:         int
                                    The number of iterations the particle swarm optimizer is allowed to execute whilst
                                    determining the optimal solution.
        Convergence:                float
                                    Used for early stopping/termination if there are still iterations left to execute.
        W:                          float
                                    The inertia weight for the particle swarm optimizer.
        C1:                         float
                                    The personal influence per particle for the particle swarm optimizer.
        C2:                         float
                                    The social influence per particle for the particle swarm optimizer.

        Returns:
        --------
        Returns the optimal solution, specifically the parameter values from the self.__global_best__ variable.

        Notes:
        ------
        None.
        """

        if NumberOfIterations is None and Convergence is None:
            raise Exception('<PSO: Optimize: Both arguments are of None type>')
        if NumberOfIterations is None:
            raise Exception('<PSO: Optimize: NumberOfIterations is of None type>')
        if W is None or C1 is None or C2 is None:
            raise Exception('<PSO: Optimize: W, C1, and/or C2 is of None type>')

        self.__w__ = W
        self.__c1__ = C1
        self.__c2__ = C2

        r_fitness = []
        g_fitness = []

        for __i__ in range(NumberOfIterations):

            __r_temp__ = []
            __g_temp__ = []

            for __j__ in self.__particle__:
                __r_temp__.append(__j__[2][0])
                __g_temp__.append(__j__[2][1])

            r_fitness.append(sum(__r_temp__) / len(__r_temp__))
            g_fitness.append(sum(__g_temp__) / len(__g_temp__))

            # Update velocity
            self._update_velocity()

            # Update position
            self._update_position()

            # Calculate fitness
            self._objective()

            # Update personal best
            self._update_personal_best()

            # Update global best
            self._update_global_best()

            # Update inertia weight
            self.__w__ -= W / NumberOfIterations

            print(f'\r<PSO: Optimize: Iteration {__i__} \t Global best is: {self.__global_best__[0]}>', end='')

            # Check for convergence
            if Convergence is not None and (self.__global_best__[1][0] <= Convergence or
                                            self.__global_best__[1][1] <= Convergence):
                break

        return self.__global_best__[0], r_fitness, g_fitness

    def _objective(self):
        """
        Description:
        ------------
        Determines the fitness values for each parameter per particle. The two surrogates, assumed trained, are used
        for the return loss and gain responses.

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
        # for __i__ in range(len(self.__particle__)):
        #     self.__particle__[__i__][2][0] = 0.1 * self.__particle__[__i__][0][0] ** 2 + 18 * self.__particle__[__i__][0][0] - 48
        for __i__ in range(len(self.__particle__)):
            __temp__ = self.__surrogate__.FeedForward(__input__=self.__particle__[__i__][0], __target__=None, __return_outputs__=True)
            __temp__[0] *= 10
            __temp__[1] *= 10
            __temp__[3] = -np.log(1 / __temp__[3] - 1)
            __objective_met__ = False

            if 2.30572 <= __temp__[0] <= 2.41428 and 2.38388 <= __temp__[1] <= 2.49612:
                if __temp__[1] - __temp__[0] == 0:
                    self.__particle__[__i__][2][0] = 1 / 1000 * 10 ** (-10 / 20)
                else:
                    self.__particle__[__i__][2][0] = 1 / (1000 * (__temp__[1] - __temp__[0])) * 10 ** (-10 / 20)

                __objective_met__ = True

            else:
                # The penalty is the bandwidth (in Mega Hertz) multiplied by the minimum return loss
                self.__particle__[__i__][2][0] = 1000 * (abs(__temp__[0] - 2.36) + abs(__temp__[1] - 2.44))

            if __objective_met__:
                self.__particle__[__i__][2][1] = 1 / __temp__[3]

            else:
                self.__particle__[__i__][2][1] = 1 / 10 ** (-80 / 10)

    def _update_personal_best(self):
        """
        Description:
        ------------
        Updates the personal best per particle by comparing the current fitness and personal best fitness values whilst
        adopting multi-objective theory for only two objectives.

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

        for __i__ in range(len(self.__particle__)):
            if (self.__particle__[__i__][2][0] < self.__particle__[__i__][3][0]
                    and self.__particle__[__i__][2][1] <= self.__particle__[__i__][3][1]) or \
                    (self.__particle__[__i__][2][0] <= self.__particle__[__i__][3][0] and
                     self.__particle__[__i__][2][1] < self.__particle__[__i__][3][1]):
                self.__particle__[__i__][3] = copy.deepcopy(self.__particle__[__i__][2])
                self.__particle__[__i__][4] = copy.deepcopy(self.__particle__[__i__][0])

    def _update_global_best(self):
        """
        Description:
        ------------
        Updates the global best for the current iteration by simply comparing the current global best fitness values
        with the personal best fitness values from the particles.

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

        for __i__ in range(len(self.__particle__)):
            if (self.__particle__[__i__][3][0] < self.__global_best__[1][0] and
                self.__particle__[__i__][3][1] <= self.__global_best__[1][1]) or \
                    (self.__particle__[__i__][3][0] <= self.__global_best__[1][0] and
                     self.__particle__[__i__][3][1] < self.__global_best__[1][1]):
                self.__global_best__[0] = copy.deepcopy(self.__particle__[__i__][4])
                self.__global_best__[1] = copy.deepcopy(self.__particle__[__i__][3])

    def _update_velocity(self):
        """
        Description:
        ------------
        Updates the velocities per parameter per particle. This function is first used as the _update_position() needs
        an updated velocity per parameter per particle.

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

        for __i__ in range(len(self.__particle__)):
            for __j__ in range(len(self.__particle__[__i__][1])):
                self.__particle__[__i__][1][__j__] = \
                    self.__w__ * self.__particle__[__i__][1][__j__] + \
                    self.__c1__ * random.uniform(0, 1) * \
                    (self.__particle__[__i__][4][__j__] - self.__particle__[__i__][0][__j__]) + \
                    self.__c2__ * random.uniform(0, 1) * \
                    (self.__global_best__[0][__j__] - self.__particle__[__i__][0][__j__])

    def _update_position(self):
        """
        Description:
        ------------
        Updates the positions (parameter values) per parameter per particle.

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

        for __i__ in range(len(self.__particle__)):
            for __j__ in range(len(self.__particle__[__i__][0])):
                # Update position
                self.__particle__[__i__][0][__j__] = self.__particle__[__i__][1][__j__] + \
                                                     self.__particle__[__i__][0][__j__]

                # Check if the new position is not out of bounds. Replace either to lower or upper bounds if
                # the new position is less than the lower bounds or greater than the upper bounds
                if self.__particle__[__i__][0][__j__] < self.__boundary__[__j__][0]:
                    self.__particle__[__i__][0][__j__] = copy.deepcopy(self.__boundary__[__j__][0])
                elif self.__particle__[__i__][0][__j__] > self.__boundary__[__j__][1]:
                    self.__particle__[__i__][0][__j__] = copy.deepcopy(self.__boundary__[__j__][1])
                else:
                    pass
