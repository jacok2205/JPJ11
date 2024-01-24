from matplotlib import pyplot as plt
import numpy as np

plt.rcParams['font.size'] = 24
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.style'] = 'normal'

file = open('cross_pol_2_3.txt', 'r')
found = False
freq = []
s11 = []
freq_2_3 = []
freq_2_34 = []
freq_2_38 = []
freq_2_4 = []
freq_2_44 = []
freq_2_5 = []
angle = []
# for __i__ in file.readlines():
#     if not found:
#         space = 0
#         for __j__ in __i__:
#             if __j__ == ' ':
#                 space += 1
#         if space + 1 == len(__i__):
#             found = True
#
#     elif found:
#         elements = 13
#         number = ''
#         for __j__ in __i__:
#             if __j__ == '-' or __j__.isdigit() or __j__ == '.':
#                 number += __j__
#             else:
#                 if number.__contains__('.'):
#                     try:
#                         if elements == 13:
#                             angle.append(float(number))
#                         elif elements == 12:
#                             freq_2_3.append(float(number))
#                         elif elements == 10:
#                             freq_2_34.append(float(number))
#                         elif elements == 8:
#                             freq_2_38.append(float(number))
#                         elif elements == 6:
#                             freq_2_4.append(float(number))
#                         elif elements == 4:
#                             freq_2_44.append(float(number))
#                         elif elements == 2:
#                             freq_2_5.append(float(number))
#
#                         elements -= 1
#                         number = ''
#
#                     except:
#                         pass
#                 else:
#                     number = ''
#         pass
#     else:
#         pass

for __i__ in file.readlines():
    if __i__.__contains__('2.0000     ') or __i__.__contains__('#---') or __i__.__contains__('Axis C -180 180 1') or __i__.__contains__('----') \
            or __i__.__contains__('Axis position C = 0.00'):
        found = True

    if found:
        elements = 2
        number = ''
        for __j__ in __i__:
            if __j__.isdigit() or __j__ == '.' or __j__ == '-' or __j__ == 'e' or __j__ == '+':
                number += __j__
            else:
                if number.__contains__('.'):
                    try:
                        if elements == 2:
                            freq.append(float(number))
                        elif elements == -1:
                            s11.append(float(number))
                        else:
                            pass
                        elements -= 1
                        number = ''
                    except:
                        pass
                else:
                    number = ''
file.close()
print(freq)
print(s11)
freq = [__i__ * np.pi / 180 + np.pi/2 for __i__ in freq]
t = [__i__ for __i__ in range(0, 181)]
l = [__i__ for __i__ in range(-179, 1, 1)]
freq = []
for __i__ in range(len(t) + len(l)):
    if __i__ < 181:
        freq.append(t[__i__] * np.pi / 180 + np.pi/2)
    else:
        freq.append(l[__i__ - 181] * np.pi / 180 + np.pi/2)
print(freq)
meas = np.load('measurement_pattern_crosspol.npy')
fig, ax = plt.subplots(1, 2, subplot_kw={'projection': 'polar'})
ax[0].set_title('2.300 GHz')
freq.pop(-1)
ax[0].plot(freq, s11, color='orange')
ax[0].plot(meas[0], meas[1])
ax[1].plot(meas[0], meas[1])
plt.show()
########################################################################################################################
# Return loss plots
simulated_rl = np.load('simulated_return_loss.npy')
measured_rl = np.load('measurement_return_loss.npy')

plt.figure(0)
plt.plot(measured_rl[0], measured_rl[1], color='orange', label='Measurement (lab)')
plt.scatter(x=2.400, y=-9.130, marker='o', color='orange', label='[2.400, -9.130]')
plt.legend(markerscale=2.0)
plt.grid()
plt.xlabel('Frequency (GHz)')
plt.ylabel('Return loss (dB)')

plt.figure(1)
plt.plot(measured_rl[0], measured_rl[2], color='red', label='Measurement (compact range 1)')
plt.scatter(x=2.192, y=-12.570, marker='o', color='red', label='[2.192, -12.570]')
plt.scatter(x=2.1337143, y=-10.000, marker='>', color='red', label='[2.134, -10.000]')
plt.scatter(x=2.254153837, y=-10.000, marker='<', color='red', label='[2.254, -10.000]')
plt.legend(markerscale=2.0)
plt.grid()
plt.xlabel('Frequency (GHz)')
plt.ylabel('Return loss (dB)')

