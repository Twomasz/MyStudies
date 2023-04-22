# SKOŃCZONE

class Element:
    def __init__(self, prio, value):
        self.prio = prio    # priorytet
        self.value = value

    def __lt__(self, other):
        return self.prio < other.prio

    def __gt__(self, other):
        return self.prio > other.prio

    def __str__(self):
        return f'{self.prio} : {self.value}'


class PrioQueue:
    def __init__(self):
        self.tab = []

    def is_empty(self):
        if len(self.tab) == 0:
            return True
        else:
            return False

    def peek(self):
        return self.tab[0].value

    def dequeue(self):
        self.tab[0], self.tab[-1] = self.tab[-1], self.tab[0]
        dequeue_elem = self.tab.pop(-1)

        # przywracanie kopca
        idx = 0
        while True:
            l_idx = self.left(idx)
            r_idx = self.right(idx)
            size = len(self.tab)
            if r_idx < size:   # gdy ma dwoje dzieci
                if self.tab[r_idx] > self.tab[l_idx]:    # prawe dziecko większe od lewego
                    if self.tab[r_idx] > self.tab[idx]:  # jeśli występuje niezgodność
                        self.tab[idx], self.tab[r_idx] = self.tab[r_idx], self.tab[idx]
                        idx = r_idx
                    else:
                        break

                else:    # lewe dziecko większe od prawego
                    if self.tab[l_idx] > self.tab[idx]:  # jeśli występuje niezgodność
                        self.tab[idx], self.tab[l_idx] = self.tab[l_idx], self.tab[idx]
                        idx = l_idx
                    else:
                        break

            elif l_idx < size:   # jest tylko lewe dziecko
                if self.tab[l_idx] > self.tab[idx]:     # jeśli występuje niezgodność
                    self.tab[idx], self.tab[l_idx] = self.tab[l_idx], self.tab[idx]
                    idx = l_idx
                else:
                    break

            else:  # gdy nie występują dzieci
                break

        return dequeue_elem.value

    def enqueue(self, elem: Element):
        self.tab.append(elem)
        idx = len(self.tab) - 1

        while self.tab[self.parent(idx)] < self.tab[idx]:
            self.tab[self.parent(idx)], self.tab[idx] = self.tab[idx], self.tab[self.parent(idx)]
            idx = self.parent(idx)

    def right(self, index):
        return 2 * index + 2

    def left(self, index):
        return 2 * index + 1

    def parent(self, index):
        parent_idx = (index - 1) // 2
        return parent_idx if parent_idx >= 0 else 0  # zabezpieczenie przed ujemnymi indeksami

    def print_tab(self):
        if len(self.tab) == 0:  # pusta tablica
            print('{ }')

        else:
            print('{', end=' ')
            for i in range(len(self.tab)-1):
                print(self.tab[i], end=', ')
            if self.tab[len(self.tab)-1]:
                print(self.tab[len(self.tab)-1], end=' ')
            print('}')

    def print_tree(self, idx, lvl):
        if idx < len(self.tab):
            self.print_tree(self.right(idx), lvl+1)
            print(2*lvl*'  ', self.tab[idx] if self.tab[idx] else None)
            self.print_tree(self.left(idx), lvl+1)


if __name__ == '__main__':
    Q = PrioQueue()

    keys = [4, 7, 6, 7, 5, 2, 2, 1]
    data = 'ALGORYTM'

    for j, key in enumerate(keys):
        Q.enqueue(Element(key, data[j]))

    Q.print_tree(0, 0)
    Q.print_tab()
    print(Q.dequeue())
    print(Q.peek())
    Q.print_tab()

    while not Q.is_empty():
        Q.dequeue()
    Q.print_tab()
