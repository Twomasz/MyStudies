import numpy as np
import scipy
import pickle

from typing import Union, List, Tuple


def absolut_error(v: Union[int, float, List, np.ndarray], v_aprox: Union[int, float, List, np.ndarray])\
        -> Union[int, float, np.ndarray]:

    if not isinstance(v, (int, float, list, np.ndarray)) or not isinstance(v_aprox, (int, float, list, np.ndarray)):
        return np.nan
    elif isinstance(v, (list, np.ndarray)) and isinstance(v_aprox, (list, np.ndarray)) and len(v) != len(v_aprox):
        return np.nan

    value = abs(np.array(v) - np.array(v_aprox))

    return value


def relative_error(v: Union[int, float, List, np.ndarray], v_aprox: Union[int, float, List, np.ndarray]) \
        -> Union[int, float, np.ndarray]:

    if not isinstance(v, (int, float, list, np.ndarray)) or not isinstance(v_aprox, (int, float, list, np.ndarray)):
        return np.nan
    elif isinstance(v, (list, np.ndarray)) and isinstance(v_aprox, (list, np.ndarray)) and len(v) != len(v_aprox):
        return np.nan
    elif isinstance(v, (int, float)) and v == 0:
        return np.nan
    if isinstance(v, (list, np.ndarray)):
        for x in range(len(v)):
            if v[x] == 0.0:
                return np.nan

    value = abs((np.array(v) - np.array(v_aprox)) / v)

    return value


def p_diff(n: int, c: float) -> float:

    if not isinstance(n, int) or not isinstance(c, (int, float)):
        return np.nan
    b = 2 ** n
    p1 = b - b + c
    p2 = b + c - b
    value = abs(p1 - p2)

    return value


def exponential(x: Union[int, float], n: int) -> float:

    if not isinstance(x, (int, float)) or not isinstance(n, int) or n <= 0:
        return np.nan

    def silnia(i: int):
        value = 1
        for k in range(1, i + 1):
            value = value * k
        return value

    expon = 0.0

    for i in range(n):
        expon += 1/silnia(i) * x ** i
    return expon


def coskx1(k: int, x: Union[int, float]) -> float:

    if not isinstance(k, int) or not isinstance(x, (int, float)) or k < 0:
        return np.nan
    elif k == 0:
        return 1
    elif k == 1:
        return np.cos(x)
    else:
        value = 2 * np.cos(x) * coskx1(k - 1, x) - coskx1(k - 2, x)
        return value


def coskx2(k: int, x: Union[int, float]) -> Tuple[float, float]:

    if not isinstance(k, int) or not isinstance(x, (int, float)) or k < 0:
        return np.nan
    if k == 1:
        return np.cos(x), np.sin(x)
    elif k == 0:
        return 1, 0
    else:
        v_cos = np.cos(x) * coskx2(k-1, x)[0] - np.sin(x)* coskx2(k-1, x)[1]
        v_sin = np.sin(x) * coskx2(k-1, x)[0] + np.cos(x)* coskx2(k-1, x)[1]
        return v_cos, v_sin


def pi(n: int) -> float:

    if not isinstance(n, int) or n <= 0:
        return np.nan

    series = 0
    for i in range(1, n + 1):
        series += 1/i ** 2

    value_pi = (6 * series) ** (1/2)

    return value_pi
