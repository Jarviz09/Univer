import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as st

from advanced import laplacian_G1, laplacian_G2, laplacian_G3, plot_laplacian, plot_adj_matrix


def plot_dev(standard_dev):
    fig, ax = plt.subplots()
    pc_numbers = [i for i in range(0, len(standard_dev))]
    ax.plot(pc_numbers, standard_dev, 'o--')
    ax.grid()
    plt.show()


def graph(A, pc, diagnosis):
    fig, ax = plt.subplots()
    x = [np.mean(A[:, 0]), np.mean(A[:, 1])]
    sigma = [st.stdev(A[:, 0]), st.stdev(A[:, 1])]
    _A = (A - x) / (sigma)
    ax.scatter(_A[:, 0], _A[:, 1], c=diagnosis, s=3)
    ax.plot([0], [0], 'go', markersize=10)
    max_val = np.max(np.abs(_A))
    for item in pc:
        ax.plot([0, max_val/1.5 * item[0]], [0, max_val/1.5 * item[1]], linewidth=3)
    ax.grid()
    plt.show()


def get_a():
    data = []
    with open("wdbc.data") as file:
        for line in file:
            data.append([x for x in line.split(',')])

    diagnosis = []
    for row in data:
        if row[1] == 'M':
            diagnosis.append("red")
        else:
            diagnosis.append("blue")

    for row in data:
        row.pop(1)
        row.pop(0)

    for row in data:
        for i in range(0, len(row)):
            row[i] = float(row[i])

    A = np.array(data)

    return A, diagnosis


def pca(A):
    self_numbers, self_vectors = np.linalg.eig(A.transpose() @ A)

    sort_num = np.argsort(self_numbers)
    i = np.flip(sort_num)
    self_numbers = self_numbers[i]
    self_vectors = self_vectors[:, i]

    nu = 1/(len(A) - 1)
    standard_dev = []
    for i in range(len(self_numbers)):
        standard_dev.append(np.sqrt(nu)*np.sqrt(self_numbers[i]))
    return self_vectors.T, standard_dev


def center(A):
    m = len(A)
    A_center = (np.eye(m) - 1./m * np.ones((m, m))) @ A
    return A_center


if __name__ == '__main__':
    data = []

    A, diagnosis = get_a()
    A_center = center(A)
    principal_comp, standard_dev = pca(A_center)
    # plot_dev(standard_dev)
    principal_comp_cut = principal_comp[:2]
    # print(principal_comp_cut)
    # graph(A_center @ principal_comp_cut.T, principal_comp_cut @ principal_comp_cut.T, diagnosis)

    L1 = laplacian_G1()
    # plot_laplacian(L1)
    L2 = laplacian_G2()
    # plot_laplacian(L2)
    L3, adj_matrix = laplacian_G3()
    L3 = np.array(L3)
    L3_numbers, L3_vectors = np.linalg.eig(L3)

    plot_adj_matrix(L3_vectors, adj_matrix)

    # plot_laplacian(L3)
