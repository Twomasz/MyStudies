# SKOŃCZONE

import random
import time
from shell import *
from selection_sort import *


class Element:
    def __init__(self, prio, value=0):
        self.prio = prio    # priorytet
        self.value = value

    def __lt__(self, other):
        return self.prio < other.prio

    def __gt__(self, other):
        return self.prio > other.prio

    def __str__(self):
        return f'{self.prio} : {self.value}'


class HeapSort:
    def __init__(self, tab=None):
        self.heap = []
        self.size = 0
        self.__insert_tab(tab)

    def __insert_tab(self, tab):
        if tab is None:
            pass

        elif isinstance(tab[0], int):
            self.heap = tab
            self.size = len(tab)
            self.heapify()  # zawołanie metody tworzącej kopiec

        elif isinstance(tab[0], tuple):
            for i in tab:
                self.heap.append(Element(i[0], i[1]))
            self.size = len(tab)
            self.heapify()  # zawołanie metody tworzącej kopiec

        else:
            raise ValueError('Nieprawidłowy format danych')

    def is_empty(self):
        if len(self.heap) == 0:
            return True
        else:
            return False

    def peek(self):
        return self.heap[0].value

    def restore_heap(self, elem_idx):  # przywracanie kopca od podanego indeksu
        while True:
            l_idx = self.left(elem_idx)
            r_idx = self.right(elem_idx)

            if r_idx < self.size:   # gdy ma dwoje dzieci
                if self.heap[r_idx] > self.heap[l_idx]:   # prawe dziecko większe od lewego
                    if self.heap[r_idx] > self.heap[elem_idx]:  # jeśli występuje niezgodność
                        self.heap[elem_idx], self.heap[r_idx] = self.heap[r_idx], self.heap[elem_idx]
                        elem_idx = r_idx
                    else:
                        break

                else:    # lewe dziecko większe od prawego
                    if self.heap[l_idx] > self.heap[elem_idx]:  # jeśli występuje niezgodność
                        self.heap[elem_idx], self.heap[l_idx] = self.heap[l_idx], self.heap[elem_idx]
                        elem_idx = l_idx
                    else:
                        break

            elif l_idx < self.size:   # jest tylko lewe dziecko
                if self.heap[l_idx] > self.heap[elem_idx]:  # jeśli występuje niezgodność
                    self.heap[elem_idx], self.heap[l_idx] = self.heap[l_idx], self.heap[elem_idx]
                    elem_idx = l_idx
                else:
                    break

            else:  # gdy nie występują dzieci
                break

    def dequeue(self):
        dequeue_elem = self.heap[0]
        self.heap[0], self.heap[self.size-1] = self.heap[self.size-1], self.heap[0]
        self.size -= 1

        self.restore_heap(0)

        return dequeue_elem

    def enqueue(self, elem):
        self.heap.append(elem)
        self.size += 1
        idx = self.size - 1

        while self.heap[self.parent(idx)] < self.heap[idx]:
            self.heap[self.parent(idx)], self.heap[idx] = self.heap[idx], self.heap[self.parent(idx)]
            idx = self.parent(idx)

    @staticmethod
    def right(index):
        return 2 * index + 2

    @staticmethod
    def left(index):
        return 2 * index + 1

    @staticmethod
    def parent(index):
        parent_idx = (index - 1) // 2
        return parent_idx if parent_idx >= 0 else 0  # zabezpieczenie przed ujemnymi indeksami

    def heapify(self):
        idx_parent_of_last_elem = self.parent(len(self.heap)-1)
        for i in range(idx_parent_of_last_elem, -1, -1):
            self.restore_heap(i)

    def create_sorted_tab_from_heap(self):
        for i in range(self.size):
            self.dequeue()

    def print_tab(self):
        if len(self.heap) == 0:  # pusta tablica
            print('{ }')

        else:
            print('{', end=' ')
            for i in range(len(self.heap) - 1):
                print(self.heap[i], end=', ')
            if self.heap[len(self.heap) - 1]:
                print(self.heap[len(self.heap) - 1], end=' ')
            print('}')

    def print_tree(self, idx, lvl):
        if idx < len(self.heap):
            self.print_tree(self.right(idx), lvl+1)
            print(2 * lvl * '  ', self.heap[idx] if self.heap[idx] else None)
            self.print_tree(self.left(idx), lvl+1)


if __name__ == '__main__':
    int_table = []
    for _ in range(10000):
        int_table.append(random.randint(0, 99))

    # tworzenie kopii takich samych tablic
    int_tab1 = copy(int_table)
    int_tab2 = copy(int_table)
    int_tab3 = copy(int_table)
    int_tab4 = copy(int_table)
    int_tab5 = copy(int_table)

    print('Sortowanie kopcowe:')
    t_start = time.perf_counter()
    # testowana metoda
    Q1 = HeapSort(int_tab1)
    Q1.create_sorted_tab_from_heap()
    print('Wyniki: ', int_tab1)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start), '\n')

    print('Sortowanie przez wstawianie:')
    t_start = time.perf_counter()
    # testowana metoda
    Q2 = SelectionSort(int_tab2)
    Q2.swapping()
    print('Wyniki: ', int_tab2)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start), '\n')

    print('Sortowanie metodą Shella:')
    t_start = time.perf_counter()
    # testowana metoda
    ShellSort(int_tab3)
    print('Wyniki: ', int_tab3)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start), '\n')

    print('Quicksort z pivotem na środku listy:')
    t_start = time.perf_counter()
    # testowana metoda
    quicksort(int_tab4, 0, (len(int_tab4) - 1), magic_fives=False)
    print('Wyniki: ', int_tab4)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start), '\n')

    print('Quicksort z pivotem poprzez medianę median:')
    t_start = time.perf_counter()
    # testowana metoda
    quicksort(int_tab5, 0, (len(int_tab5) - 1), magic_fives=True)
    print('Wyniki: ', int_tab5)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start), '\n')
