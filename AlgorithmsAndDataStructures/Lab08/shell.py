from copy import copy


def ShellSort(tab):
    N = len(tab)  # rozmiar tablicy

    # wyznaczanie optymalnej wartości początkowej dla h
    k = 1
    h = 0
    next_h = 0
    while next_h < N/3:
        h = next_h
        next_h = (3 ** k - 1) // 2
        k += 1

    # sortowanie dopóki h nie osiągnie 1
    while h >= 1:
        for i in range(h, N):
            j = i
            value = tab[i]

            while j >= h and value < tab[j - h]:
                tab[j], tab[j - h] = tab[j - h], tab[j]  # swapowanie
                j -= h

            tab[j] = value

        h //= 3  # odstęp h


def median_2(a, b):
    return (a + b) // 2


def median_3(a, b, c):
    return max(min(a, b), min(c, max(a, b)))


def median_4(a, b, c, d):
    f = max(min(a, b), min(c, d))  # usuwa najmniejsza z 4
    g = min(max(a, b), max(c, d))  # usuwa największą z 4

    return median_2(f, g)


def median_5(a, b, c, d, e):
    f = max(min(a, b), min(c, d))  # usuwa najmniejsza z 4
    g = min(max(a, b), max(c, d))  # usuwa największą z 4

    return median_3(e, f, g)


def median_medians(tab):
    pivot = copy(tab)
    median_tab = []

    while len(pivot) > 1:
        n = 0
        while n + 5 <= len(pivot):
            median = median_5(pivot[n], pivot[n+1], pivot[n+2], pivot[n+3], pivot[n+4])
            median_tab.append(median)
            n += 5

        lasts = len(pivot) - n
        if lasts == 4:  # zostały 4 elementy w liście
            median = median_4(pivot[n], pivot[n+lasts-3], pivot[n+lasts-2], pivot[n+lasts-1])
            median_tab.append(median)

        elif lasts == 3:  # zostały 3 elementy w liście
            median = median_3(pivot[n], pivot[n+lasts-2], pivot[n+lasts-1])
            median_tab.append(median)

        elif lasts == 2:  # zostały 2 elementy w liście
            median = median_2(pivot[n], pivot[n+lasts-1])
            median_tab.append(median)

        elif lasts == 1:  # zostały 1 elementy w liście
            median_tab.append(pivot[n])

        pivot = median_tab
        median_tab = []

    return pivot[0]


def quicksort(tab, start, stop, magic_fives: bool = False):
    # wybieranie pivota albo klasycznie na środku, albo magicznymi piątkami
    if magic_fives:
        pivot = median_medians(tab[start:stop])
    else:
        pivot = tab[(start + stop) // 2]

    i = start
    j = stop

    while i < j:
        while tab[i] < pivot:
            i += 1
        while tab[j] > pivot:
            j -= 1
        if i <= j:
            tab[i], tab[j] = tab[j], tab[i]
            i += 1
            j -= 1

    if j > start:
        quicksort(tab, start, j, magic_fives)
    if i < stop:
        quicksort(tab, i, stop, magic_fives)
