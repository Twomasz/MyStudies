import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
from numpy.core._multiarray_umath import ndarray
from numpy.polynomial import polynomial as P
import pickle


# zad1
def polly_A(x: np.ndarray):
    """Funkcja wyznaczajaca współczynniki wielomianu przy znanym wektorze pierwiastków.
    Parameters:
    x: wektor pierwiastków
    Results:
    (np.ndarray): wektor współczynników
        Jeżeli dane wejściowe niepoprawne funkcja zwraca None
    """
    if not isinstance(x, np.ndarray):
        return None

    return P.polyfromroots(x)


def roots_20(a: np.ndarray):
    """Funkcja zaburzająca lekko współczynniki wielomianu na postawie wyznaczonych współczynników wielomianu
        oraz zwracająca dla danych współczynników, miejsca zerowe wielomianu funkcją polyroots.
    Parameters:
    a: wektor współczynników
    Results:
    (np.ndarray, np. ndarray): wektor współczynników i miejsc zerowych w danej pętli
        Jeżeli dane wejściowe niepoprawne funkcja zwraca None
    """
    if not isinstance(a, np.ndarray):
        return None

    for i in range(len(a)):
        perturbation = 10e-10 * np.random.random_sample()
        a[i] += perturbation
    return a, P.polyroots(a)


# zad 2
def frob_a(wsp: np.ndarray):
    """Funkcja zaburzająca lekko współczynniki wielomianu na postawie wyznaczonych współczynników wielomianu
        oraz zwracająca dla danych współczynników, miejsca zerowe wielomianu funkcją polyroots.
    Parameters:
    a: wektor współczynników
    Results:
    (np.ndarray, np. ndarray, np.ndarray, np. ndarray,): macierz Frobenusa o rozmiarze nxn, gdzie n-1 stopień wielomianu,
    wektor własności własnych, wektor wartości z rozkładu schura, wektor miejsc zerowych otrzymanych za pomocą funkcji polyroots

        Jeżeli dane wejściowe niepoprawne funkcja zwraca None
    """
    if not isinstance(wsp, np.ndarray):
        return None

    m = len(wsp)
    frob = np.zeros((m, m))
    for i in range(m - 1):
        frob[i][i + 1] = 1  # ones on subdiagonal

    for j in range(m):
        frob[-1][j] = -wsp[j]  # last row as coefficient of polynomial

    return frob, np.linalg.eigvals(frob), scipy.linalg.schur(frob), P.polyroots(wsp)
