from AntennaDesign.__init__ import *


class CoarseModel:
    def __init__(self, NumberOfHiddenLayers=None, NumberOfInputChannels=None, NumberOfOutputChannels=None,
                 Learn=True, BatchSize=10, LearningRate=1e-3, Beta1=0.900, Beta2=0.999, Epsilon=1e-8,
                 ScalingFactor=1.5, LeakageRatio=0.3, ValidationAccuracy=0.8,
                 Filing=None, Directory=None, Debugging=False):
        if NumberOfHiddenLayers is None or NumberOfOutputChannels is None:
            raise Exception('<pdrn: NumberOfHiddenLayers or NumberOfOutputChannels not defined>')

        # Class objects
        self.__filing__ = Filing

        self.__debugging__ = Debugging

        if Directory is None:
            self.__directory__ = ['\\Surrogate\\']
        else:
            self.__directory__ = ['\\Surrogate\\' + Directory + '\\']
        self.__files__ = [self.__directory__[0] + 'Configuration',
                          self.__directory__[0] + 'Weights']

        # Network structure
        self.__phi_k__ = NumberOfOutputChannels
        self.__d_s__ = NumberOfHiddenLayers
        if NumberOfInputChannels is not None:
            self.__s_c__ = (NumberOfInputChannels / NumberOfOutputChannels) ** (1 / (NumberOfHiddenLayers - 1))
        else:
            self.__s_c__ = ScalingFactor

        # Activation parameters
        self.__leakage_ratio__ = LeakageRatio

        # Learning parameters
        self.__learn__ = Learn
        self.__beta_1__ = Beta1
        self.__beta_2__ = Beta2
        self.__epsilon__ = Epsilon
        self.__alpha__ = LearningRate
        self.__N__ = BatchSize
        self.__init_N__ = 0

        # Modeling accuracy
        self.__accuracy__ = ValidationAccuracy

        # 1D array(s)
        self.__error_k__ = [0.0 for _ in range(self.__phi_k__)]
        self.__rrmse__ = 0

        # 2D array(s)
        self.__neuron_array__ = []
        self.__in_j__ = []
        self.__out_j__ = []
        self.__delta__ = []

        # 3D array(s)
        __init_num_weights__ = int(round(self.__phi_k__ * self.__s_c__ ** (self.__d_s__ - 1)))
        self.__weights_array__ = [[[random.normalvariate(mu=0, sigma=1)] for _ in range(__init_num_weights__)]]
        self.__grad__ = [[[0.0] for _ in range(__init_num_weights__)]]
        self.__mean__ = [[[0.0] for _ in range(__init_num_weights__)]]
        self.__variance__ = [[[0.0] for _ in range(__init_num_weights__)]]

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
                self.__weights_array__.append([[random.normalvariate(mu=0, sigma=1) for _ in range(__num_neuron_weights__)] for _ in range((__num_neurons__ + 1))])
                self.__grad__.append([[0.0 for _ in range(__num_neuron_weights__)] for _ in range((__num_neurons__ + 1))])
                self.__mean__.append([[0.0 for _ in range(__num_neuron_weights__)] for _ in range((__num_neurons__ + 1))])
                self.__variance__.append([[0.0 for _ in range(__num_neuron_weights__)] for _ in range((__num_neurons__ + 1))])

            # Append layer lists
            self.__neuron_array__.append([0.0] * __num_neurons__)
            self.__in_j__.append([0.0 for _ in range(__num_neurons__)])
            self.__out_j__.append([0.0 for _ in range(__num_neurons__)])
            self.__delta__.append([0.0 for _ in range(__num_neurons__)])

        # Structure of network
        __structure__ = [
            self.__phi_k__,             # Number of outputs
            self.__s_c__,               # Scaling factor
            self.__d_s__,               # Number of hidden layers
            self.__beta_1__,            # ADAM constant 1
            self.__beta_2__,            # ADAM constant 2
            self.__epsilon__,           # ADAM constant 3
        ]

        if self.__filing__ is not None:
            # Create directories
            self.__filing__.CreateDirectories(Directories=self.__directory__)

            # Save the structure
            self.__filing__.Save(Filename=self.__files__[0], Lists=__structure__)

            # Attempt to get stored weights
            __weights__ = self.__filing__.Read(Filename=self.__files__[1])

            # Save the weights if the file does not exist
            if not isinstance(__weights__, list) or __weights__ == -1:
                self.__filing__.Save(Filename=self.__files__[1], Lists=self.__weights_array__)

            # Initialize weights array from file read
            else:
                self.weights_array__ = __weights__

    def Train(self, TrainingData=None, ValidationData=None, NumberOfEpochs=None, TrainDurationMinutes=None,
              RRMSEConvergence=None):
        if TrainingData is None or ValidationData is None or (NumberOfEpochs is None and TrainDurationMinutes is None):
            raise Exception('<CoarseModel: Train: One or more parameters are of type None>')

        if NumberOfEpochs is not None:
            __start__ = 0
            __finish__ = NumberOfEpochs
        else:
            __start__ = 0
            __finish__ = TrainDurationMinutes

        # Arrays used for performance analysis
        __train_loss__ = []
        __validation_loss__ = []

        __num_epochs__ = 0
        __elapsed_time__ = time.time() / 60

        while __start__ < __finish__:

            # Enable learning
            self.SetLearn(Value=True)

            # Temporary loss list
            __temp_loss__ = []

            # Loop through training data
            for __i__ in TrainingData:
                self.FeedForward(__input__=__i__[0], __target__=__i__[1])
                __temp_loss__.append(self.__rrmse__)

            __train_loss__.append(sum(__temp_loss__) / len(__temp_loss__))
            __temp_loss__.clear()

            # Disable Learning
            self.SetLearn(Value=False)

            # Loop through validation data
            for __i__ in ValidationData:
                self.FeedForward(__input__=__i__[0], __target__=__i__[1])
                __temp_loss__.append(self.__rrmse__)

            __validation_loss__.append(sum(__temp_loss__) / len(__temp_loss__))

            # Shuffle training data and validation data
            random.shuffle(TrainingData)
            random.shuffle(ValidationData)

            if NumberOfEpochs is not None:
                __start__ += 1
            else:
                __start__ = time.time() / 60 - __elapsed_time__

            if __train_loss__[-1] > 1 or __validation_loss__[-1] > 1:
                print('\033[0;31;40m', end='')
            elif 0.3 <= __train_loss__[-1] <= 1 or 0.3 <= __validation_loss__[-1] <= 1:
                print('\033[0;33;40m', end='')
            elif 0.2 <= __train_loss__[-1] < 0.3 or 0.2 <= __validation_loss__[-1] < 0.3:
                print('\033[0;34;40m', end='')
            elif 0.1 <= __train_loss__[-1] < 0.2 or 0.1 <= __validation_loss__[-1] < 0.2:
                print('\033[0;32;40m', end='')
            else:
                print('\033[0;30;47m', end='')
            print(f'Epoch = {__num_epochs__ + 1}\t'
                  f'Train relative RMSE = {"{:.3f}".format(__train_loss__[-1])}\t'
                  f'Validation relative RMSE = {"{:.3f}".format(__validation_loss__[-1])}\t'
                  f'Time elapsed: {int(time.time() / 60 - __elapsed_time__)} minutes '
                  f'and {int(time.time() - __elapsed_time__ * 60) % 60} seconds\033[0m')
            __num_epochs__ += 1

            if RRMSEConvergence is not None and __train_loss__[-1] < RRMSEConvergence and \
                    __validation_loss__[-1] < RRMSEConvergence:
                break

        self.__init_N__ = 0

        return [__train_loss__, __validation_loss__]

    def SetLearn(self, Value=None):
        if Value is None or not isinstance(Value, bool):
            return
        self.__learn__ = Value

    def SetWeights(self, Weights=None):
        if Weights is None:
            return
        self.__weights_array__ = Weights

    def FeedForward(self, __input__, __target__):

        # Feed the inputs, conditioned with the activation function and bias, which will be used as initial values.
        # Remember, the bias output value is 1.0, thus only the weight of the bias is considered
        for __i__ in range(len(__input__)):

            self.__neuron_array__[0][__i__] = \
                self._activation(__input__=__input__[__i__] + self.__weights_array__[0][__i__][0])

            # Update average output of layer neuron
            self.__out_j__[0][__i__] = \
                self.__out_j__[0][__i__] + \
                (self.__neuron_array__[0][__i__] - self.__out_j__[0][__i__]) / self.__N__

        # Perform actual feed-forward process
        # Layer loop
        for __i__ in range(1, len(self.__neuron_array__)):
            # Neuron loop
            for __j__ in range(len(self.__neuron_array__[__i__])):
                self.__neuron_array__[__i__][__j__] = \
                    self._activation(__input__=self._summation(__layer_index__=__i__, __neuron_index__=__j__))

                # Update average output of layer neuron
                self.__out_j__[__i__][__j__] = \
                    self.__out_j__[__i__][__j__] + \
                    (self.__neuron_array__[__i__][__j__] - self.__out_j__[__i__][__j__]) / self.__N__

        self._update_loss(__target__=__target__)
        self.__init_N__ += 1

        if self.__init_N__ % self.__N__ == 0 and self.__learn__:
            self._update_weights(__time_step__=self.__init_N__)

    def _summation(self, __layer_index__, __neuron_index__):
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
        self.__in_j__[__layer_index__][__neuron_index__] = \
            self.__in_j__[__layer_index__][__neuron_index__] + \
            (__total__ - self.__in_j__[__layer_index__][__neuron_index__]) / self.__N__

        return __total__

    # Combines activation function and output
    def _activation(self, __input__):
        return __input__ if __input__ >= 0 else self.__leakage_ratio__ * __input__

    def _loss(self, __expected__, __actual_index__):
        return (__expected__ - self.__neuron_array__[-1][__actual_index__]) ** 2

    # Update errors
    def _update_loss(self, __target__):
        self.__rrmse__ = 0
        __numerator__ = 0
        __target_mean__ = sum(__target__) / len(__target__)
        for __i__ in range(self.__phi_k__):
            # Update average root-mean-square error for analysis
            self.__rrmse__ += (__target__[__i__] - self.__neuron_array__[-1][__i__]) ** 2
            __numerator__ += (self.__neuron_array__[-1][__i__] - __target_mean__) ** 2

            if self.__learn__:
                # Update L2 loss that will be used for calculating the gradients. The derivative of the L2 loss function
                # is dL2/d(predicted) = -2 * (target - predicted), where L2 = (target - predicted) ** 2
                self.__error_k__[__i__] += -1 * (__target__[__i__] - self.__neuron_array__[-1][__i__]) / self.__N__

        self.__rrmse__ = (self.__rrmse__ / self.__phi_k__) ** 0.5 / (__numerator__ / self.__phi_k__) ** 0.5

    def _update_weights(self, __time_step__):

        # Update gradients
        self._update_gradients()

        # Update mean and variance
        self._update_mean_variance()

        # Perform the weight updates
        for __i__ in range(len(self.__weights_array__)):
            for __j__ in range(len(self.__weights_array__[__i__])):
                for __k__ in range(len(self.__weights_array__[__i__][__j__])):
                    self.__weights_array__[__i__][__j__][__k__] -=\
                        (self.__alpha__ * (1 - self.__beta_2__ ** __time_step__) ** 0.5 /
                         (1 - self.__beta_1__)) * (self.__mean__[__i__][__j__][__k__] /
                                                   (self.__variance__[__i__][__j__][__k__] ** 0.5 +
                                                    self.__epsilon__))
                    self.__mean__[__i__][__j__][__k__] = 0
                    self.__variance__[__i__][__j__][__k__] = 0

        # Save weights
        if self.__filing__ is not None:
            self.__filing__.Save(Filename=self.__files__[1], Lists=self.__weights_array__)

    def _activation_derivative(self, __input__):
        return 1 if __input__ >= 0 else self.__leakage_ratio__

    # Loss used is the mean-square-error derivative
    def _update_gradients(self):

        # Output layer
        for __i__ in range(self.__phi_k__):
            # Update delta value
            self.__delta__[-1][__i__] = self.__error_k__[__i__] * self._activation_derivative(self.__in_j__[-1][__i__])
            self.__error_k__[__i__] = 0

            # Update gradient values. The '-1' is for the skipping the bias neuron since it does not have an official
            # output
            for __j__ in range(len(self.__grad__[-1]) - 1):
                self.__grad__[-1][__j__][__i__] = self.__delta__[-1][__i__] * self.__out_j__[-2][__j__]

            # Update bias gradient value
            self.__grad__[-1][-1][__i__] = self.__delta__[-1][__i__]

        # Hidden layers
        for __i__ in range(len(self.__delta__) - 2, -1, -1):
            for __j__ in range(len(self.__delta__[__i__])):
                __sum__ = 0

                # Determine the summation of the weights and their deltas for the current neuron
                for __k__ in range(len(self.__weights_array__[__i__ + 1][__j__])):
                    __sum__ += self.__weights_array__[__i__ + 1][__j__][__k__] * self.__delta__[__i__ + 1][__k__]

                # Update current neuron's delta value
                self.__delta__[__i__][__j__] = self._activation_derivative(self.__in_j__[__i__][__j__]) * __sum__

                # Conditioned only for the hidden layers as there is no out_j_i from the input layer
                if __i__ > 0:
                    # Update the gradients involved with the current delta value
                    for __k__ in range(len(self.__grad__[__i__]) - 1):
                        self.__grad__[__i__][__k__][__j__] = self.__delta__[__i__][__j__] * \
                                                             self.__out_j__[__i__ - 1][__k__]

                    # Update bias gradient for delta n
                    self.__grad__[__i__][-1][__j__] = self.__delta__[__i__][__j__]

                # Conditioned when in the first hidden layer, the conditioned input layer
                else:
                    self.__grad__[0][__j__][0] = self.__delta__[__i__][__j__]

    def _update_mean_variance(self):
        # Layer
        for __i__ in range(len(self.__grad__)):

            # Gradient array
            for __j__ in range(len(self.__grad__[__i__])):

                # Gradient element corresponding to weight element
                for __k__ in range(len(self.__grad__[__i__][__j__])):

                    # Update average of mean
                    self.__mean__[__i__][__j__][__k__] = \
                        self.__mean__[__i__][__j__][__k__] * self.__beta_1__ +\
                        (1 - self.__beta_1__) * self.__grad__[__i__][__j__][__k__]

                    # Update average of variance
                    self.__variance__[__i__][__j__][__k__] = \
                        self.__variance__[__i__][__j__][__k__] * self.__beta_2__ + \
                        (1 - self.__beta_2__) * self.__grad__[__i__][__j__][__k__] ** 2

                    # Reset gradient n
                    self.__grad__[__i__][__j__][__k__] = 0
