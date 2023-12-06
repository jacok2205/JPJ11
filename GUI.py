from PyQt5 import QtWidgets, uic, QtCore
import sys
from AntennaDesign.__init__ import *
from AntennaDesign.Filing import Filing
from AntennaDesign.Surrogate import CoarseModel


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        # Load the .ui file
        uic.loadUi("C:\\Users\\\Jakes-Work\\\Desktop\\\JPJ11_ver_1.0\\\JPJ11\\\JPJ11_GUI.ui", self)

        self.__location__ = pkg_resources.files('AntennaDesign') / 'Filing\\SSO\\Pi-Slotted\\Explored'
        self.__data__ = []

        File = open(self.__location__, 'r')
        self.__filing__ = Filing()
        self.__surrogate__ = CoarseModel(NumberOfHiddenLayers=3,
                                         NumberOfInputChannels=28,
                                         NumberOfOutputChannels=1001,
                                         Learn=True,
                                         LearningInterval=3,
                                         LearningRate=1e-3,
                                         LeakageRatio=0.001,
                                         Filing=self.__filing__,
                                         Directory='Pi-Slotted')
        for __i__ in File.readlines():
            __first_index__ = __i__.index('[')
            __last_index__ = __i__.index('\n')
            self.__data__.append(ast.literal_eval(__i__[__first_index__: __last_index__]))
        File.close()
        self.__inputs__ = []
        self.__outputs__ = []
        for __i__ in self.__data__:

            # inputs
            self.__inputs__.append([])
            self.__outputs__.append([])

            for __j__ in __i__[0]:
                for __k__ in __j__[4]:
                    self.__inputs__[-1].append(__k__[0])
                    self.__inputs__[-1].append(__k__[1])
                    self.__inputs__[-1].append(__k__[2])
                    self.__inputs__[-1].append(__k__[3])
            self.__inputs__[-1] = np.asarray(self.__inputs__[-1])

            # outputs
            # self.__num_bands__ = self.GetNumberOfBands(s11_min=-10, s11=__i__[1][0])
            # self.__outputs__[-1].append(self.__num_bands__[0])
            # self.__outputs__[-1].append(self.__num_bands__[1][0])
            # self.__outputs__[-1].append(self.__num_bands__[1][1])
            self.__outputs__[-1].append(__i__[1][0][1])
            self.__outputs__[-1] = np.asarray(self.__outputs__[-1][-1])

        self.__outputs__ = np.asarray(self.__outputs__)
        self.__inputs__ = np.asarray(self.__inputs__)
        self.__training__ = [[], []]
        self.__validation__ = [[], []]

        for __i__ in range(len(self.__inputs__)):
            if __i__ < len(self.__inputs__) / 2:
                self.__training__[0].append(self.__inputs__[__i__])
                self.__training__[1].append(self.__outputs__[__i__])
            else:
                self.__validation__[0].append(self.__inputs__[__i__])
                self.__validation__[1].append(self.__outputs__[__i__])

        self.__train_error__ = [1.0 for _ in range(100)]
        self.__validation_error__ = [1.0 for _ in range(100)]

        self.__data_index__ = [__i__ for __i__ in range(int(len(self.__inputs__) / 2))]

        self.__freq__ = None
        self.__s11__ = None
        self.__timer__ = QtCore.QTimer()
        self.__nn_timer__ = QtCore.QTimer()
        self.__nn_timer__.timeout.connect(self.PDRNNetwork)
        self.__nn_timer__.start(50)
        self.__updated__ = False
        self.__timer__.timeout.connect(self.UpdateGraph)
        self.__timer__.start(50)
        self.__pdrn__ = [self.PDRN.plot(range(len(self.__train_error__)), self.__train_error__, pen='r'),
                         self.PDRN.plot(range(len(self.__validation_error__)), self.__validation_error__, pen='g')]
        self.PDRN.setLabel('left', 'RMSE')
        self.show()

    def PDRNNetwork(self):
        if not self.__updated__:
            __index__ = 0
            __temp__ = []
            random.shuffle(self.__data_index__)
            for __i__ in self.__data_index__:
                self.__surrogate__.FeedForward(__input__=self.__training__[0][__i__], __target__=self.__training__[1][__i__])
                for __j__ in self.__surrogate__.__loss__:
                    __temp__.append(__j__)
                __index__ += 1
            self.__train_error__.pop()
            __avg__ = sum(__temp__) / len(__temp__)
            self.__train_error__.insert(0, __avg__)
            self.__surrogate__.SetLearn(False)
            __temp__ = []
            for __i__ in self.__data_index__:
                self.__surrogate__.FeedForward(__input__=self.__validation__[0][__i__], __target__=self.__validation__[1][__i__])
                for __j__ in self.__surrogate__.__loss__:
                    __temp__.append(__j__)
                __index__ += 1
            self.__validation_error__.pop()
            __avg__ = sum(__temp__) / len(__temp__)
            self.__validation_error__.insert(0, __avg__)
            self.__surrogate__.SetLearn(True)
            temp = self.__training__
            self.__training__ = self.__validation__
            self.__validation__ = temp
            self.__updated__ = True
            print(f'\r{sum(self.__validation_error__)/len(self.__validation_error__)}\t{min(self.__validation_error__)}\t{max(self.__validation_error__)}', end='')

    def UpdateGraph(self):
        if self.__updated__:
            self.__pdrn__[0].setData(range(len(self.__train_error__)), self.__train_error__)
            self.__pdrn__[1].setData(range(len(self.__validation_error__)), self.__validation_error__)
            self.__updated__ = False

    def GetNumberOfBands(self, s11, s11_min=-10):
        self.__freq__ = s11[0]
        self.__s11__ = s11[1]
        num_bands = 0
        index = 0
        freq_bands = []
        while index < len(self.__freq__):
            if self.__s11__[index] <= s11_min:
                freq_bands.append([self.__freq__[index]])
                num_bands += 1
                while index < len(self.__freq__) and self.__s11__[index] <= s11_min:
                    index += 1
                freq_bands[-1].append(self.__freq__[index - 1])
            index += 1
        result = []
        for i in range(len(freq_bands)):
            result.append(abs(freq_bands[i][0] - 2.33) + abs(freq_bands[i][1] - 2.44))
        if len(result) > 0:
            return num_bands, freq_bands[result.index(min(result))]
        else:
            return num_bands, [-1, -1]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
