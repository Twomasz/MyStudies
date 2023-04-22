# SKOŃCZONE

tabSize = 6


# Unrolled Linked List Node
class Tab:
    def __init__(self):
        self.tabElems = 0
        self.tab = [None for _ in range(tabSize)]
        self.next = None


class UnrolledList:
    def __init__(self):
        self.lst = None
        self.lstElems = 0
        self.index_of_last_elem = 0

    def __push_elems_in_list(self, current_elem, index):
        next_tab = current_elem.next

        elems_to_push = current_elem.tab[tabSize//2:]   # pobranie drugiej połowy tablicy
        current_elem.tab[tabSize//2:] = [None for _ in range(tabSize // 2)]
        current_elem.tabElems = tabSize//2  # aktualizacja liczby elem obecnej tab

        current_elem.next = Tab()  # tworzenie pustej tablicy wstawianej między istniejące
        current_elem.next.tab[0:tabSize//2] = elems_to_push  # przenoszenie tam elementów
        current_elem.next.tabElems += tabSize//2

        current_elem.next.next = next_tab

        if index >= tabSize//2:
            current_elem = current_elem.next
            index %= tabSize//2

        return current_elem, index

    def __push_elems_in_tab(self, current_elem, index):
        i = tabSize - 2     # index przedostatniego elementu
        while i >= index:
            if current_elem.tab[i] is not None:
                current_elem.tab[i + 1] = current_elem.tab[i]
            i -= 1

    def insert(self, index, data):
        if self.lst is None:    # Inicjowanie piewzsego elementu listy :)
            self.lst = Tab()

        if index > self.lstElems:
            self.index_of_last_elem += 1   # aktualizacja indeksu ostatniego elementu
            index = self.index_of_last_elem  # dodawanie na koniec listy :D

        which_tab = index // tabSize  # przyporządkowanie tablicy do której ma trafić elem
        index %= tabSize

        current_elem = self.lst
        for i in range(which_tab):
            if current_elem.next is None:  # inicjowanie elementu listy jeśli go nie ma
                current_elem.next = Tab()
            current_elem = current_elem.next   # przeiterowanie po liście

        if current_elem.tabElems == tabSize:
            current_elem, index = self.__push_elems_in_list(current_elem, index)

        if current_elem.tab[index] is not None:
            self.__push_elems_in_tab(current_elem, index)

        current_elem.tab[index] = data
        current_elem.tabElems += 1
        self.lstElems += 1

    def delete(self, index):
        which_tab = index // tabSize  # przyporządkowanie tablicy do której ma trafić elem
        index %= tabSize

        current_elem = self.lst
        for i in range(which_tab):
            current_elem = current_elem.next  # przeiterowanie po liście

        current_elem.tab[index] = None
        current_elem.tabElems -= 1
        self.lstElems -= 1

        for i in range(index, tabSize - 1):
            current_elem.tab[i] = current_elem.tab[i+1]  # przesuwanie elenetów w tablicy
        current_elem.tab[tabSize-1] = None   # czyszczenie ostatniego elementu tablicy

        if current_elem.tabElems < tabSize//2:
            next_elem = current_elem.next
            current_elem.tab[tabSize//2-1] = next_elem.tab[0]  # przenoszenie elementu z następnej tablicy do obecnej
            for i in range(0, tabSize - 1):
                next_elem.tab[i] = next_elem.tab[i + 1]  # przesuwanie elenetów w tablicy
            next_elem.tab[tabSize - 1] = None  # czyszczenie ostatniego elementu tablicy
            next_elem.tabElems -= 1

            if next_elem.tabElems < tabSize:    # gdy nastepna tablica ma mniej niż połowę elementów
                elem_to_push = next_elem.tab[0:tabSize // 2]    # wybranie elementów do przeniesienia
                current_elem.tab[tabSize//2:] = elem_to_push
                current_elem.next = current_elem.next.next      # usunięcie następnej tablicy poprzez przeniesienie wskaźnika na jeszcze dalszą tablicę

    def get(self, index):
        which_tab = index // tabSize  # przyporządkowanie tablicy do której ma trafić elem
        index %= tabSize

        current_elem = self.lst
        for i in range(which_tab):
            current_elem = current_elem.next   # przeiterowanie po liście

        return current_elem.tab[index]

    def print_list(self):
        current_tab = self.lst
        while current_tab is not None:
            print(current_tab.tab)
            current_tab = current_tab.next


if __name__ == '__main__':
    lista = UnrolledList()
    for i in range(9):
        lista.insert(i, i+1)
    print(lista.get(4), '\n')
    lista.insert(1, 10)
    lista.insert(8, 11)
    lista.print_list()
    print()
    lista.delete(1)
    lista.delete(2)
    lista.print_list()
