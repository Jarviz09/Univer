import numpy as np
import matplotlib.pyplot as plt


def plot_adj_matrix(L3_vectors, M):
    plt.matshow(M)

    i = np.argsort(L3_vectors[:, 1].T)
    M1 = M[np.ix_(i, i)]
    plt.matshow(M1)

    plt.grid()
    plt.show()


def plot_laplacian(L_i):
    L_numbers, L_vectors = np.linalg.eig(L_i)

    L_vectors = L_vectors[:, np.argsort(L_numbers)]
    L_vectors = np.flip(L_vectors)
    L_numbers = L_numbers[np.argsort(L_numbers)]
    L_numbers = np.flip(L_numbers)

    fig, ax = plt.subplots()
    ax.plot(1. + np.arange(len(L_numbers)), L_numbers, 'o--')

    ax.grid()
    plt.show()

    return L_vectors


def laplacian_G1():
    adj_matrix = np.ones((10, 10))

    for i in range(0, 10):
        adj_matrix[i][i] = 0

    D = np.zeros((10, 10))
    for i in range(0, 10):
        D[i][i] = 9

    L = D - adj_matrix


    return L


def laplacian_G2():
    adj_list = [[2, 5, 6], [1, 3, 4, 5], [2, 5, 6], [2, 5, 7, 8, 18], [1, 2, 3, 4, 7, 8], [1, 3, 7, 9],
                [4, 5, 6, 8, 13], [4, 5, 7, 16], [6, 11, 13], [11, 12, 13], [9, 10, 12, 13], [10, 11, 13, 15],
                [7, 9, 10, 11, 12], [16, 18, 20], [12, 16, 18, 20], [8, 14, 15, 17, 18], [16, 18, 20],
                [4, 14, 15, 16, 17, 19, 20], [18, 20], [14, 15, 17, 18, 19]]

    adj_matrix = np.zeros((20, 20))

    for item in range(0, len(adj_list)):
        for i in adj_list[item]:
            adj_matrix[item][i - 1] = 1

    D = np.zeros((20, 20))

    for i in range(0, len(adj_list)):
        D[i][i] = len(adj_list[i])

    L = D - adj_matrix

    return L


def laplacian_G3():
    data = []
    with open("adjacency_matrix.txt") as file:
        for line in file:
            data.append([int(x) for x in line.split(' ')])

    adj_matrix = np.array(data)

    powers = []

    for row in adj_matrix:
        powers.append(sum(row, 0))

    D = np.zeros((1000, 1000))

    for i in range(0, len(powers)):
        D[i][i] = powers[i]

    return D - adj_matrix, adj_matrix
