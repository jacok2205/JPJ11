# Rough implementation for fast prototyping and demonstration purposes
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
    fig0, ax0 = plt.subplots(1, 2)

    for __i__ in data:
        if __use_alpha__:
            ax0[0].plot(__i__[1][0][0], [10 ** (__j__ / 20) for __j__ in __i__[1][0][1]])
            ax0[1].plot(__i__[1][1][0], [1 / (1 + np.exp(-10 ** (__j__ / 10))) for __j__ in __i__[1][1][1]])
        else:
            avg = [__i__[__j__][0] for __j__ in range(len(__i__))]
            result.append(sum(avg) / len(avg))
            avg = [__i__[__j__][1] for __j__ in range(len(__i__))]
            result1.append(sum(avg) / len(avg))

    plt.grid()
    ax0[0].set_xlabel('Frequency (GHz)')
    ax0[0].set_ylabel('Return loss (linear)')
    ax0[1].set_xlabel('Frequency (GHz)')
    ax0[1].set_ylabel(r'$\sigma$(Gain$_{linear}$)')
    fig0.suptitle('Dataset')
    ax0[0].set_xlim(2.0, 2.8)
    ax0[0].grid()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
    refined_data = []
    for __i__ in data:
        refined_data.append([__i__[0], []])
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

    surrogate = Surrogate(NumberOfHiddenLayers=3,
                          NumberOfInputChannels=len(refined_data[0][0]),
                          NumberOfOutputChannels=len(refined_data[0][1]),
                          Debugging=True,
                          Filing=filing)
    loss1, loss2, loss3 = surrogate.Train(BatchSize=1,
                                          LearningRate=5e-5,
                                          TrainingData=refined_data[0: 250],
                                          ValidationData=refined_data[250: 260],
                                          TestingData=refined_data[260: 270],
                                          TrainDurationMinutes=0.5,
                                          NRMSEConvergence=0.001)
    test = surrogate.FeedForward(__input__=refined_data[0][0],
                                 __target__=refined_data[0][1],
                                 __learn__=False,
                                 __return_outputs__=True)
    plt.figure(1)
    plt.plot(range(len(loss1)), loss1, label='Train')
    plt.plot(range(len(loss2)), loss2, label='Validate')
    plt.legend()
    plt.grid()
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
    print(test)
    print(refined_data[0][1])
    optimizer = PSO(NumberOfParticles=1000,
                    ParameterRanges=[[21.5 - 0.5, 21.5 + 0.5],
                                     [11 - 0.5, 11 + 0.5],
                                     [9 - 0.5, 9 + 0.5],
                                     [4 - 0.5, 4 + 0.5]],
                    Objective=surrogate)
    result = optimizer.Optimize(NumberOfIterations=100,
                                Convergence=0.00001,
                                W=0.001,
                                C1=1.0,
                                C2=1.0)

    fig1, ax1 = plt.subplots(2, 1, sharex=True)
    ax1[0].semilogy(result[1])
    ax1[1].semilogx(result[2])
    ax1[0].grid()
    ax1[1].grid()
    ax1[1].set_xlabel('Iteration')
    ax1[0].set_ylabel('Return loss fitness')
    ax1[1].set_ylabel('Gain fitness')
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