plt.figure(2)
plt.plot(measured_rl[0], measured_rl[3], color='black', label='Measurement (compact range 2)')
plt.scatter(x=2.358, y=-13.300, marker='o', color='black', label='[2.358, -13.300]')
plt.scatter(x=2.323826088, y=-10.000, marker='>', color='black', label='[2.324, -10.000]')
plt.scatter(x=2.387806449, y=-10.000, marker='<', color='black', label='[2.388, -10.000]')
plt.legend(markerscale=2.0)
plt.grid()
plt.xlabel('Frequency (GHz)')
plt.ylabel('Return loss (dB)')

plt.figure(3)
plt.plot(simulated_rl[0], simulated_rl[1], color='b', label='Simulation')
plt.plot(measured_rl[0], measured_rl[1], color='orange', label='Measurement (lab)')
plt.plot(measured_rl[0], measured_rl[2], color='red', label='Measurement (compact range 1)')
plt.plot(measured_rl[0], measured_rl[3], color='black', label='Measurement (compact range 2)')
plt.scatter(x=2.398, y=-27.758, marker='o', color='b', label='[2.398, -27.758]')
plt.scatter(x=2.3551019669, y=-10.000, marker='>', color='b', label='[2.355, -10.000]')
plt.scatter(x=2.438785, y=-10.000, marker='<', color='b', label='[2.439, -10.000]')
plt.scatter(x=2.400, y=-9.130, marker='o', color='orange', label='[2.400, -9.130]')
plt.scatter(x=2.192, y=-12.570, marker='o', color='red', label='[2.192, -12.570]')
plt.scatter(x=2.358, y=-13.300, marker='o', color='black', label='[2.358, -13.300]')
plt.grid()
plt.legend(loc='lower right', markerscale=2.0)
plt.xlabel('Frequency (GHz)')
plt.ylabel('Return loss (dB)')
measured_rl = measured_rl.tolist()

########################################################################################################################
# Gain plots
measured_gain = np.load('measured_gain.npy')
simulated_gain = np.load('simulated_gain.npy')

plt.figure(4)
plt.plot(measured_gain[0], measured_gain[1], color='orange', label='Measurement @ 0 degrees (V-V)')
plt.scatter(x=2.016, y=-2.17, marker='o', color='orange', label='[2.016, -2.170]')
plt.grid()
plt.title('Gain @ 0 degrees (vertical to vertical polarization)')
plt.xlabel('Frequency (GHz)')
plt.ylabel('Gain (dBi)')
plt.legend()

plt.figure(5)
plt.plot(measured_gain[0], measured_gain[2], color='red', label='Measurement @ 0 degrees (H-H)')
plt.scatter(x=2.398, y=-1.68, marker='o', color='red', label='[2.398, -1.680]')
plt.title('Gain @ 0 degrees (horizontal to horizontal polarization)')
plt.grid()
plt.xlabel('Frequency (GHz)')
plt.ylabel('Gain (dBi)')
plt.legend()

plt.figure(6)
plt.plot(measured_gain[0], measured_gain[3], color='black', label='Measurement changed feed cable (V-V)')
plt.scatter(x=2.388, y=-3.43, marker='o', color='black', label='[2.388, -3.430]')
plt.title('Gain with feed cable changed (vertical to vertical polarization)')
plt.grid()
plt.xlabel('Frequency (GHz)')
plt.ylabel('Gain (dBi)')
plt.legend()

plt.figure(7)
plt.plot(measured_gain[0], measured_gain[4], color='green', label='Measurement changed feed cable (H-H)')
plt.scatter(x=2.4, y=-3.09, marker='o', color='green', label='[2.400, -3.090]')
plt.title('Gain with feed cable changed (horizontal to horizontal polarization)')
plt.grid()
plt.xlabel('Frequency (GHz)')
plt.ylabel('Gain (dBi)')
plt.legend()

plt.figure(8)
plt.plot(measured_gain[0], measured_gain[5], color='purple', label='Measurement changed feed cable @ 75 degrees elevation (H-H)')
plt.scatter(x=2.386, y=-1.880, marker='o', color='purple', label='[2.386, -1.880]')
plt.title('Gain with feed cable changed @ 75 degrees (horizontal to horizontal polarization)')
plt.grid()
plt.xlabel('Frequency (GHz)')
plt.ylabel('Gain (dBi)')
plt.legend()

