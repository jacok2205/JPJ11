# The initialization module for the package AntennaDesign, which will be a list of common public libraries,
# see AntennaDesign.__init__ for more information
from AntennaDesign.__init__ import *


class CoarseModel:
    """
    Description:
    ------------
    Based on a pyramidal deep regression neural network architecture, this class trains, verifies, and tests the 
    defined architecture from the user given the parameters. The optimizer for the network is based on the adaptive
    moments estimator (ADAM) algorithm. Also, the structure of the neural network is a fully connected neural network.

    Attributes:
    -----------
    __beta1__:                      float
                                    Biased value for the first moment (__mean__).
    __beta2__:                      float
                                    Biased value for the second moment (__variance__).
    __epsilon__:                    float
                                    A value for the ADAM algorithm so that division by zero is avoided.
    __alpha__:                      float
                                    The learning rate for the neural network.
    __N__:                          int
                                    The batch size for the neural network.
    __init_N__:                     int
                                    Variable used to notify the network when to back-propagate.
    __time_step__:                  int
                                    A variable used for adjusting the learning rate dynamically.
    __filing__:                     Filing
                                    Used for writing, reading, appending, deleting data for later use.
    __directory__:                  str
                                    A string representing the directory for the instance of this class to store results.
    __files__:                      list
                                    A list that contains file names to create, write, and read from. The following files
                                    are used: 'Weights'.
    __phi_k__:                      int
                                    Variable that describes the number of output channels / output neurons for the
                                    neural network.
    __d_s__:                        int
                                    Variable that describes the number of hidden layers for the neural network.
    __s_c__:                        float
                                    Variable that describes the rate that the architecture of the neural network expands
                                    from the output layer to the input layer, in a trapezoidal fashion.
    __error_k__:                    list
                                    Variable used to keep the error at the output layer given the target/actual output.
    __nrmse__:                      float
                                    Variable used to keep the normalized root-mean-square-error value per feedforward
                                    operation.
    __neuron_array__:               list
                                    A 2D list which is the architecture of the neural network, where the first
                                    dimension is the layer of the network and the second layer is the neuron of the
                                    network.
    __in_j__:                       list
                                    A 2D list which keeps all the values, averaged to the batch size __N__, of the
                                    dot product operation for the neural network in order to train on.
    __out_j__:                      list
                                    A 2D list which keeps all the values, averaged to the batch size __N__, of the
                                    activation operation for the neural network in order to train on.
    __delta__:                      list
                                    A 2D list which keeps all the values of the delta values per neuron per layer for
                                    the neural network in order to train on.
    __weights_array__:              list
                                    A 3D list which keeps all the weights linking the neurons to each other per layer
                                    of the neural network.
    __grad__:                       list
                                    A 3D list which keeps all the gradients, averaged over the batch size,
                                    per weight per the neuron per layer of the neural network.
    __mean__:                       list
                                    A 3D list which keeps all the first moment values, averaged over the batch size,
                                    per weight per the neuron per layer of the neural network.
    __variance__:                   list
                                    A 3D list which keeps all the second moment values, averaged over the batch size,
                                    per weight per the neuron per layer of the neural network.
    __debugging__:                  bool
                                    For debugging purposes (developer mode).

    Methods:
    --------
    __init__(NumberOfHiddenLayers=None, NumberOfInputChannels=None, NumberOfOutputChannels=None,
                 ScalingFactor=1.5, Filing=None, Directory=None, Debugging=False):
                                    The constructor of the class, where the NumberOfOutputChannels and
                                    NumberOfHiddenLayers must be given as arguments. The neural network is
                                    initialized if all required parameters are correct.
    Train(BatchSize=10, LearningRate=1e-3, Beta1=0.900, Beta2=0.999, Epsilon=1e-8, TrainingData=None,
                ValidationData=None, TestingData=None, NumberOfEpochs=None, TrainDurationMinutes=None,
                NRMSEConvergence=None):
                                    Used for training the neural network given that the TrainingData, ValidationData,
                                    and TestingData is correctly parsed as arguments.
    FeedForward(__input__, __target__, __learn__=False, __return_outputs__=False):
                                    Feeds the neural network given the input and target lists where the output
                                    is analysed if in training mode.
    _summation(__layer_index__, __neuron_index__):
                                    Performs the dot product operation per neuron in the neural network given the
                                    layer index and neuron index.
    _activation(__input__):
                                    Performs the activation operation per neuron in the neural network given the input.
    _activation_derivative(__input__):
                                    Performs the derivative of the activation operation.
    _update_loss(__target__, __learn__=True):
                                    Updates the loss at the outputs of the neural network given the target list and
                                    whether training mode is True (__learn__=True).
    _update_weights():
                                    In training mode, the weights of the neural network are updated.
    _update_gradients():
                                    In training mode, the gradients of the weights are updated.
    _update_mean_variance():
                                    In training mode, the two moments per weight, both the mean and variance, are
                                    updated.

    Notes:
    ------
    None.
    """

    def __init__(self, NumberOfHiddenLayers=None, NumberOfInputChannels=None, NumberOfOutputChannels=None,
                 ScalingFactor=1.5, Filing=None, Directory=None, Debugging=False):
        """
        Description:
        ------------
        The constructor of the ModelGeometry class. It expects four parameters as arguments, specifically the
        NumberOfInputChannels (optional), NumberOfHiddenLayers, NumberOfOutputChannels, and ScalingFactor (optional).
        The neural network is then constructed. Finally, the weights are replaced with the Weights file (if available).

        Parameters:
        -----------
        NumberOfHiddenLayers:       int
                                    The number of hidden layers the neural network should be, defined by the user.
        NumberOfInputChannels:      int
                                    The number of input channels (input neurons) the neural network should have,
                                    defined by the user.
        NumberOfOutputChannels:     int
                                    The number of output channels (output neurons) the neural network should have,
                                    defined by the user.
        ScalingFactor:              float
                                    The rate that the neural network grows from the output layer to the input layer
                                    in order to maintain a trapezoidal shape.
        Filing:                     Filing
                                    The results that are stored using the Filing class for reading, writing, appending,
                                    and deleting files.
        Directory:                  str
                                    Should the user wish to define a unique directory for his/her current antenna
                                    geometry, this should be named something meaningful.
        Debugging:                  bool
                                    For debugging purposes (developer mode).

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        if NumberOfHiddenLayers is None or NumberOfOutputChannels is None:
            raise Exception('<CoarseModel: NumberOfHiddenLayers and/or NumberOfOutputChannels is of None type>')

        # Learning parameters
        self.__beta_1__ = None
        self.__beta_2__ = None
        self.__epsilon__ = None
        self.__alpha__ = None
        self.__N__ = None
        self.__init_N__ = 0
        self.__time_step__ = 0

        # Class objects
        self.__filing__ = Filing

        # Create directory for surrogate
        if Directory is None:
            self.__directory__ = ['\\Surrogate\\']
        else:
            self.__directory__ = ['\\Surrogate\\' + Directory + '\\']
        self.__files__ = [self.__directory__[0] + 'Weights']

        # Network structure
        self.__phi_k__ = NumberOfOutputChannels
        self.__d_s__ = NumberOfHiddenLayers
        if NumberOfInputChannels is not None:
            self.__s_c__ = (NumberOfInputChannels / NumberOfOutputChannels) ** (1 / (NumberOfHiddenLayers - 1))
        else:
            self.__s_c__ = ScalingFactor

        # 1D array(s)
        self.__error_k__ = [0.0 for _ in range(self.__phi_k__)]
        self.__nrmse__ = 0.0

        # 2D array(s)
        self.__neuron_array__ = []
        self.__in_j__ = []
        self.__out_j__ = []
        self.__delta__ = []

        # 3D array(s)
        __init_num_weights__ = int(round(self.__phi_k__ * self.__s_c__ ** (self.__d_s__ - 1)))
        self.__weights_array__ = [[copy.deepcopy([random.normalvariate(mu=0, sigma=1)])
                                   for _ in range(__init_num_weights__)]]
        self.__grad__ = [[copy.deepcopy([0.0]) for _ in range(__init_num_weights__)]]
        self.__mean__ = [[copy.deepcopy([0.0]) for _ in range(__init_num_weights__)]]
        self.__variance__ = [[copy.deepcopy([0.0]) for _ in range(__init_num_weights__)]]

        # Construct neural network
        for __i__ in range(self.__d_s__ - 1, -1, -1):

            # Number of neurons for layer __i__
            __num_neurons__ = int(round(self.__phi_k__ * (self.__s_c__ ** __i__), 0))

            # Since there are no weights from the output, do not append a list that
            # will have no value for the neural network
            if __i__ > 0:

                # Number of weights for the current neuron to the next layer's neurons. The plus 1 in the
                # self.__weights_array__ is for accommodating the bias weight links, which does not have
                # links into it from previous layers
                __num_neuron_weights__ = int(round(self.__phi_k__ * (self.__s_c__ ** (__i__ - 1)), 0))
                self.__weights_array__.append([
                    [copy.deepcopy(random.normalvariate(mu=0, sigma=1)) for _ in range(__num_neuron_weights__)]
                    for _ in range(__num_neurons__ + 1)])
                self.__grad__.append([
                    [0.0 for _ in range(__num_neuron_weights__)]
                    for _ in range(__num_neurons__ + 1)])
                self.__mean__.append([
                    [0.0 for _ in range(__num_neuron_weights__)]
                    for _ in range(__num_neurons__ + 1)])
                self.__variance__.append([
                    [0.0 for _ in range(__num_neuron_weights__)]
                    for _ in range(__num_neurons__ + 1)])

            # Append layer lists
            self.__neuron_array__.append([0.0 for _ in range(__num_neurons__)])
            self.__in_j__.append([0.0 for _ in range(__num_neurons__)])
            self.__out_j__.append([0.0 for _ in range(__num_neurons__)])
            self.__delta__.append([0.0 for _ in range(__num_neurons__)])

        # For debugging (developer mode)
        self.__debugging__ = Debugging

        # Extract the weights array
        if self.__filing__ is not None:
            # Create directories
            self.__filing__.CreateDirectories(Directories=self.__directory__)

            # Attempt to get stored weights
            __weights__ = self.__filing__.Read(Filename=self.__files__[0])

            # Save the weights if the file does not exist
            if not isinstance(__weights__, list) or __weights__ == -1:
                self.__filing__.Save(Filename=self.__files__[0], Lists=self.__weights_array__)

            # Initialize weights array from file read
            else:
                __temp_weights__ = copy.deepcopy(self.__weights_array__)

                # The full iteration through the read __weights__ array should match the architecture of the defined
                # neural network
                try:
                    for __i__ in range(len(__weights__)):
                        for __j__ in range(len(__weights__[__i__])):
                            for __k__ in range(len(__weights__[__i__][__j__])):
                                self.__weights_array__[__i__][__j__][__k__] = __weights__[__i__][__j__][__k__]

                # The architecture does not match the defined architecture of the neural network
                except Exception as __error__:
                    if self.__debugging__:
                        print(f'<CoarseModel: __init__: Read weights do not match the defined architecture: '
                              f'{__error__}>')
                    self.weights_array__ = __temp_weights__

    def Train(self, BatchSize=10, LearningRate=1e-3, Beta1=0.900, Beta2=0.999, Epsilon=1e-8,
              TrainingData=None, ValidationData=None, TestingData=None, NumberOfEpochs=None,
              TrainDurationMinutes=None, NRMSEConvergence=None):
        """
        Description:
        ------------
        Performs training on the neural network (optimizing the weights of the network). It expects four parameters
        as arguments, specifically the TrainingData, ValidationData, TestingData, NumberOfEpochs (optional) and/or
        TrainDurationMinutes (optional). Additionally, the user can define the convergence value should the network
        be optimized enough before termination is met.

        Parameters:
        -----------
        BatchSize:                  int
                                    The batch size used for training, which is typically 1, 2, 4, 8, 16, and 32.
        LearningRate:               float
                                    The initial learning rate for optimizing the weights of the neural network.
        Beta1:                      float
                                    The biased value for the first moment variable of the ADAM algorithm.
        Beta2:                      float
                                    The biased value for the second moment variable of the ADAM algorithm.
        Epsilon:                    float
                                    Value used to avoid division by zero in the ADAM algorithm.
        TrainingData:               list
                                    A list that contains the training data for the neural network to train on. Note that
                                    each data point/element are comprised of the input vector and the output vector.
        ValidationData:             list
                                    A list that contains the validation data for the neural network to be validated on.
                                    Note that each data point/element are comprised of the input vector and the output
                                    vector.
        TestingData:                list
                                    A list that contains the testing data for the neural network to be tested on.
                                    Note that each data point/element are comprised of the input vector and the output
                                    vector.
        NumberOfEpochs:             int
                                    The number of epochs the training is allowed for the neural network, defined by the
                                    user.
        TrainDurationMinutes:       float
                                    The amount of time, in minutes, training is allowed for the neural network, defined
                                    by the user.
        NRMSEConvergence:           float
                                    The value for the convergence that will halt the training process should the
                                    loss meet the convergence before the termination condition.

        Returns:
        --------
        Returns the training loss, validation loss, and testing loss where each element (except for the testing loss)
        is the loss for an epoch in the form of [test loss, validation loss, test loss].

        Notes:
        ------
        None.
        """

        if TrainingData is None or ValidationData is None or TestingData is None or \
                (NumberOfEpochs is None and TrainDurationMinutes is None):
            raise Exception('<CoarseModel: Train: One or more parameters are of type None>')

        # Learning parameters
        self.__beta_1__ = Beta1
        self.__beta_2__ = Beta2
        self.__epsilon__ = Epsilon
        self.__alpha__ = LearningRate
        self.__N__ = BatchSize
        self.__init_N__ = 0
        self.__time_step__ = 0

        # Reset self.__init_N__
        self.__init_N__ = 0

        # Initialize start and finish variables
        if NumberOfEpochs is not None:
            __start__ = 0
            __finish__ = NumberOfEpochs
        else:
            __start__ = 0
            __finish__ = TrainDurationMinutes

        # Arrays used for performance analysis
        __validation_loss__ = []
        __train_loss__ = []
        __test_loss__ = []

        __num_epochs__ = 0
        __elapsed_time__ = time.time() / 60

        # Temporary loss list
        __temp_loss__ = []

        for __i__ in range(len(self.__grad__)):
            for __j__ in range(len(self.__grad__[__i__])):
                for __k__ in range(len(self.__grad__[__i__][__j__])):
                    self.__grad__[__i__][__j__][__k__] = 0.0
                    self.__mean__[__i__][__j__][__k__] = 0.0
                    self.__variance__[__i__][__j__][__k__] = 0.0

        while __start__ < __finish__:

            # Loop through training data
            for __i__ in TrainingData:
                self.FeedForward(__input__=__i__[0], __target__=__i__[1], __learn__=True)
                __temp_loss__.append(self.__nrmse__)

            __train_loss__.append(copy.deepcopy(sum(__temp_loss__) / len(__temp_loss__)))
            __temp_loss__.clear()

            # Loop through validation data
            for __i__ in ValidationData:
                self.FeedForward(__input__=__i__[0], __target__=__i__[1], __learn__=False)
                __temp_loss__.append(self.__nrmse__)

            __validation_loss__.append(copy.deepcopy(sum(__temp_loss__) / len(__temp_loss__)))
            __temp_loss__.clear()

            # Either increment the number of epochs or update the timer
            if NumberOfEpochs is not None:
                __start__ += 1
            else:
                __start__ = time.time() / 60 - __elapsed_time__

            if __train_loss__[-1] > 1 or __validation_loss__[-1] > 1:
                print('\033[0;31;40m', end='')

            elif 0.3 <= __train_loss__[-1] <= 1 or 0.3 <= __validation_loss__[-1] <= 1:
                self.__alpha__ = 1e-3
                print('\033[0;33;40m', end='')

            elif 0.2 <= __train_loss__[-1] < 0.3 or 0.2 <= __validation_loss__[-1] < 0.3:
                self.__alpha__ = 1e-4
                print('\033[0;34;40m', end='')

            elif 0.1 <= __train_loss__[-1] < 0.2 or 0.1 <= __validation_loss__[-1] < 0.2:
                self.__alpha__ = 1e-5
                print('\033[0;32;40m', end='')

            else:
                print('\033[0;30;47m', end='')

            print(f'Epoch: {__num_epochs__ + 1}\t'
                  f'Train normalized RMSE = {"{:.3f}".format(__train_loss__[-1])}\t'
                  f'Validation normalized RMSE = {"{:.3f}".format(__validation_loss__[-1])}\t'
                  f'Time elapsed: {int(time.time() / 60 - __elapsed_time__)} minutes '
                  f'and {int(time.time() - __elapsed_time__ * 60) % 60} seconds\033[0m')

            __num_epochs__ += 1

            if NRMSEConvergence is not None and __train_loss__[-1] <= NRMSEConvergence and \
                    __validation_loss__[-1] <= NRMSEConvergence:
                break

        # Evaluate the network with test data
        for __i__ in TestingData:
            self.FeedForward(__input__=__i__[0], __target__=__i__[1], __learn__=False)
            __test_loss__.append(copy.deepcopy(self.__nrmse__))

        return [__train_loss__, __validation_loss__, __test_loss__]

    def FeedForward(self, __input__, __target__, __learn__=False, __return_outputs__=False):
        """
        Description:
        ------------
        Performs a feedforward operation given the input and target values. Additionally, the neural network will
        be trained if __learn__ is True. Finally, the output layer of the network is returned if __return_outputs__
        is set to True.

        Parameters:
        -----------
        __input__:                  list
                                    The input to the neural network where the output will be determined via the
                                    feedforward process.
        __target__:                 list
                                    The actual outputs that the neural network should match with.
        __learn__:                  bool
                                    Used for training the neural network. When True, the network is trained, else
                                    the network is not trained.
        __return_outputs__:         bool
                                    Used for returning the output values of the neural network when True, else the
                                    output values are not returned.

        Returns:
        --------
        Returns the output layer values, in a 1D list, should the outputs be required to be returned after a
        feedforward operation.

        Notes:
        ------
        None.
        """

        # Feed the inputs, conditioned with the activation function and bias, which will be used as initial values.
        # Remember, the bias output value is 1.0, thus only the weight of the bias is considered
        for __i__ in range(len(__input__)):

            self.__neuron_array__[0][__i__] = \
                self._activation(__input__=__input__[__i__] + self.__weights_array__[0][__i__][0])

            # Update average output of layer neuron
            self.__out_j__[0][__i__] += self.__neuron_array__[0][__i__] / self.__N__

        # Perform actual feed-forward process
        # Layer loop
        for __i__ in range(1, len(self.__neuron_array__)):
            # Neuron loop
            for __j__ in range(len(self.__neuron_array__[__i__])):
                self.__neuron_array__[__i__][__j__] = \
                    self._activation(__input__=self._summation(__layer_index__=__i__, __neuron_index__=__j__))

                # Update average output of layer neuron
                self.__out_j__[__i__][__j__] += self.__neuron_array__[__i__][__j__] / self.__N__

        self._update_loss(__target__=__target__, __learn__=__learn__)

        if __learn__:
            self.__init_N__ += 1
            if self.__init_N__ % self.__N__ == 0:
                self._update_weights()
                return

        if __return_outputs__:
            return [__i__ for __i__ in self.__neuron_array__[-1]]

    def _summation(self, __layer_index__, __neuron_index__):
        """
        Description:
        ------------
        Performs a dot product operation given the layer index and neuron index.

        Parameters:
        -----------
        __layer_index__:            int
                                    Used for pointing to the indexed layer of the neural network.
        __neuron_index__:           int
                                    Used for pointing to the indexed neuron of the neural network.

        Returns:
        --------
        Returns the result after the dot product operation.

        Notes:
        ------
        None.
        """

        __total__ = 0.0

        # The indices for both the self.__input_array__ and self.__weights_array__ are
        # the same, except for the self.__weights_array__ having an extra dimension,
        # weights that are associated with neuron n.
        for __i__ in range(len(self.__weights_array__[__layer_index__]) - 1):
            __total__ += self.__neuron_array__[__layer_index__ - 1][__i__] * \
                         self.__weights_array__[__layer_index__][__i__][__neuron_index__]

        # Add bias
        __total__ += self.__weights_array__[__layer_index__][-1][__neuron_index__]

        # Update average summation input to neuron __neuron_index__
        self.__in_j__[__layer_index__][__neuron_index__] += __total__ / self.__N__

        return __total__

    # Combines activation function and output
    @staticmethod
    def _activation(__input__):
        """
        Description:
        ------------
        Performs an activation operation given the input (__input__).

        Parameters:
        -----------
        __input__:                  float
                                    The value to perform the activation function on.

        Returns:
        --------
        Returns the result of the activation function operation.

        Notes:
        ------
        None.
        """

        return 1 / (1 + np.exp(-__input__))

    def _activation_derivative(self, __input__):
        """
        Description:
        ------------
        Performs the derivative activation operation given the input (__input__).

        Parameters:
        -----------
        __input__:                  float
                                    The value to perform the activation function on.

        Returns:
        --------
        Returns the result of the derivative activation function operation.

        Notes:
        ------
        None.
        """

        return self._activation(__input__=__input__) * (1 - self._activation(__input__=__input__))

    # Update errors
    def _update_loss(self, __target__, __learn__=True):
        """
        Description:
        ------------
        Updates the loss of the neural network and determines the error at the output layer, averaged over __N__
        (batch size).

        Parameters:
        -----------
        __target__:                 list
                                    A list that has the actual output values that the neural network should match with.
        __learn__:                  bool
                                    Updates the error of the neural network if True, else the error is left alone.

        Returns:
        --------
        None.

        Notes:
        ------
        None.
        """

        self.__nrmse__ = 0
        for __i__ in range(self.__phi_k__):
            # Update average root-mean-square error for analysis
            self.__nrmse__ += ((__target__[__i__] - self.__neuron_array__[-1][__i__]) ** 2) ** 0.5 / \
                              (max(__target__) - min(__target__))

            if __learn__:
                # Update L2 loss that will be used for calculating the gradients. The derivative of the L2 loss function
                # is dL2/d(predicted) = -2 * (target - predicted), where L2 = (target - predicted) ** 2
                self.__error_k__[__i__] += -2 * (__target__[__i__] - self.__neuron_array__[-1][__i__]) / self.__N__

    def _update_weights(self):
        """
        Description:
        ------------
        Updates the weights of the neural network given that training mode is enabled. The gradients are first updated,
        after which the two moments are updated, before the weights are updated.

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

        # Update gradients
        self._update_gradients()

        self.__time_step__ += 1

        # Update mean and variance
        self._update_mean_variance()

        # Perform the weight updates
        for __i__ in range(len(self.__weights_array__)):
            for __j__ in range(len(self.__weights_array__[__i__])):
                for __k__ in range(len(self.__weights_array__[__i__][__j__])):
                    self.__weights_array__[__i__][__j__][__k__] = self.__weights_array__[__i__][__j__][__k__] - \
                        (self.__alpha__ * (1 - self.__beta_2__ ** self.__time_step__) ** 0.5 /
                         (1 - self.__beta_1__ ** self.__time_step__)) * \
                        (self.__mean__[__i__][__j__][__k__] /
                         (self.__variance__[__i__][__j__][__k__] ** 0.5 +
                          self.__epsilon__))
                    self.__mean__[__i__][__j__][__k__] = 0.0
                    self.__variance__[__i__][__j__][__k__] = 0.0

        # Save weights
        if self.__filing__ is not None:
            self.__filing__.Save(Filename=self.__files__[0], Lists=self.__weights_array__)

    # Loss used is the mean-square-error derivative
    def _update_gradients(self):
        """
        Description:
        ------------
        Updates the gradients of the weights, averaged over __N__ (batch size). The deltas are determined before the
        gradients are updated.

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

        # Output layer
        for __i__ in range(self.__phi_k__):
            # Update delta value
            self.__delta__[-1][__i__] = self.__error_k__[__i__] * self._activation_derivative(self.__in_j__[-1][__i__])
            self.__error_k__[__i__] = 0.0

            # Update gradient values. The '-1' is for the skipping the bias neuron since it does not have an official
            # output
            for __j__ in range(len(self.__grad__[-1]) - 1):
                self.__grad__[-1][__j__][__i__] = self.__delta__[-1][__i__] * self.__out_j__[-2][__j__]

                # Clear output
                self.__out_j__[-2][__j__] = 0.0

            # Update bias gradient value
            self.__grad__[-1][-1][__i__] = self.__delta__[-1][__i__]

            # Clear input
            self.__in_j__[-1][__i__] = 0.0

        # Hidden layers
        for __i__ in range(len(self.__delta__) - 2, -1, -1):
            for __j__ in range(len(self.__delta__[__i__])):
                __sum__ = 0

                # Determine the summation of the weights and their deltas for the current neuron
                for __k__ in range(len(self.__weights_array__[__i__ + 1][__j__])):
                    __sum__ += self.__weights_array__[__i__ + 1][__j__][__k__] * self.__delta__[__i__ + 1][__k__]

                # Update current neuron's delta value
                self.__delta__[__i__][__j__] = self._activation_derivative(self.__in_j__[__i__][__j__]) * __sum__

                # Clear input
                self.__in_j__[__i__][__j__] = 0.0

                # Conditioned only for the hidden layers as there is no out_j_i from the input layer
                if __i__ > 0:
                    # Update the gradients involved with the current delta value
                    for __k__ in range(len(self.__grad__[__i__]) - 1):
                        self.__grad__[__i__][__k__][__j__] = self.__delta__[__i__][__j__] * \
                                                             self.__out_j__[__i__ - 1][__k__]
                        # Clear output
                        self.__out_j__[__i__ - 1][__k__] = 0.0

                    # Update bias gradient for delta n
                    self.__grad__[__i__][-1][__j__] = self.__delta__[__i__][__j__]

                # Conditioned when in the first hidden layer, the conditioned input layer
                else:
                    self.__grad__[0][__j__][0] = self.__delta__[__i__][__j__]

    def _update_mean_variance(self):
        """
        Description:
        ------------
        Updates the two moments of the ADAM algorithm. This is the last function called before the weights of the
        neural network are updated. The optimized variant of the ADAM algorithm is adopted for the whole process of
        optimizing the weights of the neural network.

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

        # Layer
        for __i__ in range(len(self.__grad__)):

            # Gradient array
            for __j__ in range(len(self.__grad__[__i__])):

                # Gradient element corresponding to weight element
                for __k__ in range(len(self.__grad__[__i__][__j__])):

                    # Update average of mean
                    self.__mean__[__i__][__j__][__k__] = \
                        self.__mean__[__i__][__j__][__k__] * self.__beta_1__ + \
                        (1 - self.__beta_1__) * self.__grad__[__i__][__j__][__k__]

                    # Update average of variance
                    self.__variance__[__i__][__j__][__k__] = \
                        self.__variance__[__i__][__j__][__k__] * self.__beta_2__ + \
                        (1 - self.__beta_2__) * self.__grad__[__i__][__j__][__k__] ** 2

                    # Clear gradient n
                    self.__grad__[__i__][__j__][__k__] = 0.0
