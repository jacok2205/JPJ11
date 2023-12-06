# from matplotlib import pyplot as plt
#
# file = open('C:\\Users\\Jakes-Work\\Desktop\\Lab PC Results\\Generation S11 Results\\generation_S11_results_104', 'r')
#
# brackets = 0
# data = []
# for i in file.readlines():
#     temp = ''
#     data.append([])
#     for j in i:
#         if j == '[':
#             brackets += 1
#             if brackets == 2:
#                 data[-1].append([])
#         elif j == ']':
#             brackets -= 1
#
#         elif (j.isdigit() or j == '-' or j == '.' or j == 'e') and brackets == 2:
#             temp += j
#
#         elif j == ',' or j == ']':
#             data[-1][-1].append(float(temp))
#             temp = ''
#
# freqmin = 2.0
# freqmax = 3.0
# fedgemin = 2.36
# fedgemax = 2.44
# tolerance = 0.023
# fedgemintol1 = fedgemin * (1 - tolerance)
# fedgemintol2 = fedgemin * (1 + tolerance)
# fedgemaxtol1 = fedgemax * (1 - tolerance)
# fedgemaxtol2 = fedgemax * (1 + tolerance)
# newdata = []
# for i in range(len(data)):
#     newdata.append([[], []])
#     for j in range(min(len(data[i][0]), len(data[i][1]))):
#         if freqmin <= data[i][0][j] <= freqmax:
#             newdata[-1][0].append(data[i][0][j])
#             newdata[-1][1].append(data[i][1][j])
#
# index = 0
# plt.plot(newdata[index][0], newdata[index][1])
# plt.plot([fedgemintol1, fedgemintol1], [min(newdata[index][1]), -10], color='g')
# plt.plot([fedgemintol2, fedgemintol2], [min(newdata[index][1]), -10], color='g')
# plt.plot([fedgemaxtol1, fedgemaxtol1], [min(newdata[index][1]), -10], color='b')
# plt.plot([fedgemaxtol2, fedgemaxtol2], [min(newdata[index][1]), -10], color='b')
# plt.plot([freqmin, freqmax], [-10, -10], color='k')
# # plt.show()


# import fine_model
# from fine_model import __config__
# fine_model.pdrn.__initializeNeuralNetworkStructure__()
# for __i__ in range(len(__config__.__input_array__)):
#     for __j__ in range(len(__config__.__input_array__[__i__])):
#         print(__config__.__input_array__[__i__][__j__], end=', ')
#     print()
#
# print('\n\n\n')
# print('Weights Array')
# for __i__ in range(len(__config__.__weights_array__)):
#     print(f'Layer: {__i__ + 1}')
#     for __j__ in range(len(__config__.__weights_array__[__i__])):
#         print(f'Neuron: {__j__ + 1}')
#         for __k__ in range(len(__config__.__weights_array__[__i__][__j__])):
#             print(__config__.__weights_array__[__i__][__j__][__k__], end=', ')
#         print()
# print(len(__config__.__weights_array__))
#
# print('\n\n\n')
# print(len(__config__.__bias_array__))
# print(__config__.__activation_array__)

# import file_system.file_system as fs
# fs.__delete_all_history_files__(__log_operation__=False, __module__='coarse_model', __directory_names__=['Generation Geometry', 'Generation S11 Results', 'Generation Fitness Results', 'temp'])

import coarse_model
import cst_interface
import file_system
import system_logging
