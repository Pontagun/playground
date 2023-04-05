import csv
import math
import data_helper
import numpy as np
import matplotlib.pyplot as plt
import quaternion_operators as quat

data = []
row = []
with open('rec011.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for line in reader:
        row = [float(i) for i in line]
        data.append(row)

data = data_helper.create_json(data, "r")

gyro_thrs_x = 0.0271
gyro_thrs_y = 0.0232
gyro_thrs_z = 0.0305
b_scaling = 1

data_n = len(data)
sampling_rate = data_n / float(data[data_n - 1]["t"])

gyro_avg = np.zeros((data_n, 3))
magn_avg = np.zeros((data_n, 3))
accl_avg = np.zeros((data_n, 3))
bias = np.zeros((data_n, 3))
bias_buff = np.zeros((data_n, 3))
unbiased_xyz = np.zeros((data_n, 3))
stage_m = np.zeros(data_n)

accl_inert = np.zeros((data_n, 3))
magn_inert = np.zeros((data_n, 3))

qg = np.zeros((data_n, 4))  # purely read from gyro.
qg[0] = [0, 0, 0, 1]
dq_g = np.zeros((data_n, 4))

qg_a = np.zeros((data_n, 4))
qg_a[0] = [0, 0, 0, 1]
dq_ga = np.zeros((data_n, 4))

qg_m = np.zeros((data_n, 4))
qg_m[0] = [0, 0, 0, 1]
dq_gm = np.zeros((data_n, 4))

q_sa = np.zeros((data_n, 4))
q_sm = np.zeros((data_n, 4))
q_out1 = np.zeros((data_n, 4))

data[0]["accel"].append(0)
a_init = data[0]["accel"]

data[0]["magne"].append(0)
m_init = data[0]["magne"]

e = np.zeros((data_n, 3))  # Error between computed and measured gravity vector
e_magnitude = np.zeros((data_n, 1))
trigcount_x = trigcount_y = trigcount_z = 0

mean = lambda a, b, c: (float(a) + float(b) + float(c)) / 3
magnitude = lambda vec: math.sqrt(sum(pow(element, 2) for element in vec))

for i, row in enumerate(data):
    if i < data_n - 2:
        gyro_avg[i][0] = mean(data[i]["gyro"][0], data[i + 1]["gyro"][0], data[i + 2]["gyro"][0])
        gyro_avg[i][1] = mean(data[i]["gyro"][1], data[i + 1]["gyro"][1], data[i + 2]["gyro"][1])
        gyro_avg[i][2] = mean(data[i]["gyro"][2], data[i + 1]["gyro"][2], data[i + 2]["gyro"][2])

        accl_avg[i][0] = mean(data[i]["accel"][0], data[i + 1]["accel"][0], data[i + 2]["accel"][0])
        accl_avg[i][1] = mean(data[i]["accel"][1], data[i + 1]["accel"][1], data[i + 2]["accel"][1])
        accl_avg[i][2] = mean(data[i]["accel"][2], data[i + 1]["accel"][2], data[i + 2]["accel"][2])

        magn_avg[i][0] = mean(data[i]["magne"][0], data[i + 1]["magne"][0], data[i + 2]["magne"][0])
        magn_avg[i][1] = mean(data[i]["magne"][1], data[i + 1]["magne"][1], data[i + 2]["magne"][1])
        magn_avg[i][2] = mean(data[i]["magne"][2], data[i + 1]["magne"][2], data[i + 2]["magne"][2])

        if i > 0:
            bias[i] = bias[i - 1]

        if abs(gyro_avg[i, 0]) < gyro_thrs_x:
            trigcount_x += 1
            bias_buff[i, 0] = bias[i, 0] + data[i]["gyro"][0]
        else:
            trigcount_x = bias_buff[i, 0] = 0

        if abs(gyro_avg[i, 1]) < gyro_thrs_y:
            trigcount_y += 1
            bias_buff[i, 1] = bias[i, 1] + data[i]["gyro"][1]
        else:
            trigcount_y = bias_buff[i, 0] = 0

        if abs(gyro_avg[i, 2]) < gyro_thrs_z:
            trigcount_z += 1
            bias_buff[i, 2] = bias[i, 2] + data[i]["gyro"][2]
        else:
            trigcount_z = bias_buff[i, 0] = 0

        if trigcount_x == 5:
            bias[i, 0] = bias_buff[i, 0] / 5
            trigcount_x = bias_buff[i, 0] = 0

        if trigcount_y == 5:
            bias[i, 1] = bias_buff[i, 1] / 5
            trigcount_y = bias_buff[i, 1] = 0

        if trigcount_z == 5:
            bias[i, 2] = bias_buff[i, 2] / 5
            trigcount_z = bias_buff[i, 2] = 0

        unbiased_xyz[i] = data[i]["gyro"] - (b_scaling * bias[i])

        if i > 0:
            w = np.append(unbiased_xyz[i], 0)
            sampling_interval = data[i]["t"] - data[i - 1]["t"]

            dq_g[i] = 0.5 * quat.myQuatProd(qg[i - 1], w)
            qg[i] = quat.myQuatIntegrate(dq_g[i], qg[i - 1], sampling_interval)

            dq_ga[i] = 0.5 * quat.myQuatProd(qg_a[i - 1], w)
            qg_a[i] = quat.myQuatIntegrate(dq_ga[i], qg_a[i - 1], sampling_interval)

            dq_gm[i] = 0.5 * quat.myQuatProd(qg_m[i - 1], w)
            qg_m[i] = quat.myQuatIntegrate(dq_gm[i], qg_m[i - 1], sampling_interval)

        a4 = quat.myQuatProd(quat.myQuatConj(qg_a[i]), quat.myQuatProd(a_init, qg_a[i]))
        m4 = quat.myQuatProd(quat.myQuatConj(qg_m[i]), quat.myQuatProd(m_init, qg_m[i]))
        a3 = a4[0:3]
        m3 = m4[0:3]

        e = accl_avg[i] - a3        #No usage in the algorithm
        e_magnitude = magnitude(e)  #No usage in the algorithm

        deltaQa = quat.myHamilton(accl_avg[i], a3)
        deltaQm = quat.myHamilton(magn_avg[i], m3)

        qg_m[i] = quat.myQuatNormalize(quat.myQuatProd(qg_m[i], deltaQm))
        qg_a[i] = quat.myQuatNormalize(quat.myQuatProd(qg_a[i], deltaQa))

        q_sm[i] = quat.myQuatSlerp(qg[i], qg_m[i], data[i]["mu"])
        q_sa[i] = quat.myQuatSlerp(qg[i], qg_a[i], data[i]["alpha"])

        q_out1[i] = quat.myQuatSlerp(q_sm[i], q_sa[i], data[i]["alpha"])

        qg[i] = qg_m[i] = qg_a[i] = q_out1[i]

plt.plot(qg); plt.show()
