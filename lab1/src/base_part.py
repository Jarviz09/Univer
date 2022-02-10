import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt

def correct_index(x, x_nodes):
    n = len(x_nodes)
    if x > x_nodes[n - 1]:
        return n - 2
    if x < x_nodes[0]:
        return 0

    for i in range(0, n - 1):
        if x >= x_nodes[i] and x <= x_nodes[i + 1]:
            return i


def qubic_spline_coeff(x_nodes, y_nodes):
    a = y_nodes
    h = [x_nodes[i + 1] - x_nodes[i] for i in range(0, 10)]
    res = [0 for i in range(0,11)]
    for i in range(1,10):
        res[i] = 3*(a[i+1]-a[i])/h[i] - 3*(a[i]-a[i-1])/h[i-1]
    matrix = np.zeros((11, 11))
    for i in range(0,11):
        for j in range(0,11):
            if (i == j):
                if (i > 0) and (i<10):
                    matrix[i, j] = (h[i]+h[i-1])*2
                else:
                    matrix[i, j] = 1
            if (j == i - 1) and (i < 10):
                matrix[i, j] = h[j]
            if (j == i + 1) and (i > 0):
                matrix[i, j] = h[i]
    # print(res)
    matrix = LA.inv(matrix)
    c = matrix @ res
    b = [(a[i+1]-a[i])/h[i] - h[i]*(c[i+1]+2*c[i])/3 for i in range(0,10)]
    d = [(c[i+1]-c[i])/(3*h[i]) for i in range(0,10)]
    c = np.delete(c,(10), axis = 0)
    qs_coeff = np.c_[b, c, d]
    return(qs_coeff)

def qubic_spline(x, x_nodes, y_nodes, qs_coeff):
    node = x_nodes[correct_index(x, x_nodes)]
    i = correct_index(x, x_nodes)
    S = y_nodes[i] + qs_coeff[i][0]*(x-x_nodes[i]) + qs_coeff[i][1]*((x-x_nodes[i])**2) + qs_coeff[i][2]*((x-x_nodes[i])**3)
    return S

def d_qubic_spline(x, x_nodes, qs_coeff):
    node = x_nodes[correct_index(x, x_nodes)]
    i = correct_index(x, x_nodes)
    _S = qs_coeff[i][0] + 2*qs_coeff[i][1]*(x-x_nodes[i]) + 3*qs_coeff[i][2]*((x-x_nodes[i])**2)
    return(_S)

def graphic_qubic_spline(x_nodes, y_nodes, qs_coeff):
    _x = np.linspace(0, 1, 1000)
    F = [qubic_spline(_x[i],x_nodes, y_nodes, qs_coeff) for i in range(0, 1000)]
    plt.plot(_x, F)
    plt.plot(x_nodes,y_nodes, 'o', color='blue')
    plt.show()


if __name__ == '__main__':
    x = 0.44
    x_nodes = [i/10 for i in range(0, 11)]
    y_nodes = [3.37, 3.95, 3.73, 3.59, 3.15, 3.15, 3.05, 3.86, 3.60, 3.70, 3.02]
    qs_coeff = qubic_spline_coeff(x_nodes, y_nodes)
    qubic_spline(x, x_nodes, y_nodes, qs_coeff)
    d_qubic_spline(x, x_nodes, qs_coeff)
    graphic_qubic_spline(x_nodes, y_nodes, qs_coeff)

