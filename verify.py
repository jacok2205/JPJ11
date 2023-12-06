from AntennaDesign.surrogate import CoarseModel
from AntennaDesign.Filing import Filing
from AntennaDesign.__init__ import *

def Verify():
    File = Filing(Directories=None, Debugging=False)
    file_path = '\\SSO\\Pi-Slotted\\Explored'
    data = File.Read(Filename=file_path)

    train_validation_ratio = 0.8
    output_reduction_factor = 2

    # [Input, Output]
    sorted_data = []
    __max_input_value__ = 0
    __range__ = [2.5, 2.7]

    for i in data:
        sorted_data.append([[], []])

        for j in i[0]:
            for k in j[4]:
                sorted_data[-1][0].append(k[0])
                sorted_data[-1][0].append(k[1])
                sorted_data[-1][0].append(k[2])
                sorted_data[-1][0].append(k[3])

                if abs(k[0]) > __max_input_value__:
                    __max_input_value__ = abs(k[0])
                if abs(k[1]) > __max_input_value__:
                    __max_input_value__ = abs(k[1])
                if abs(k[2]) > __max_input_value__:
                    __max_input_value__ = abs(k[2])
                if abs(k[3]) > __max_input_value__:
                    __max_input_value__ = abs(k[3])

        # for j in range(0, len(i[1][0][1]), output_reduction_factor):
            # Append normalized data (simply the magnitude of the return loss response --> |S11| = 10 ^ (dB_value / 20))
            # sorted_data[-1][1].append(10 ** (i[1][0][1][j] / 20))
            # sorted_data[-1][1].append(i[1][0][1][j])

        for j in range(len(i[1][0][1])):
            if __range__[0] <= i[1][0][0][j] <= __range__[1]:
                sorted_data[-1][1].append(i[1][0][1][j])

    # Normalize inputs
    # for i in range(len(sorted_data)):
    #     for j in range(len(sorted_data[i][0])):
    #         sorted_data[i][0][j] /= __max_input_value__

    num_inputs = len(sorted_data[0][0])
    num_outputs = len(sorted_data[0][1])

    # print(f'Number of inputs: {num_inputs}')
    # print(f'Number of outputs: {num_outputs}')

    train_data = []
    validation_data = []

    for i in sorted_data:
        if np.random.choice([True, False]) and len(validation_data) < len(sorted_data) * (1 - train_validation_ratio):
            validation_data.append(i)
        else:
            train_data.append(i)

    # surrogate = CoarseModel(NumberOfHiddenLayers=4, NumberOfInputChannels=num_inputs, NumberOfOutputChannels=num_outputs, LearningRate=1e-4, LeakageRatio=0.02, LearningInterval=1)
    # train, validation = surrogate.Train(TrainingData=train_data, ValidationData=validation_data, NumberOfEpochs=None, TrainDurationMinutes=3)
    # print(len(train))
    # print(len(validation))

    # plt.figure(1)
    # plt.plot(range(len(train)), train)
    # plt.plot(range(len(validation)), validation)
    # plt.show()
    # choose = 0
    # for i in range(len(train_data)):
    #     for j in range(len(train_data[i][1])):
    #         if train_data[i][1][j] <= -10:
    #             choose = i
    # surrogate.FeedForward(__input__=train_data[choose][0], __target__=train_data[choose][1])
    # plt.plot(range(len(surrogate.__neuron_array__[-1])), surrogate.__neuron_array__[-1])
    # plt.plot(range(len(train_data[choose][1])), train_data[choose][1])
    # plt.show()
    file = open('AntennaDesign/Filing/SSO/Pi-Slotted/Explored', 'r')
    data = []
    for i in file.readlines():
        __first_index__ = i.index('[')
        __last_index__ = i.index('\n')
        data.append(ast.literal_eval(i[__first_index__: __last_index__]))
    file.close()

    plt.figure(1)
    index = -3
    # plt.plot(data[index][1][0][0], data[index][1][0][1])
    # plt.plot(data[index][1][1][0], data[index][1][1][1])

    refined_data = []

    for i in data:
        j = 0
        while j < len(i[1][0][0]):
            if 2.45 <= i[1][0][0][j] <= 2.65 and i[1][0][1][j] <= -10:
                while j < len(i[1][0][0]) and i[1][0][1][j] <= -10 and 2.45 <= i[1][0][0][j] <= 2.65:
                    j += 1
                j -= 1
                if i[1][0][1][j] <= -10 and i[1][0][0][j] <= 2.65:
                    # plt.plot(i[1][0][0], i[1][0][1])
                    refined_data.append(i)
                    k = 0
                    while k < len(refined_data[-1][1][0][0]):
                        if 2.4 > refined_data[-1][1][0][0][k] or refined_data[-1][1][0][0][k] > 2.7:
                            refined_data[-1][1][0][0].pop(k)
                            refined_data[-1][1][0][1].pop(k)
                        else:
                            k += 1
                    j = len(i[1][0][0])
                    plt.plot(refined_data[-1][1][0][0], refined_data[-1][1][0][1])
            j += 1

    train_data = []
    validation_data = []
    for i in refined_data:
        if len(train_data) <= len(refined_data) * train_validation_ratio:   # 0.5
            # get inputs
            inp = []
            for j in i[0]:
                for k in j[4]:
                    inp.append(k[0])
                    inp.append(k[1])
                    inp.append(k[2])
                    inp.append(k[3])
            freq_response = [i[1][0][1][j] for j in range(0, len(i[1][0][1]), 1)]
            train_data.append([freq_response, inp])
        else:
            inp = []
            for j in i[0]:
                for k in j[4]:
                    inp.append(k[0])
                    inp.append(k[1])
                    inp.append(k[2])
                    inp.append(k[3])
            freq_response = [i[1][0][1][j] for j in range(0, len(i[1][0][1]), 1)]
            validation_data.append([freq_response, inp])

    print(f'Number of inputs: {len(train_data[0][0])}')
    print(f'Number of outputs: {len(train_data[0][1])}')

    plt.show()

    surrogate = CoarseModel(NumberOfHiddenLayers=5, NumberOfInputChannels=len(train_data[0][0]),
                            NumberOfOutputChannels=len(train_data[0][1]),
                            LearningRate=1e-4,
                            LeakageRatio=0.02, BatchSize=4)
    train, validation = surrogate.Train(TrainingData=train_data, ValidationData=validation_data,
                                        NumberOfEpochs=None, TrainDurationMinutes=20, RRMSEConvergence=0.055)
    print(len(train_data))
    print(len(validation_data))


