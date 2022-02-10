import math

import numpy as np
from matplotlib import pyplot as plt

from qubic_library import qubic_spline_coeff, graphic_qubic_spline, qubic_spline, d_qubic_spline


def func(t):
    C = 1.03439984
    g = 10
    # return np.sqrt(1/g) * np.sqrt( 1 + ( np.sin(2*t)**2 )/( 1 - np.cos(2*t) )**2 ) /\
    #     np.sqrt( C * (1 - np.cos(2*t)) ) * C * (1 - np.cos(2*t))
    return np.sqrt(C/g) * np.sqrt((1 - np.cos(2*t))**2 + np.sin(2*t)**2) / np.sqrt(1 - np.cos(2*t))
    # return 1 / np.sqrt(2 * g) * np.sqrt((2 + 2 *\
# (np.sin(2 * t) / (1 - np.cos(2 * t))) ** 2) / (C * (1 - np.cos(2 * t)))) * C * (1 - np.cos(2 * t))

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def find_exact(C, T):
    g = 10
    a = 1e-7
    return((T - a)*np.sqrt(2*C/g))


def graphic_absolute_error(a, b, func):
    n = [i for i in range(3, 10000, 100)]
    simpson = 0
    trapezoid = 0
    for i in n:
        h = (b - a) / (i - 1)
        simpson = composite_simpson(a, b, i, func)
        trapezoid = composite_trapezoid(a, b, i, func)
        plt.scatter(h, find_absolute_error(simpson), color="green", s = 18, label="Simpson error")
        plt.scatter(h, find_absolute_error(trapezoid), color="deeppink", s = 18, label="Trapezoid error")

    plt.legend(['Simpson error', 'Trapezoid error'])
    plt.grid(True)
    plt.loglog()
    plt.show()


def find_absolute_error(calc):
    exact = find_exact(C, T)
    return abs(exact - calc)


def composite_simpson(a, b, n, func):
    if (n % 2 == 1):
        n += 1
    h = (b - a) / n
    t = [a + (i - 1)*h for i in range(1, n + 2)]

    chetniy = 0
    nechetniy = 0

    print(len(t))

    for i in range(1, n):
        if ((i + 1 ) % 2 == 0):
            chetniy += func(t[i])
            # print('Значение в точке ', i, ' равно ', func(t[i]))
        else:
            nechetniy += func(t[i])
            # print('Значение в точке ',i,' равно ',func(t[i]))

    integral_simpson = (func(t[0]) + func(t[n]) + 4 * chetniy + 2 * nechetniy) * (h/3)

    print(integral_simpson)

    return integral_simpson


def composite_trapezoid(a, b, n, func):
    h = (b - a) / n
    t = [a + (i - 1)*h for i in range(1, n + 2)]

    summa = 0
    print(len(t))

    for i in range(1, n):
        summa += func(t[i])

    integral_trapezoid = (func(t[0]) + func(t[n]) + 2 * summa) * (h/2)

    print(integral_trapezoid)

    return integral_trapezoid


if __name__ == '__main__':
    C = 1.03439984
    T = 1.75418438
    t = np.linspace(0, T, 100)
    # x = []
    graphic_absolute_error(1e-7, T, func)
    # plt.plot(t, func(t), color="red")
    # plt.show()

    # for i in t:
    #     x.append(C*(t - 0.5*np.sin(2*i)))
    #
    # y = [C*(0.5 - 0.5*np.cos(2*i)) for i in t]
    # print(x)
    # print(y)
    # x_nodes = np.linspace(0, 2, 150)
    # y_nodes = np.interp(x_nodes, x, y, left=None, right=None)
    # plt.plot(x_nodes, y_nodes)
    # plt.show()
    # print(find_exact(C,T))
