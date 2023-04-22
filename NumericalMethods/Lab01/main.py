import numpy as np


def cylinder_area(r: float, h: float) -> float:

    nan = np.NAN
    pi = np.pi

    if r <= 0 or h <= 0:
        return nan
    else:
        value = 2 * pi * ((r ** 2) + (r * h))
        return value


def fib(n: int):

    if n <= 0 or isinstance(n, float):
        return None
    elif n == 1:
        series = np.array([1])
        return series
    else:
        series = np.array([1, 1])
        for i in range(0, n):
            series = np.append(series, series[-1] + series[-2])
        return series


def matrix_calculations(a: float):
    m = np.array([[a, 1, -a], [0, 1, 1], [-a, a, 1]])
    m_inv = np.linalg.inv(m)
    m_t = np.transpose(m)
    m_det = np.linalg.det(m)

    return m_inv, m_t, m_det


def custom_matrix(m: int, n: int):

    if m < 0 or n < 0 or isinstance(m, float) or isinstance(n, float):
        return None
    else:
        matrix = (np.zeros((m, n)))
        for i in range(m):
            for j in range(n):
                if j > i:
                    matrix[i, j] = j
                else:
                    matrix[i, j] = i
        return matrix
