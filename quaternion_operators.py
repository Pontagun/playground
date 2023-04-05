import numpy as np
import math


def myQuatSlerp(q, t, h):  # cutety
    omega = math.acos(np.dot(q, t))
    acc_q = q * np.sin((1 - h) * omega)
    mag_q = t * np.sin(h * omega)

    q_intpl = (acc_q + mag_q) / np.sin(omega)

    return q_intpl


def myQuatProd(q, w):
    q = np.array(q)
    ww = np.array([[w[3], w[2], -w[1], w[0]],
                   [-w[2], w[3], w[0], w[1]],
                   [w[1], -w[0], w[3], w[2]],
                   [-w[0], -w[1], -w[2], w[3]]])
    r = np.matmul(ww, q)

    return r


def myQuatConj(q):
    return [-q[0], -q[1], -q[2], q[3]]


def myQuatIntegrate(dq, q0, dt):
    w = 2 * myQuatProd(dq, myQuatConj(q0));
    exp = myQuatExponential((w * dt) / 2);
    q1 = myQuatProd(exp, q0);
    q1_norm = myQuatNormalize(q1)

    return q1_norm


def myQuatExponential(q):
    qvnorm2 = math.sqrt(pow(q[0], 2) + pow(q[1], 2) + pow(q[2], 2))

    if qvnorm2 != 0:
        exp_q = math.exp(q[3]) * np.append((math.sin(qvnorm2) / qvnorm2) * q[0:3], math.cos(qvnorm2))
    else:
        exp_q = math.exp(q[3]) * np.append(q[0:3], math.cos(qvnorm2))

    return exp_q


def myQuatNormalize(q):
    normalized_q = q / math.sqrt(pow(q[0], 2) + pow(q[1], 2) + pow(q[2], 2) + pow(q[3], 2))
    return normalized_q


def myHamilton(m, c):
    # m: reading value from a sensor
    # c calulated value from q_g
    magnitude = lambda vec: math.sqrt(sum(pow(element, 2) for element in vec))

    qv = np.cross(m, c)
    qw = math.sqrt(magnitude(m) * magnitude(c)) + np.dot(m, c)
    deltaQ = myQuatNormalize(np.append(qv, qw))
    return deltaQ
