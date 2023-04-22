import numpy as np
from typing import Callable


def solve_euler(fun: Callable, t_span: np.array, y0: np.array):
    """
    Funkcja umożliwiająca rozwiązanie układu równań różniczkowych z wykorzystaniem metody Eulera w przód.
    
    Parameters:
    fun: Prawa strona równania. Podana funkcja musi mieć postać fun(t, y). 
    Tutaj t jest skalarem i istnieją dwie opcje dla ndarray y: Może mieć kształt (n,); wtedy fun musi zwrócić
    array_like z kształtem (n,). Alternatywnie może mieć kształt (n, k); wtedy fun musi zwrócić tablicę typu
    array_like z kształtem (n, k), tj. każda kolumna odpowiada jednej kolumnie w y.
    t_span: wektor czasu dla którego ma zostać rozwiązane równanie
    y0: warunke początkowy równania o wymiarze (n,)
    Results:
    (np.array): macierz o wymiarze (n,m) zawierająca w kolumnach kolejne rozwiązania fun w czasie t_span.
    """

    result = np.zeros((t_span.size, y0.size))
    h = t_span[1] - t_span[0]
    result[0] = y0

    for n in range(t_span.size - 1):
        result[n + 1] = result[n] + fun(t_span[n], result[n]) * h
    return result
