import numpy as np
import typing
from inspect import isfunction
from typing import Union, Tuple


def fun(x):
    return np.exp(-2*x)+x**2-1


def dfun(x):
    return -2*np.exp(-2*x) + 2*x


def ddfun(x):
    return 4*np.exp(-2*x) + 2


def bisection(a: Union[int, float], b: Union[int, float], f: typing.Callable[[float], float], epsilon: float,
              iteration: int) -> Union[Tuple[float, int], None]:
    '''
    funkcja aproksymująca rozwiązanie równania f(x) = 0 na przedziale [a,b] metodą bisekcji.

    Parametry:
    a - początek przedziału
    b - koniec przedziału
    f - funkcja dla której jest poszukiwane rozwiązanie
    epsilon - tolerancja zera maszynowego (warunek stopu)
    iteration - ilość iteracji

    Return:
    float: aproksymowane rozwiązanie
    int: ilość iteracji
    '''
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)) or not isinstance(epsilon, float) or \
            not isinstance(iteration, int) or not isfunction(f) or f(a)*f(b) >= 0 or iteration <= 0:
        return None

    else:
        i = 0
        for i in range(iteration):
            x1 = (a+b)/2
            if np.abs(f(x1)) < epsilon:
                return x1, i
            else:
                if f(a)*f(x1) < 0:
                    b = x1
                else:
                    a = x1
        return x1, i


def secant(a: Union[int, float], b: Union[int, float], f: typing.Callable[[float], float], epsilon: float,
           iteration: int) -> Union[Tuple[float, int], None]:
    '''
    funkcja aproksymująca rozwiązanie równania f(x) = 0 na przedziale [a,b] metodą siecznych.

    Parametry:
    a - początek przedziału
    b - koniec przedziału
    f - funkcja dla której jest poszukiwane rozwiązanie
    epsilon - tolerancja zera maszynowego (warunek stopu)
    iteration - ilość iteracji

    Return:
    float: aproksymowane rozwiązanie
    int: ilość iteracji
    '''
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)) or not isinstance(epsilon, float) or \
            not isinstance(iteration, int) or not isfunction(f) or f(a)*f(b) >= 0 or iteration <= 0:
        return None
    else:
        i = 0
        for i in range(iteration):
            xn = a - f(a)*(a-b)/(f(a)-f(b))

            if np.abs(f(xn)) < epsilon:
                return xn, i
            else:
                if f(a) * f(xn) < 0:
                    b = xn
                else:
                    a = xn
        xn = a - f(a)*(a-b)/(f(a)-f(b))
        return xn, i+1


def newton(f: typing.Callable[[float], float], df: typing.Callable[[float], float],
           ddf: typing.Callable[[float], float], a: Union[int, float], b: Union[int, float], epsilon: float,
           iteration: int) -> Union[Tuple[float, int], None]:
    '''
    Funkcja aproksymująca rozwiązanie równania f(x) = 0 metodą Newtona.
    Parametry: 
    f - funkcja dla której jest poszukiwane rozwiązanie
    df - pochodna funkcji dla której jest poszukiwane rozwiązanie
    ddf - druga pochodna funkcji dla której jest poszukiwane rozwiązanie
    a - początek przedziału
    b - koniec przedziału
    epsilon - tolerancja zera maszynowego (warunek stopu)
    Return:
    float: aproksymowane rozwiązanie
    int: ilość iteracji
    '''

    if not isfunction(f) or not isfunction(df) or not isfunction(ddf) or not isinstance(a, (int, float)) or \
            not isinstance(b, (int, float)) or not isinstance(epsilon, float) or not isinstance(iteration, int) \
            or f(a)*f(b) >= 0 or iteration <= 0 or df(a)*df(b) < 0 or ddf(a)*ddf(b) < 0:
        return None
    else:
        i = 0
        xn = 0
        for i in range(1, iteration+1):
            xn = b - f(b)/df(b)

            if np.abs(f(xn)) < epsilon:
                return xn, i
            else:
                b = xn

        return xn, i
