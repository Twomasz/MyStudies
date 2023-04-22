import numpy as np

from typing import Union, Tuple, Optional


def diag_dominant_matrix_A_b(m: int) -> Union[Tuple[np.ndarray, np.ndarray], None]:
    """Funkcja tworząca zestaw składający się z macierzy A (m,m), wektora b (m,) o losowych wartościach całkowitych
    z przedziału 0, 9. Macierz A ma być diagonalnie zdominowana, tzn. wyrazy na przekątnej sa wieksze od pozostałych
    w danej kolumnie i wierszu
    Parameters:
    m int: wymiary macierzy i wektora
    
    Returns:
    Tuple[np.ndarray, np.ndarray]: macierz diagonalnie zdominowana o rozmiarze (m,m) i wektorem (m,)
                                   Jeżeli dane wejściowe niepoprawne funkcja zwraca None
    """
    if isinstance(m, int) and m > 0:
        A = np.random.randint(0, 9, (m, m))
        b = np.random.randint(0, 9, m)
        for k in range(m):
            while A[k][k] <= sum(A[k]) - A[k][k]:
                A[k][k] += 1
        for k in range(m):
            while A[k][k] <= sum(A.T[k]) - A[k][k]:
                A[k][k] += 1
        return A, b
    else:
        return None


def is_diag_dominant(A: np.ndarray) -> Union[bool, None]:
    """Funkcja sprawdzająca czy macierzy A (m,m) jest diagonalnie zdominowana
    Parameters:
    A np.ndarray: macierz wejściowa
    
    Returns:
    bool: sprawdzenie warunku 
          Jeżeli dane wejściowe niepoprawne funkcja zwraca None
    """
    if isinstance(A, np.ndarray):
        if len(A.shape) == 1 and A.shape[0] == 1:
            return True

        elif len(A.shape) > 1 and A.shape[0] == A.shape[1]:
            for k in range(A.shape[0]):
                if A[k][k] <= sum(A[k]) - A[k][k] or A[k][k] <= sum(A.T[k]) - A[k][k]:
                    return None

            return True

        else:
            return None
    else:
        return None


def symmetric_matrix_A_b(m: int) -> Union[Tuple[np.ndarray, np.ndarray], None]:
    """Funkcja tworząca zestaw składający się z macierzy A (m,m), wektora b (m,) o losowych wartościach całkowitych z
    przedziału 0, 9
    Parameters:
    m int: wymiary macierzy i wektora
    
    Returns:
    Tuple[np.ndarray, np.ndarray]: symetryczną macierz o rozmiarze (m,m) i wektorem (m,)
                                   Jeżeli dane wejściowe niepoprawne funkcja zwraca None
    """
    if isinstance(m, int) and m > 0:
        A = np.random.randint(0, 9, (m, m))
        new_A = (A+A.T)/2
        b = np.random.randint(0, 9, m)
        return new_A, b
    else:
        return None


def is_symmetric(A: np.ndarray) -> Union[bool, None]:
    """Funkcja sprawdzająca czy macierzy A (m,m) jest symetryczna
    Parameters:
    A np.ndarray: macierz wejściowa
    
    Returns:
    bool: sprawdzenie warunku 
          Jeżeli dane wejściowe niepoprawne funkcja zwraca None
    """
    if isinstance(A, np.ndarray):
        if len(A.shape) == 1 and A.shape[0] == 1:
            return True

        elif len(A.shape) > 1 and A.shape[0] == A.shape[1]:
            for i in range(A.shape[0]):
                for j in range(A.shape[1]):
                    if A[i][j] != A.T[i][j]:
                        return None
            return True

        else:
            return None
    else:
        return None


def solve_jacobi(A: np.ndarray, b: np.ndarray, x_init: np.ndarray, epsilon: Optional[float] = 1e-8,
                 maxiter: Optional[int] = 100) -> Union[Tuple[np.ndarray, int], None]:
    """Funkcja tworząca zestaw składający się z macierzy A (m,m), wektora b (m,) o losowych wartościach całkowitych
    Parameters:
    A np.ndarray: macierz współczynników
    b np.ndarray: wektor wartości prawej strony układu
    x_init np.ndarray: rozwiązanie początkowe
    epsilon Optional[float]: zadana dokładność
    maxiter Optional[int]: ograniczenie iteracji
    
    Returns:
    np.ndarray: przybliżone rozwiązanie (m,)
                Jeżeli dane wejściowe niepoprawne funkcja zwraca None
    int: iteracja
    """
    if not isinstance(A, np.ndarray) or \
            not isinstance(b, np.ndarray) or \
            not isinstance(x_init, np.ndarray) or \
            not isinstance(epsilon, (float, int)) or \
            not isinstance(maxiter, int) or \
            A.shape[0] != A.shape[1] or not A.shape[0] == b.shape[0] == x_init.shape[0] or \
            epsilon < 0 or maxiter < 0:
        return None

    else:
        D = np.diag(np.diag(A))
        LU = A - D
        x = x_init
        D_inv = np.diag(1 / np.diag(D))
        i = 1
        for i in range(1, maxiter+1):
            x_new = np.dot(D_inv, b - np.dot(LU, x))
            r_norm = np.linalg.norm(x_new - x)
            if r_norm < epsilon:
                return x_new, i
            x = x_new
        return x, i