plt.figure(9)
max1 = [0.0, -20]
max2 = [0.0, -20]
max3 = [0.0, -20]
max4 = [0.0, -20]
max5 = [0.0, -20]
max6 = [0.0, -20]
min1 = [0.0, 0.0]
min2 = [0.0, 0.0]
min3 = [0.0, 0.0]
min4 = [0.0, 0.0]
min5 = [0.0, 0.0]
avg1 = []
avg2 = []
avg3 = []
avg4 = []
avg5 = []
for __i__ in range(len(measured_gain[0])):
    if 2.324 <= measured_gain[0][__i__] <= 2.388:
        avg1.append(measured_gain[1][__i__])
        avg2.append(measured_gain[2][__i__])
        avg3.append(measured_gain[3][__i__])
        avg4.append(measured_gain[4][__i__])
        avg5.append(measured_gain[5][__i__])
        if max1[1] < measured_gain[1][__i__]:
            max1[0] = measured_gain[0][__i__]
            max1[1] = measured_gain[1][__i__]
        if max2[1] < measured_gain[2][__i__]:
            max2[0] = measured_gain[0][__i__]
            max2[1] = measured_gain[2][__i__]
        if max3[1] < measured_gain[3][__i__]:
            max3[0] = measured_gain[0][__i__]
            max3[1] = measured_gain[3][__i__]
        if max4[1] < measured_gain[4][__i__]:
            max4[0] = measured_gain[0][__i__]
            max4[1] = measured_gain[4][__i__]
        if max5[1] < measured_gain[5][__i__]:
            max5[0] = measured_gain[0][__i__]
            max5[1] = measured_gain[5][__i__]

        if min1[1] > measured_gain[1][__i__]:
            min1[0] = measured_gain[0][__i__]
            min1[1] = measured_gain[1][__i__]
        if min2[1] > measured_gain[1][__i__]:
            min2[0] = measured_gain[0][__i__]
            min2[1] = measured_gain[1][__i__]
        if min3[1] > measured_gain[1][__i__]:
            min3[0] = measured_gain[0][__i__]
            min3[1] = measured_gain[1][__i__]
        if min4[1] > measured_gain[1][__i__]:
            min4[0] = measured_gain[0][__i__]
            min4[1] = measured_gain[1][__i__]
        if min5[1] > measured_gain[1][__i__]:
            min5[0] = measured_gain[0][__i__]
            min5[1] = measured_gain[1][__i__]
max6 = [0.0, -20]
min6 = [0.0, 20.0]
avg6 = []
for __i__ in range(len(simulated_gain[0])):
    if 2.324 <= simulated_gain[0][__i__] <= 2.388:
        avg6.append(simulated_gain[1][__i__])
        if max6[1] < simulated_gain[1][__i__]:
            max6[0] = simulated_gain[0][__i__]
            max6[1] = simulated_gain[1][__i__]
        if min6[1] > simulated_gain[1][__i__]:
            min6[0] = simulated_gain[0][__i__]
            min6[1] = simulated_gain[1][__i__]
plt.plot(simulated_gain[0], simulated_gain[1], color='b', label='Simulation (max. solid angle)')
plt.plot(measured_gain[0], measured_gain[1], color='orange')
plt.plot(measured_gain[0], measured_gain[2], color='red')
plt.plot(measured_gain[0], measured_gain[3], color='black')
plt.plot(measured_gain[0], measured_gain[4], color='green')
plt.plot(measured_gain[0], measured_gain[5], color='purple')
plt.scatter(x=2.388, y=2.1802706006819, marker='o', color='b', label='[2.388, 2.180]')
plt.scatter(x=2.372, y=-5.34, marker='o', color='orange', label='[2.372, -5.34]')
plt.scatter(x=2.388, y=-1.74, marker='o', color='red', label='[2.388, -1.740]')
plt.scatter(x=2.388, y=-3.43, marker='o', color='black', label='[2.388, -3.430]')
plt.scatter(x=2.388, y=-3.14, marker='o', color='green', label='[2.388, -3.140]')
plt.scatter(x=2.386, y=-1.88, marker='o', color='purple', label='[2.386, -1.880]')
print('min1: ', min1)
print('min2: ', min2)
print('min3: ', min3)
print('min4: ', min4)
print('min5: ', min5)
print('min6: ', min6)
print('max1: ', max1)
print('max2: ', max2)
print('max3: ', max3)
print('max4: ', max4)
print('max5: ', max5)
print('max6: ', max6)
print('Avg1: ', sum(avg1) / len(avg1))
print('Avg2: ', sum(avg2) / len(avg2))
print('Avg3: ', sum(avg3) / len(avg3))
print('Avg4: ', sum(avg4) / len(avg4))
print('Avg5: ', sum(avg5) / len(avg5))
print('Avg6: ', sum(avg6) / len(avg6))
plt.text(2.22, -12.5, '2.324 GHz')
plt.text(2.395, -12.5, '2.388 GHz')
plt.axvline(x=2.324, color='black', dashes=[0.5])
plt.axvline(x=2.388, color='black', dashes=[0.5])
plt.axvspan(2.324, 2.388, color='grey', alpha=0.1, lw=0)
plt.grid()
plt.xlabel('Frequency (GHz)')
plt.ylabel('Gain (dBi)')
plt.legend(loc='lower left')
measured_gain = measured_gain.tolist()
simulated_gain = simulated_gain.tolist()
print(max(simulated_gain[1]))
print(simulated_gain[0][simulated_gain[1].index(max(simulated_gain[1]))])

