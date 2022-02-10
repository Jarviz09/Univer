import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sps
import random

from base_part import qubic_spline, qubic_spline_coeff

def l_i(i, x, x_nodes):
    l = 1
    for j in range(0,11):
        if (i != j):
            l = l * (x - x_nodes[j]) / (x_nodes[i] - x_nodes[j])

    #print(l)
    return l

def L(x, x_nodes, y_nodes):
    L = 0.0
    for i in range(0,11):
        L = L + y_nodes[i] * l_i(i, x, x_nodes)

    #print(L)
    return L

def gen_vector(x_nodes):
    X_vector = []
    # Z = sps.norm(loc = 0, scale = 0.01).rvs(11)
    for i in range(0, len(x_nodes)):
        Z = np.random.normal(loc = 0.0, scale=0.01)
        X_vector.append(x_nodes[i] + Z)
    # print(X_vector)
    return(X_vector)

def graph_thousand_vectors(x_nodes, y_nodes):
    for i in range(0, 1000):
        x_shift = np.linspace(0, 1, 1000)
        #print(x_shift)
        x_nodes_new = gen_vector(x_nodes)
        Function = [qubic_spline(x_shift[i], x_nodes_new, y_nodes, qubic_spline_coeff(x_nodes_new, y_nodes)) for i in range(0, 1000)]
        #print(x_shift, Function)
        plt.plot(x_shift, Function)
    plt.grid(True)
    plt.show()

"""def graph_thousand_vectors(x_nodes, y_nodes):
    for i in range(0, 1000):
        x_shift = np.linspace(0, 1, 1000)
        #print(x_shift)
        y_nodes_new = gen_vector(y_nodes)
        Function = [qubic_spline(x_shift[i], x_nodes, y_nodes_new, qubic_spline_coeff(x_nodes, y_nodes_new)) for i in range(0, 1000)]
        #print(x_shift, Function)
        plt.plot(x_shift, Function)
    plt.grid(True)
    plt.show()"""


"""def graph_qubic_spline(x_new):
    x_nodes = [i / 10 for i in range(0, 11)]
    y_new_nodes = gen_vector(y_nodes)
    _y = []
    for i in range(0, len(x_new)):
        F = qubic_spline(x_new[i], x_nodes, y_new_nodes, qubic_spline_coeff(x_nodes, y_new_nodes))
        _y.append(F)
    return _y"""

def graph_qubic_spline(x_new):
    x_nodes = [i / 10 for i in range(0, 11)]
    x_new_nodes = gen_vector(x_nodes)
    _y = []
    for i in range(0, len(x_new)):
        F = qubic_spline(x_new[i], x_new_nodes, y_nodes, qubic_spline_coeff(x_new_nodes, y_nodes))
        _y.append(F)
    return _y

def graph_h_functions_lagrange(x_nodes, y_nodes):
    h_l = []
    h_medium = []
    h_u = []
    matrix =[]
    x = np.linspace(0, 1, 1000)
    for i in range(0, 1000):
        y = []
        gen_nodes = gen_vector(y_nodes)
        for j in range(0, 1000):
            y.append(L(x[j], x_nodes, gen_nodes))
        matrix.append(y)
    # print(matrix)

    for i in range(0, 1000):
        list = []
        for j in range(0, 1000):
            list.append(matrix[j][i])
        list = sorted(list)
        h_l.append(list[49])
        h_medium.append(list[499])
        h_u.append(list[949])

    plt.plot(x, h_l)
    plt.plot(x, h_medium)
    plt.plot(x, h_u)
    plt.fill_between(x, h_u, h_l, color = 'yellow')
    plt.show()

"""def graph_h_functions_lagrange(x_nodes, y_nodes):
    h_l = []
    h_medium = []
    h_u = []
    matrix =[]
    x = np.linspace(0, 1, 1000)
    for i in range(0, 1000):
        y = []
        gen_nodes = gen_vector(x_nodes)
        for j in range(0, 1000):
            y.append(L(x[j], gen_nodes, y_nodes))
        matrix.append(y)
    # print(matrix)

    for i in range(0, 1000):
        list = []
        for j in range(0, 1000):
            list.append(matrix[j][i])
        list = sorted(list)
        h_l.append(list[49])
        h_medium.append(list[499])
        h_u.append(list[949])

    plt.plot(x, h_l)
    plt.plot(x, h_medium)
    plt.plot(x, h_u)
    plt.fill_between(x, h_u, h_l, color = 'yellow')
    plt.show()"""


def graph_h_functions_qubic(x_nodes, y_nodes):
    h_l = []
    h_medium = []
    h_u = []
    matrix =[]
    x = np.linspace(0, 1, 1000)
    for i in range(0, 1000):
        y = graph_qubic_spline(x)
        matrix.append(y)

    for i in range(0, 1000):
        list = []
        for j in range(0, 1000):
            list.append(matrix[j][i])
        list = sorted(list)
        h_l.append(list[49])
        h_medium.append(list[499])
        h_u.append(list[949])

    plt.plot(x, h_l)
    plt.plot(x, h_medium)
    plt.plot(x, h_u)
    plt.fill_between(x, h_u, h_l, color = 'yellow')
    plt.show()

if __name__ == '__main__':
    x_nodes = [i / 10 for i in range(0, 11)]
    y_nodes = [3.37, 3.95, 3.73, 3.59, 3.15, 3.15, 3.05, 3.86, 3.60, 3.70, 3.02]
    #l_i(3,2,x_nodes)
    #L(0.44, x_nodes, y_nodes)
    graph_thousand_vectors(x_nodes, y_nodes)
    # graph_h_functions_qubic(x_nodes, y_nodes)
    # graph_h_functions_lagrange(x_nodes, y_nodes)
    # graph_h_functions_qubic(x_nodes, y_nodes)
    #a = gen_vector(x_nodes)
    # print(a)