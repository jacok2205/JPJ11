# Imports
from AntennaDesign.filing import Filing
from AntennaDesign.__init__ import *
from AntennaDesign.surrogate import CoarseModel as Surrogate
from AntennaDesign.pso import PSO

# Used for having no alpha value (see through) to fully solid whilst plotting
__use_alpha__ = True

plt.rcParams['font.size'] = 24
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.style'] = 'normal'

if __name__ == '__main__':
    filing = Filing(Debugging=True)
    data = filing.Read(Filename='\\Surrogate\\lhs0')
    max_alpha = 0
    result = []
    result1 = []

    for __i__ in data:
        if __use_alpha__:
            plt.plot(__i__[1][0][0], __i__[1][0][1])
        else:
            avg = [__i__[__j__][0] for __j__ in range(len(__i__))]
            result.append(sum(avg) / len(avg))
            avg = [__i__[__j__][1] for __j__ in range(len(__i__))]
            result1.append(sum(avg) / len(avg))

    plt.grid()
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.show()
    refined_data = []
    for __i__ in data:
        refined_data.append([__i__[0], []])
        # for __j__ in range(len(refined_data[-1][0])):
        #     refined_data[-1][0][__j__] /= 22.5
        __j__ = 0
        while __j__ < len(__i__[1][0][0]):
            if __i__[1][0][1][__j__] <= -10:
                refined_data[-1][1].append(__i__[1][0][0][__j__] / 10)
                min_rl = __i__[1][0][1][__j__]
                while __j__ < len(__i__[1][0][0]) and __i__[1][0][1][__j__] < -10:
                    if min_rl > __i__[1][0][1][__j__]:
                        min_rl = __i__[1][0][1][__j__]
                    __j__ += 1
                refined_data[-1][1].append(__i__[1][0][0][__j__] / 10)
                refined_data[-1][1].append(10 ** (min_rl / 20))
            else:
                __j__ += 1
        if len(refined_data[-1][1]) == 0:
            # refined_data[-1][1] = [0, 0, 1, 0.5]
            refined_data.pop(-1)
        else:
            __j__ = 0
            gain = [__i__[1][1][1][__j__]]
            while __j__ < len(__i__[1][1][0]):
                if refined_data[-1][1][0] <= __i__[1][1][0][__j__] <= refined_data[-1][1][1]:
                    gain.append(__i__[1][1][1][__j__])
                __j__ += 1
            refined_data[-1][1].append(1 / (1 + np.exp(-1 * 10 ** ((sum(gain) / len(gain)) / 10))))
            print(refined_data[-1])
    print(refined_data[0])
    plt.plot(refined_data[0][1])
    plt.plot(data[0][1][1][1])
    plt.show()
    surrogate = Surrogate(NumberOfHiddenLayers=3, NumberOfInputChannels=len(refined_data[0][0]), NumberOfOutputChannels=len(refined_data[0][1]), Debugging=True, Filing=filing)
    # loss1, loss2, loss3 = surrogate.Train(BatchSize=1, LearningRate=1e-4, TrainingData=refined_data[0: 250], ValidationData=refined_data[250: 260], TestingData=refined_data[260: 270], TrainDurationMinutes=0.5, NRMSEConvergence=0.001)
    test = surrogate.FeedForward(__input__=refined_data[0][0], __target__=refined_data[0][1], __learn__=False, __return_outputs__=True)
    print(test)
    print(refined_data[0][1])
    optimizer = PSO(NumberOfParticles=12, ParameterRanges=[[21.5 - 0.5, 21.5 + 0.5], [11 - 0.5, 11 + 0.5], [9 - 0.5, 9 + 0.5], [4 - 0.5, 4 + 0.5]],
                    Objective=surrogate)
    result = optimizer.Optimize(NumberOfIterations=1000, Convergence=0.0001, W=0.01, C1=1.0, C2=1.0)
    print(result[0])
    plt.plot(result[1])
    plt.plot(result[2])
    plt.show()
    # plt.plot(loss1, label='Train')
    # plt.plot(loss2, label='Validate')
    # plt.grid()
    # plt.legend()
    # plt.xlabel('Epoch')
    # plt.ylabel('Loss')
    # print(sum(loss3) / len(loss3))
    # plt.show()
    # test = [-np.log(1 / __i__ - 1) for __i__ in test]
    # test = [__i__ for __i__ in test]
    # linear = [10 ** (data[0][1][0][1][__i__] / 20) for __i__ in range(len(data[0][1][0][0])) if 2.2 <= data[0][1][0][0][__i__] <= 2.6]
    # plt.plot(np.linspace(2.2, 2.6, len(linear)), linear, label='Target')
    # plt.plot(np.linspace(2.2, 2.6, len(linear)), test, 'o', alpha=0.3, label='Surrogate')
    # plt.grid()
    # plt.xlabel('Frequency (GHz)')
    # plt.ylabel('Return Loss (linear)')
    # plt.title('Frequency (GHz) vs Return Loss (linear)')
    # plt.legend()
    # plt.show()
    # plt.plot(loss1, label='Train')
    # plt.plot(loss2, label='Validate')
    # print(sum(loss3) / len(loss3))
    # plt.legend()
    # plt.show()