########################################################################################################################
# Cross-polarization plots (both measurement and simulation normalized)
meas_crosspol = np.load('measurement_pattern_crosspol.npy')
fig, ax = plt.subplots(1, 2, subplot_kw={'projection': 'polar'})
ax[0].set_title('2.300 GHz')
ax[0].plot(meas_crosspol[0], meas_crosspol[1], label='Measurement', color='orange')
ax[1].set_title('2.3400 GHz')
ax[1].plot(meas_crosspol[0], meas_crosspol[2], label='Measurement', color='orange')
plt.legend(bbox_to_anchor=(-0.1, 0.05), loc='upper center')
fig.suptitle('Cross-polarization')

fig1, ax1 = plt.subplots(1, 2, subplot_kw={'projection': 'polar'})
ax1[0].set_title('2.380 GHz')
ax1[0].plot(meas_crosspol[0], meas_crosspol[3], label='Measurement', color='orange')
ax1[1].set_title('2.400 GHz')
ax1[1].plot(meas_crosspol[0], meas_crosspol[4], label='Measurement', color='orange')
plt.legend(bbox_to_anchor=(-0.1, 0.05), loc='upper center')
fig1.suptitle('Cross-polarization')

fig2, ax2 = plt.subplots(1, 2, subplot_kw={'projection': 'polar'})
ax2[0].set_title('2.440 GHz')
ax2[0].plot(meas_crosspol[0], meas_crosspol[5], label='Measurement', color='orange')
ax2[1].set_title('2.500 GHz')
ax2[1].plot(meas_crosspol[0], meas_crosspol[6], label='Measurement', color='orange')
plt.legend(bbox_to_anchor=(-0.1, 0.05), loc='upper center')
fig2.suptitle('Cross-polarization')

########################################################################################################################
# Co-polarization plots (both measurement and simulation normalized)
measurement_pattern = np.load('measurement_pattern_copol.npy')
simulated_copol = np.load('simulated_pattern_copol.npy')
fig, ax = plt.subplots(1, 2, subplot_kw={'projection': 'polar'})
angle = [__i__ * np.pi / 180 - np.pi / 2 for __i__ in angle]
ax[0].set_title('2.300 GHz')
ax[0].plot(measurement_pattern[0], measurement_pattern[1], label='Measurement', color='orange')
ax[0].plot(simulated_copol[0], simulated_copol[1], label='Simulation', color='b')
ax[1].set_title('2.3400 GHz')
ax[1].plot(measurement_pattern[0], measurement_pattern[2], label='Measurement', color='orange')
ax[1].plot(simulated_copol[0], simulated_copol[2], label='Simulation', color='b')
plt.legend(bbox_to_anchor=(-0.1, 0.05), loc='upper center')
fig.suptitle('Co-polarization')

fig1, ax1 = plt.subplots(1, 2, subplot_kw={'projection': 'polar'})
ax1[0].set_title('2.380 GHz')
ax1[0].plot(measurement_pattern[0], measurement_pattern[3], label='Measurement', color='orange')
ax1[0].plot(simulated_copol[0], simulated_copol[3], label='Simulation', color='b')
ax1[1].set_title('2.400 GHz')
ax1[1].plot(measurement_pattern[0], measurement_pattern[4], label='Measurement', color='orange')
ax1[1].plot(simulated_copol[0], simulated_copol[4], label='Simulation', color='b')
plt.legend(bbox_to_anchor=(-0.1, 0.05), loc='upper center')
fig1.suptitle('Co-polarization')

fig2, ax2 = plt.subplots(1, 2, subplot_kw={'projection': 'polar'})
ax2[0].set_title('2.440 GHz')
ax2[0].plot(measurement_pattern[0], measurement_pattern[5], label='Measurement', color='orange')
ax2[0].plot(simulated_copol[0], simulated_copol[5], label='Simulation', color='b')
ax2[1].set_title('2.500 GHz')
ax2[1].plot(measurement_pattern[0], measurement_pattern[6], label='Measurement', color='orange')
ax2[1].plot(simulated_copol[0], simulated_copol[6], label='Simulation', color='b')
plt.legend(bbox_to_anchor=(-0.1, 0.05), loc='upper center')
fig2.suptitle('Co-polarization')
plt.show()
########################################################################################################################
