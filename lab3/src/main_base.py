import json
import numpy as np
import matplotlib.pyplot as plt
from tools.methods import euler, implicit_euler, runge_kutta


BASE_CONST = json.load(open('configs/config_base.json', 'r'))


def f(nums, consts):
    # consts - a,b,c,d,I for a specific mode
    # nums - v,u values
    v, u = nums
    I = consts['I']
    current_v = 0.04 * v ** 2 + 5 * v + 140 - u + I
    current_u = consts['a'] * (consts['b'] * v - u)

    return np.asarray([current_v, current_u])


if __name__ == '__main__':

    h = 0.1
    t_n = 300

    t = np.linspace(0, t_n, 201)
    fig, ax = plt.subplots(2, 2, figsize=(14, 6))
    axes = [ax[0][0], ax[0][1], ax[1][0], ax[1][1]]

    for name, current_ax in zip(BASE_CONST, axes):
        x_0 = [BASE_CONST[name]['c'], BASE_CONST[name]['c'] * BASE_CONST[name]['b']]
        x_1, y_1 = euler(x_0, t_n, f, h, BASE_CONST[name])
        x_2, y_2 = implicit_euler(x_0, t_n, f, h, BASE_CONST[name])
        x_3, y_3 = runge_kutta(x_0, t_n, f, h, BASE_CONST[name])

        current_ax.set_title(name, loc='left')
        current_ax.set_ylim([-80, 40])
        current_ax.set_xlabel(r'$t$', fontsize=16)
        current_ax.set_ylabel(r'$v$', fontsize=16)
        current_ax.plot(x_1, y_1[:,0], ':', label=r"Метод Эйлера", marker='o', markersize=2)
        current_ax.plot(x_2, y_2[:,0], ':', label=r"Неявный метод Эйлера", marker='o', markersize=2)
        current_ax.plot(x_3, y_3[:,0], ':', label=r"Метод Рунге-Кута", marker='o', markersize=2)

        current_ax.grid()
        current_ax.legend(loc=1)

    plt.show()
