from AntennaDesign.__init__ import *


class PSO:
    def __init__(self, NumberOfParticles=None, ParameterRanges=None, Objective=None):
        # Parameter ranges is used to initialize particles

        if NumberOfParticles is None or ParameterRanges is None or Objective is None:
            raise Exception('<PSO: One or more arguments are of None type>')

        # ParameterRanges is in the form: [[l0, u0], [l1, u1], ..., [l_n, u_n]]
        self.__boundary__ = ParameterRanges
        self.__surrogate__ = Objective
        self.__particle__ = []
        self.__global_best__ = [[], []]
        self.__w__ = None
        self.__c1__ = None
        self.__c2__ = None

        # Initialize particles
        for __i__ in range(NumberOfParticles):
            # Append particle n with following format: [position, velocity, fitness, best fitness, personal best]
            self.__particle__.append([[], [], None, None, []])

            for __j__ in ParameterRanges:
                # Initialize particle position with following formula:
                # Parameter n = Lower bound + rand(1, 0) * (Upper bound - Lower bound)
                self.__particle__[-1][0].append(__j__[0] + random.uniform(a=__j__[0], b=__j__[1]))

                # Initialize particle velocity with a uniform number between 0 and 1
                self.__particle__[-1][1].append(random.uniform(a=0, b=1))

        # Update fitness values of particles
        self.__objective__()

        # Initialize personal best
        for __i__ in range(len(self.__particle__)):
            self.__particle__[__i__][3] = copy.deepcopy(self.__particle__[__i__][2])
            self.__particle__[__i__][4] = copy.deepcopy(self.__particle__[__i__][0])

        # Initialize global best
        self.__global_best__[0] = copy.deepcopy(self.__particle__[0][4])
        self.__global_best__[1] = copy.deepcopy(self.__particle__[0][3])
        for __i__ in range(1, len(self.__particle__), 1):
            if self.__particle__[__i__][3] < self.__global_best__[1]:
                self.__global_best__[0] = copy.deepcopy(self.__particle__[__i__][4])
                self.__global_best__[1] = copy.deepcopy(self.__particle__[__i__][3])

    def Optimize(self, NumberOfIterations=None, Convergence=None, W=0.9, C1=1.5, C2=1.5):
        if NumberOfIterations is None and Convergence is None:
            raise Exception('<PSO: Optimize: Both arguments are of None type>')
        if NumberOfIterations is None:
            raise Exception('<PSO: Optimize: NumberOfIterations is of None type>')
        if W is None or C1 is None or C2 is None:
            raise Exception('<PSO: Optimize: W, C1, and/or C2 is of None type>')

        self.__w__ = W
        self.__c1__ = C1
        self.__c2__ = C2

        for __i__ in range(NumberOfIterations):

            # Update velocity
            self.__update_velocity__()

            # Update position
            self.__update_position__()

            # Calculate fitness
            self.__objective__()

            # Update personal best
            self.__update_personal_best__()

            # Update global best
            self.__update_global_best__()

            # Update inertia weight
            self.__w__ -= W / NumberOfIterations

            print(f'\r<PSO: Optimize: Iteration {__i__} \t Global best is: {self.__global_best__[0]}>', end='')

            # Check for convergence
            if Convergence is not None:
                if self.__global_best__[1] <= Convergence:
                    break

        return self.__global_best__[0]

    def __objective__(self):
        for __i__ in range(len(self.__particle__)):
            self.__particle__[__i__][2] = 3 * self.__particle__[__i__][0][0] ** 2 - 18 * self.__particle__[__i__][0][0] - 48

    def __update_personal_best__(self):
        for __i__ in range(len(self.__particle__)):
            if self.__particle__[__i__][2] < self.__particle__[__i__][3]:
                self.__particle__[__i__][3] = copy.deepcopy(self.__particle__[__i__][2])
                self.__particle__[__i__][4] = copy.deepcopy(self.__particle__[__i__][0])

    def __update_global_best__(self):
        for __i__ in range(len(self.__particle__)):
            if self.__particle__[__i__][3] < self.__global_best__[1]:
                self.__global_best__[0] = copy.deepcopy(self.__particle__[__i__][4])
                self.__global_best__[1] = copy.deepcopy(self.__particle__[__i__][3])

    def __update_velocity__(self):
        for __i__ in range(len(self.__particle__)):
            for __j__ in range(len(self.__particle__[__i__][1])):
                self.__particle__[__i__][1][__j__] = \
                    self.__w__ * self.__particle__[__i__][1][__j__] + \
                    self.__c1__ * random.uniform(0, 1) * \
                    (self.__particle__[__i__][4][__j__] - self.__particle__[__i__][0][__j__]) + \
                    self.__c2__ * random.uniform(0, 1) * \
                    (self.__global_best__[0][__j__] - self.__particle__[__i__][0][__j__])

    def __update_position__(self):
        for __i__ in range(len(self.__particle__)):
            for __j__ in range(len(self.__particle__[__i__][0])):
                # Update position
                self.__particle__[__i__][0][__j__] = self.__particle__[__i__][1][__j__] + self.__particle__[__i__][0][__j__]

                # Check if the new position is not out of bounds. Replace either to lower or upper bounds if
                # the new position is less than the lower bounds or greater than the upper bounds
                if self.__particle__[__i__][0][__j__] < self.__boundary__[__j__][0]:
                    self.__particle__[__i__][0][__j__] = copy.deepcopy(self.__boundary__[__j__][0])
                elif self.__particle__[__i__][0][__j__] > self.__boundary__[__j__][1]:
                    self.__particle__[__i__][0][__j__] = copy.deepcopy(self.__boundary__[__j__][1])
                else:
                    pass
