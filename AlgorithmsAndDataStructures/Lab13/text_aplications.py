# SKOŃCZONE

def printTab(tab):  # funkcja do testów
    for i in range(len(tab)):
        print(tab[i])


def string_compare(P, T, i, j):
    if i == 0:
        return len(T[:j])
    elif j == 0:
        return len(P[:i])

    change = string_compare(P, T, i-1, j-1) + (P[i] != T[j])
    embed = string_compare(P, T, i, j-1) + 1
    delete = string_compare(P, T, i-1, j) + 1

    min_cost = min(change, embed, delete)

    return min_cost


def string_compare_PD(P, T):
    Y, X = len(P), len(T)

    # wypełnianie tablicy najmniejszych kosztów
    D = [[k for k in range(X)]]
    for m in range(1, Y):
        D.append([m if n == 0 else 0 for n in range(X)])

    # wypełnianie tablicy rodziców
    parent = [['X' if k == 0 else 'I' for k in range(X)]]
    for m in range(1, Y):
        parent.append(['D' if n == 0 else 'X' for n in range(X)])

    for i in range(1, Y):
        for j in range(1, X):
            not_same = P[i] != T[j]
            change = D[i - 1][j - 1] + not_same
            embed = D[i][j - 1] + 1
            delete = D[i - 1][j] + 1

            min_cost = min(change, embed, delete)
            D[i][j] = min_cost

            if min_cost == change:  # zamiana dała najniższy koszt
                if not_same:  # elementy były różne i doszło do zamiany
                    parent[i][j] = 'S'
                else:  # elementy były takie same i nie doszło do zamiany
                    parent[i][j] = 'M'
            elif min_cost == embed:  # wstawienie dała najniższy koszt
                parent[i][j] = 'I'
            else:  # usuwanie dało najniższy koszt
                parent[i][j] = 'D'

    return D, parent


def recreate_path(parent, j=None):
    i = len(parent)-1

    if j is None:
        j = len(parent[0]) - 1

    path = ''

    while parent[i][j] != 'X':
        char = parent[i][j]
        path += char

        if char == 'M' or char == 'S':
            j -= 1
            i -= 1

        elif char == 'D':
            i -= 1

        elif char == 'I':
            j -= 1

    return path[::-1]


def goal_cell(D):
    i = len(D)-1
    j = 0

    for k in range(1, len(D[0])):
        if D[i][k] < D[i][j]:
            j = k

    return j


def string_compare_PD_vol2(P, T):
    Y, X = len(P), len(T)

    # wypełnianie tablicy najmniejszych kosztów
    D = [[0 for _ in range(X)]]
    for m in range(1, Y):
        D.append([m if n == 0 else 0 for n in range(X)])

    # wypełnianie tablicy rodziców
    parent = [['X' for _ in range(X)]]
    for m in range(1, Y):
        parent.append(['D' if n == 0 else 'X' for n in range(X)])

    for i in range(1, Y):
        for j in range(1, X):
            not_same = P[i] != T[j]
            change = D[i - 1][j - 1] + not_same
            embed = D[i][j - 1] + 1
            delete = D[i - 1][j] + 1

            min_cost = min(change, embed, delete)
            D[i][j] = min_cost

            if min_cost == change:  # zamiana dała najniższy koszt
                if not_same:  # elementy były różne i doszło do zamiany
                    parent[i][j] = 'S'
                else:  # elementy były takie same i nie doszło do zamiany
                    parent[i][j] = 'M'
            elif min_cost == embed:  # wstawienie dała najniższy koszt
                parent[i][j] = 'I'
            else:  # usuwanie dało najniższy koszt
                parent[i][j] = 'D'

    return D, parent


def string_compare_PD_vol3(P, T):
    Y, X = len(P), len(T)

    # wypełnianie tablicy najmniejszych kosztów
    D = [[k for k in range(X)]]
    for m in range(1, Y):
        D.append([m if n == 0 else 0 for n in range(X)])

    # wypełnianie tablicy rodziców
    parent = [['X' if k == 0 else 'I' for k in range(X)]]
    for m in range(1, Y):
        parent.append(['D' if n == 0 else 'X' for n in range(X)])

    for i in range(1, Y):
        for j in range(1, X):
            not_same = P[i] != T[j]

            big_number = 0
            if not_same:
                big_number = X**2 * Y**2

            change = D[i - 1][j - 1] + big_number
            embed = D[i][j - 1] + 1
            delete = D[i - 1][j] + 1

            min_cost = min(change, embed, delete)
            D[i][j] = min_cost

            if min_cost == change:  # zamiana dała najniższy koszt
                if not_same:  # elementy były różne i doszło do zamiany
                    parent[i][j] = 'S'
                else:  # elementy były takie same i nie doszło do zamiany
                    parent[i][j] = 'M'
            elif min_cost == embed:  # wstawienie dała najniższy koszt
                parent[i][j] = 'I'
            else:  # usuwanie dało najniższy koszt
                parent[i][j] = 'D'

    return D, parent


def find_common_sequence(path, T):
    path = path.replace('D', '')

    result = ''
    for i in range(len(path)-1):
        if path[i] == 'M':
            result += T[i+1]

    return result


def prepare_P(T):
    lst_P = [int(elem) for elem in T if elem != ' ']

    lst_P.sort()

    P = ' '
    for number in lst_P:
        P += str(number)

    return P


def pkt_a():
    P1 = ' kot'
    T1 = ' koń'

    P2 = ' kot'
    T2 = ' pies'

    print(string_compare(P1, T1, len(P1) - 1, len(T1) - 1))
    print(string_compare(P2, T2, len(P2) - 1, len(T2) - 1))


def pkt_b():
    P1 = ' kot'
    T1 = ' koń'

    P2 = ' kot'
    T2 = ' pies'

    print(string_compare_PD(P1, T1))
    print(string_compare_PD(P2, T2))


def pkt_c():
    P = ' thou shalt not'
    T = ' you should not'

    D, parent = string_compare_PD(P, T)

    print(recreate_path(parent))


def pkt_d():
    P = ' ban'
    T = ' mokeyssbanana'

    D, parent = string_compare_PD_vol2(P, T)  # przerobiona funkcja (zmienione pierwsze wiersze w macierzach D i parent)

    j = goal_cell(D)
    print(j)
    recreate_path(parent, j)


def pkt_e():
    P = ' democrat'
    T = ' republican'

    D, parent = string_compare_PD_vol3(P, T)  # przerobiona funkcja -dodawanie dużej liczby blokującej możliwość zamiany

    path = recreate_path(parent)
    print(find_common_sequence(path, T))


def pkt_f():
    T = ' 243517698'
    P = prepare_P(T)

    D, parent = string_compare_PD_vol3(P, T)  # przerobiona funkcja -dodawanie dużej liczby blokującej możliwość zamiany

    path = recreate_path(parent)
    print(find_common_sequence(path, T))


if __name__ == '__main__':
    pkt_a()
    pkt_b()
    pkt_c()
    pkt_d()
    pkt_e()
    pkt_f()
