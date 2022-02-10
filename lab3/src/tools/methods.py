import numpy as np
from scipy import optimize


def benchmark(func):
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__}: Время выполнения: {end - start} секунд.')

        return res

    return wrapper


def normal(consts, values):
    v, u = values
    if v >= 30:
        v = consts['c']
        u = u + consts['d']

    return [v, u]


@benchmark
def euler(x_0, t_n, f, h, consts):
    # x_0 - initial conditions  v(0) = c, u(0) = bv(0)
    # f - function of the ODE system
    # consts - a,b,c,d,I for a specific mode
    t_0 = 0
    t_nums = np.arange(t_0, t_n + h, h)  # generation of t according to the condition of the Euler method
    y = np.zeros(shape=(len(t_nums), len(x_0)))
    y[0] = x_0

    for i in range(len(t_nums) - 1):
        w = y[i]
        w = w + h * f(w, consts)
        y[i + 1] = normal(consts, w)

    return t_nums, y


@benchmark
def implicit_euler(x_0, t_n, f, h, consts):
    # x_0 - initial conditions  v(0) = c, u(0) = bv(0)
    # f - function of the ODE system
    # consts - a,b,c,d,I for a specific mode
    t_0 = 0
    t_nums = np.arange(t_0, t_n + h, h)
    y = np.zeros(shape=(len(t_nums), len(x_0)))
    y[0] = x_0

    for i in range(len(t_nums) - 1):
        w = y[i]
        fun = lambda foo: w - foo + h * f(foo, consts)
        sol = optimize.root(fun, w)
        w = sol.x
        y[i + 1] = normal(consts, w)

    return t_nums, y


@benchmark
def runge_kutta(x_0, t_n, f, h, consts):
    # x_0 - initial conditions  v(0) = c, u(0) = bv(0)
    # f - function of the ODE system
    # consts - a,b,c,d,I for a specific mode
    t_0 = 0
    t_nums = np.arange(t_0, t_n + h, h)
    y = np.zeros(shape=(len(t_nums), len(x_0)))
    y[0] = x_0

    for i in range(len(t_nums) - 1):
        w = y[i]
        k_1 = h * f(w, consts)
        k_2 = h * f(w + k_1 / 2, consts)
        k_3 = h * f(w + k_2 / 2, consts)
        k_4 = h * f(w + k_3, consts)

        w = w + (k_1 + 2 * k_2 + 2 * k_3 + k_4) / 6

        y[i + 1] = normal(consts, w)

    return t_nums, y
