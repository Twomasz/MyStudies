# SKOŃCZONE

def realloc(tab, size):
    old_size = len(tab)
    return [tab[i] if i < old_size else None for i in range(size)]


class Queue:
    def __init__(self):
        self.tab = [None for _ in range(5)]
        self.size = len(self.tab)
        self.front = 0
        self.back = 0

    def is_empty(self):
        return self.front == self.back

    def peek(self):
        if self.back == self.front:
            return None
        return self.tab[self.front]

    def dequeue(self):
        if self.back == self.front:
            return None

        self.front += 1
        if self.front == self.size:
            self.front = 0

        return self.tab[self.front]

    def enqueue(self, elem):

        self.tab[self.back] = elem      # dodanie nowego elementu
        self.back += 1                  # zwiększenie indeksu odczytu

        if self.back == self.size:      # zapętlenie indeksu zapisu w przypadku dojścia do końca tablicy
            self.back = 0

        if self.back == self.front:     # dwukrotne powiększenie tablicy i wszystko co się z tym wiąże
            last_elems = self.tab[self.front:]            # wszystkie elem. tablicy od idx odczytu do końca tablicy
            self.tab = realloc(self.tab, self.size * 2)   # powiększenie dwukrotne rozmiaru tablicy
            self.front += self.size                       # powiększenie idx odczytu o połowę rozm. nowej tablicy
            self.tab[self.front:] = last_elems            # wpisanie ostatnich elem. starej tablicy na koniec nowej
            self.size *= 2                                # końcowo powiększenie rozmiaru nowej tablicy
            # nie przejmujemy się śmieciami pozostałymi na końcowych elementach starej tablicy,
            # gdyż potem możemy je nadpisać nowymi
        return self.front, self.back

    def print_queue(self):
        if self.front == self.back:    # sytuacja pustej kolejki
            print('[]')

        elif self.front > self.back:   # sytuacja gdy tablica się zawija
            last_elems = self.tab[self.front:]     # część kolejki zawarta na końcu tablicy
            first_elems = self.tab[0: self.back]   # część kolejki zawarta na początku tablicy
            print(f'{last_elems + first_elems}')

        else:                          # sytuacja, gdy kolejka jest zawarta w środku tablicy
            print(f'{self.tab[self.front:self.back]}')

    def print_tab(self):
        print(self.tab)


if __name__ == '__main__':
    q = Queue()
    for j in range(1, 5):
        q.enqueue(j)
    print(q.dequeue())
    q.peek()
    q.print_queue()
    for k in range(5, 9):
        q.enqueue(k)
    q.print_tab()
    while q.is_empty():
        q.dequeue()
    q.print_queue()
