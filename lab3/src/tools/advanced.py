import numpy as np
from matplotlib import pyplot as plt


def get_consts(n, n_e, n_b):
    # n - number of neurons
    # n_e - number of excitatory neurons
    # n_b - number of braking neurons
    W = np.hstack((np.random.default_rng().random((n, n_e)) / 2, - np.random.default_rng().random((n, n_b))))
    a = np.hstack((0.02 * np.ones(n_e), 0.02 + 0.08 * np.random.default_rng().random(n_b)))
    b = np.hstack((0.2 * np.ones(n_e), 0.25 - 0.05 * np.random.default_rng().random(n_b)))
    c = np.hstack((-65 + 15 * np.random.default_rng().random(n_e) ** 2, -65 * np.ones(n_b)))
    d = np.hstack((8 - 6 * np.random.default_rng().random(n_e) ** 2, 2 * np.ones(n_b)))

    return W, a, b, c, d


def neural_network():

    t_n = 1000
    n = 1000
    h = 0.5
    n_b = int(0.2 * n)
    n_e = int(0.8 * n)

    W, a, b, c, d = get_consts(n, n_e, n_b)

    v = -65.0 * np.ones(n)
    u = v * b

    ex_t_plot = []
    br_t_plot = []

    ex_neuron_id = []
    br_neuron_id = []

    steps_in_t = int(1 / h)

    I = np.hstack((5 * np.random.default_rng().random(n_e), 2 * np.random.default_rng().random(n_b)))

    for t in range(t_n):
        impulse = v >= 30

        for i, is_impulse in enumerate(impulse):
            if is_impulse:
                if i > 799:
                    br_t_plot.append(t)
                    br_neuron_id.append(i)
                else:
                    ex_t_plot.append(t)
                    ex_neuron_id.append(i)

        v[impulse] = c[impulse]
        u[impulse] = u[impulse] + d[impulse]

        I_new = I.copy()
        I_new += np.sum(W[:, impulse], axis=1)

        for i in range(steps_in_t):
            new_v = v + h * (0.04 * v ** 2 + 5 * v + 140 - u + I_new)
            new_u = u + h * a * (b * v - u)
            v = new_v
            u = new_u

    fig, ax_1 = plt.subplots(1, 1, figsize=(14, 6))
    ax_1.scatter(x=br_t_plot, y=br_neuron_id, color="orangered", s=5)
    ax_1.scatter(x=ex_t_plot, y=ex_neuron_id, color="deepskyblue", s=5)
    ax_1.set_xlabel('time', fontsize=16)
    ax_1.set_ylabel('neuron id', fontsize=16)
    ax_1.grid()
    plt.show()

    t = br_t_plot + ex_t_plot
    fig_2, ax_2 = plt.subplots(1, 1, figsize=(14, 6))
    ax_2.hist(x=t, bins=t[len(t) - 1], linewidth=2, color="olive")
    ax_2.set_xlabel('time', fontsize=16)
    ax_2.set_ylabel('number of spikes in 1 ms', fontsize=16)
    ax_2.grid()
    plt.show()