def convert(imgf, labelf, outf, n):
    f = open(imgf, "rb")
    o = open(outf, "w")
    l = open(labelf, "rb")

    f.read(16)
    l.read(8)
    images = []

    for i in range(n):
        image = [ord(l.read(1))]
        for j in range(28*28):
            image.append(ord(f.read(1)))
        images.append(image)

    for image in images:
        o.write(",".join(str(pix) for pix in image)+"\n")
    f.close()
    o.close()
    l.close()

def show_image(image, shape, label="", cmp=None):
    img = np.reshape(image,shape)
    plt.imshow(img,cmap=cmp, interpolation='none')
    plt.title(label)


def count_exemple_per_digit(exemples):
    hist = np.ones(10)

    for y in exemples:
        hist[y] += 1

    colors = []
    for i in range(10):
        colors.append(plt.get_cmap('viridis')(np.random.uniform(0.0,1.0,1)[0]))

    bar = plt.bar(np.arange(10), hist, 0.8, color=colors)

    plt.grid()
    plt.show()


def normalization(x, mu, sigma):
    x_norm = np.zeros_like(x)

    for n in range(len(x)):
        for j in range(len(x[n])):
            if (sigma[j] != 0):
                x_norm[n, j] = (x[n, j] - mu[j]) / sigma[j]
            else:
                x_norm[n, j] = 0

    return x_norm

if __name__ == '__main__':
    # import matplotlib.pyplot as plt
    # import pandas as pd
    # import numpy as np
    # import time
    # import sys
    # import warnings
    # warnings.filterwarnings("ignore")
    # seed = 782
    # np.random.seed(seed)
    #
    # convert("train-images.idx3-ubyte", "train-labels.idx1-ubyte",
    #         "mnist_train.csv", 60000)
    # convert("t10k-images.idx3-ubyte", "t10k-labels.idx1-ubyte",
    #         "mnist_test.csv", 10000)
    #
    # # 1
    # df = pd.read_csv("mnist_train.csv")
    # # train = df.as_matrix()
    # train = df.to_numpy()
    # train_y = train[:, 0].astype('int8')
    # train_x = train[:, 1:].astype('float64')
    # train = None
    # print("Shape Train Images: (%d,%d)" % train_x.shape)
    # print("Shape Labels: (%d)" % train_y.shape)
    #
    # # 2
    # df = pd.read_csv("mnist_test.csv")
    # test = df.to_numpy().astype('float64')
    # print("Shape Test Images: (%d,%d)" % test.shape)
    #
    # # 3
    # # plt.figure(figsize=(12, 10))
    # # y, x = 5, 10
    # # for i in range(0, (y * x)):
    # #     plt.subplot(y, x, i + 1)
    # #     ni = np.random.randint(0, train_x.shape[0], 1)[0]
    # #     show_image(train_x[ni], (28, 28), train_y[ni], cmp="gray")
    # # plt.show()
    #
    # # 4
    # # count_exemple_per_digit(train_y)
    #
    # # 5
    # mu = np.mean(train_x, axis=0)
    # sigma = np.max(train_x, axis=0) - np.min(train_x, axis=0)
    # test = normalization(test, mu, sigma)
    # train_x = normalization(train_x, mu, sigma)
    # print("Test Min: %.2f" % np.min(test))
    # print("Test Max: %.2f" % np.max(test))
    # print("Train Min: %.2f" % np.min(train_x))
    # print("Train Max: %.2f" % np.max(train_x))

    Verify()
