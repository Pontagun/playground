import numpy as np
import math

def myQuatSlerp(q, t, h): #cutety
    omega = np.arccos(np.dot(q, t))

    acc_q = q*np.sin((1-h)*omega)
    mag_q = t*np.sin(h*omega)

    q_intpl = (acc_q + mag_q) / np.sin(h)

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

    return q1


def myQuatExponential(q):
    qvnorm2 = math.sqrt(pow(q[0], 2) + pow(q[1], 2) + pow(q[2], 2))

    if qvnorm2 != 0:
        exp_q = math.exp(q[3]) * np.append((math.sin(qvnorm2) / qvnorm2) * q[0:3], math.cos(qvnorm2))
    else:
        exp_q = math.exp(q[3]) * np.append(q[0:3], math.cos(qvnorm2))

    return exp_q


def myQuatNormalize(q):
    normalized_q = q / math.sqrt(pow(q[0], 2) + pow(q[1], 2) + pow(q[2], 2) + pow(q[3],2))
    return normalized_q
