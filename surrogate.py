from AntennaDesign.__init__ import *
from AntennaDesign.Surrogate import CoarseModel
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from AntennaDesign.Filing import Filing
import tensorflow as tf

def GetNumberOfBands(s11, s11_min=-10):
        freq = s11[0]
        s11 = s11[1]
        num_bands = 0
        index = 0
        freq_bands = []
        while index < len(freq):
                if s11[index] <= s11_min:
                        freq_bands.append([freq[index]])
                        num_bands += 1
                        while index < len(freq) and s11[index] <= s11_min:
                                index += 1
                        freq_bands[-1].append(freq[index - 1])
                index += 1

        result = []
        for i in range(len(freq_bands)):
                result.append(abs(freq_bands[i][0] - 2.33) + abs(freq_bands[i][1] - 2.44))
        if len(result) > 0:
                return num_bands, freq_bands[result.index(min(result))]
        else:
                return num_bands, [-1, -1]


Parameter = [
        ['a0', -12, [-12, 'b0']],
        ['a1', 12, ['b1', 12]],
        ['b0', -10, ['a0', 'c0']],
        ['b1', 10, ['c1', 'a1']],
        ['c0', -7.5, ['b0', 'd0']],
        ['c1', 7.5, ['e1', 'b1']],
        ['d0', -4, ['c0', 'd1']],
        ['d1', -2, ['d0', 'e0']],
        ['e0', 2, ['d1', 'e1']],
        ['e1', 4, ['e0', 'c1']],
        ['f0', -0.55, [-0.55, -0.55]],
        ['f1', 0.55, [0.55, 0.55]],
        ['g0', -10, [-10, 'h0']],
        ['g1', 10, ['h1', 10]],
        ['h0', -5, ['l1', 'l1']],
        ['h1', 9, ['i1', 'g1']],
        ['i0', 5, ['j1', 'i1']],
        ['i1', 7, ['i0', 'h1']],
        ['j0', -4, ['h0', 'j1']],
        ['j1', 5, ['i0', 'i0']],
        ['k0', -4, ['h0', 'k1']],
        ['k1', 5, ['i0', 'i0']],
        ['l0', -10, [-10, -10]],
        ['l1', -5, [-5, 'h0']],
        ['m0', -12, [-12, 'f0']],
        ['m1', 12, ['f1', 12]],
        ['n0', -10, [-10, -10]],
        ['n1', -3, ['n0', 'g1']],
    ]
DataLocation = pkg_resources.files('AntennaDesign') / 'Filing\\SSO\\Pi-Slotted\\Explored'
File = open(DataLocation, 'r')
data = []
file = Filing()
surrogate = CoarseModel(NumberOfHiddenLayers=3,
                        NumberOfOutputChannels=3,
                        ScalingFactor=3.0550505,
                        Learn=True,
                        LearningInterval=3,
                        LearningRate=1e-4,
                        LeakageRatio=0.001,
                        Filing=file,
                        Directory='Pi-Slotted')
for __i__ in File.readlines():
        __first_index__ = __i__.index('[')
        __last_index__ = __i__.index('\n')
        data.append(ast.literal_eval(__i__[__first_index__: __last_index__]))

File.close()
Inputs = []
Outputs = []
for __i__ in data:
        # inputs
        Inputs.append([])
        Outputs.append([])
        for __j__ in __i__[0]:
                for __k__ in __j__[4]:
                        Inputs[-1].append(__k__[0])
                        Inputs[-1].append(__k__[1])
                        Inputs[-1].append(__k__[2])
                        Inputs[-1].append(__k__[3])
        Inputs[-1] = np.asarray(Inputs[-1])
        # outputs
        temp = GetNumberOfBands(s11_min=-10, s11=__i__[1][0])
        Outputs[-1].append(temp[0])
        Outputs[-1].append(temp[1][0])
        Outputs[-1].append(temp[1][1])
        Outputs[-1] = np.asarray(Outputs[-1])
Outputs = np.asarray(Outputs)
Inputs = np.asarray(Inputs)
training = [[], []]
validation = [[], []]
for __i__ in range(len(Inputs)):
        if __i__ < len(Inputs) / 2:
                training[0].append(Inputs[__i__])
                training[1].append(Outputs[__i__])
        else:
                validation[0].append(Inputs[__i__])
                validation[1].append(Outputs[__i__])
__start__ = time.time() / 60
__finish__ = 60 * 4
frames = 100
print(len(Inputs))
print(len(Outputs))
average = [1.0] * frames
validation_error = [1.0] * frames
print(len(Parameter))
print(len(data))
_index_ = [h for h in range(int(len(Inputs) / 2))]
# while time.time() / 60 - __start__ < __finish__:
        # i = 0
        # for __i__ in range(len(Inputs)):
        #         surrogate.FeedForward(__input__=Inputs[_index_[i]], __target__=Outputs[_index_[i]])
        #         average[0].append(surrogate.__loss__[0])
        #         average[1].append(surrogate.__loss__[1])
        #         average[2].append(surrogate.__loss__[2])
        #         print(f'\r{round(sum(average[0])/len(average[0]), 6)}\t{round(sum(average[1])/len(average[1]), 6)}\t'
        #               f'{round(sum(average[2])/len(average[2]), 6)}', end='')
        #         average[0].pop(0)
        #         average[1].pop(1)
        #         average[2].pop(2)
        #         i += 1
        #
        # _index_ = [h for h in range(len(Inputs))]
        # random.shuffle(_index_)



fig, ax = plt.subplots()


def animate(i):
        global training, validation
        i = 0
        temp = [[], [], []]
        random.shuffle(_index_)
        for __i__ in _index_:
                surrogate.FeedForward(__input__=training[0][__i__], __target__=training[1][__i__])
                temp[0].append(surrogate.__loss__[0])
                temp[1].append(surrogate.__loss__[1])
                temp[2].append(surrogate.__loss__[2])
                # print(f'\r{round(sum(average[0]) / len(average[0]), 6)}\t{round(sum(average[1]) / len(average[1]), 6)}\t'
                #       f'{round(sum(average[2]) / len(average[2]), 6)}', end='')
                i += 1
        average.pop()
        avg = (sum(temp[0]) / len(temp[0]) + sum(temp[1]) / len(temp[1]) + sum(temp[2]) / len(temp[2])) / 3
        average.insert(0, avg)
        surrogate.SetLearn(False)
        temp = [[], [], []]
        for __i__ in _index_:
                surrogate.FeedForward(__input__=validation[0][__i__], __target__=validation[1][__i__])
                temp[0].append(surrogate.__loss__[0])
                temp[1].append(surrogate.__loss__[1])
                temp[2].append(surrogate.__loss__[2])
                # print(f'\r{round(sum(average[0]) / len(average[0]), 6)}\t{round(sum(average[1]) / len(average[1]), 6)}\t'
                #       f'{round(sum(average[2]) / len(average[2]), 6)}', end='')
                i += 1
        validation_error.pop()
        avg = (sum(temp[0]) / len(temp[0]) + sum(temp[1]) / len(temp[1]) + sum(temp[2]) / len(temp[2])) / 3
        validation_error.insert(0, avg)
        surrogate.SetLearn(True)
        ax.clear()
        ax.plot(range(len(average)), average, color='black', label='Training')
        ax.plot(range(len(validation_error)), validation_error, color='red', label='Validation')
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Loss')
        ax.legend()


ani = animation.FuncAnimation(fig, animate, interval=100, frames=60)
plt.show()
