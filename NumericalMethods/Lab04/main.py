import numpy as np
import scipy
import pickle
import matplotlib.pyplot as plt

from typing import Union, List, Tuple


def chebyshev_nodes(n: int = 10) -> Union[None, np.ndarray]:
    if not isinstance(n, int) or n <= 0:
        return None

    return np.array([np.cos(k*np.pi/n) for k in range(n + 1)])


def bar_czeb_weights(n: int = 10) -> Union[None, np.ndarray]:
    if not isinstance(n, int) or n <= 0:
        return None

    delta = [1.0 for i in range(1, n)]
    delta.insert(0, 0.5)
    delta.append(0.5)

    return np.array([(-1) ** j * delta[j] for j in range(n+1)])


def barycentric_inte(xi: np.ndarray, yi: np.ndarray, wi: np.ndarray, x: np.ndarray) -> Union[None, np.ndarray]:

    '''
    Parameters:
    xi(np.ndarray): węzły interpolacji w postaci wektora(m, ), gdzie m > 0
    yi(np.ndarray): wartości funkcji interpolowanej w węzłach w postaci wektora(m, ), gdzie m > 0
    wi(np.ndarray): wagi interpolacji w postaci wektora(m, ), gdzie m > 0
    x(np.ndarray): argumenty dla funkcji interpolującej(n, ), gdzie n > 0
    '''


    if isinstance(xi, np.ndarray) and isinstance(yi, np.ndarray) and isinstance(wi, np.ndarray) and isinstance(x,
                                                                                                           np.ndarray):

        Y = []
        try:
            for x in np.nditer(x):
                if x in xi:
                    # omijamy dzielenie przez 0
                    Y.append(yi[np.where(xi == x)[0][0]])
                else:
                    # wzór w drugiej formie
                    L = wi / (x - xi)
                    Y.append(yi @ L / sum(L))
            return np.array(Y)
        except:
            return None

    return None


def L_inf(xr: Union[int, float, List, np.ndarray], x: Union[int, float, List, np.ndarray]) -> float:

    if np.array([xr]).shape != np.array([x]).shape:
        return np.nan
    try:
        return max(abs(np.array(xr) - np.array(x)))
    except:
        return abs(xr - x) if isinstance(xr, (int, float)) and isinstance(x, (int, float)) else np.nan
