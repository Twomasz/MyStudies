# SKOŃCZONE

from random import random
maxLevel = 5   # zdefiniowanie maksymalnej wysokości elementu


class Node:
    def __init__(self, key, value, elemLevel):
        self.key = key
        self.value = value
        self.next = [None for _ in range(elemLevel)]

    def __str__(self):
        return f'{self.key}:{self.value}'


class SkipList:
    def __init__(self):
        self.maxLevel = maxLevel
        self.head = Node(None, None, maxLevel)  # tworzenie pustego elementu będącego tablicą wskazań na nast. elementy

    def _random_level(self, p=0.5):
        lvl = 1
        while random() < p and lvl < maxLevel:
            lvl += 1
        return lvl

    def display_list(self):
        node = self.head.next[0]  # pierwszy element na poziomie 0
        keys = []                 # lista kluczy na tym poziomie
        while node is not None:
            keys.append(node.key)
            node = node.next[0]

        for lvl in range(maxLevel - 1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head.next[lvl]
            idx = 0
            while node is not None:
                while node.key > keys[idx]:
                    print("->", end=" ")
                    idx += 1
                idx += 1
                print("{:2d}".format(node.key), end=" ")
                node = node.next[lvl]
            print("")

    def search(self, key):
        lvl = maxLevel - 1
        elem = self.head

        while lvl >= 0:
            if elem.next[lvl] is None:
                lvl -= 1
            else:
                if elem.next[lvl].key < key:
                    elem = elem.next[lvl]

                elif elem.next[lvl].key == key:
                    return elem.next[lvl].value

                elif elem.next[lvl].key > key:
                    lvl -= 1

        return None

    def insert(self, key, value):
        # próba znalezienia danego klucza w liście i podmiany wartości
        # (kod prawie identyczny jak w przypadku metody search)
        lvl = maxLevel - 1
        elem = self.head

        while lvl >= 0:
            if elem.next[lvl] is None:
                lvl -= 1
            else:
                if elem.next[lvl].key < key:
                    elem = elem.next[lvl]

                elif elem.next[lvl].key == key:
                    elem.next[lvl].value = value
                    return None

                elif elem.next[lvl].key > key:
                    lvl -= 1

        # w przeciwnym wypadku trzeba będzie dodać nowy element do listy
        elem_to_add = Node(key, value, self._random_level())

        for lvl in range(maxLevel-1, -1, -1):
            predecessor = self.head
            while predecessor.next[lvl] is not None:
                # skakanie po liście
                if predecessor.next[lvl].key < key:
                    predecessor = predecessor.next[lvl]
                else:
                    break

            # dzięki temu warunkowi nie tworzę listy poprzedników (wydaje mi się, że to nie błąd)
            # tylko na bieżąco (na każdym z poziomów) "wciskam" dodawany element
            if lvl < len(elem_to_add.next):
                elem_to_add.next[lvl] = predecessor.next[lvl]
                predecessor.next[lvl] = elem_to_add

    def remove(self, key):
        lvl = maxLevel - 1
        elem = self.head

        while lvl >= 0:
            if elem.next[lvl] is None:
                lvl -= 1
            else:
                if elem.next[lvl].key < key:
                    elem = elem.next[lvl]
                elif elem.next[lvl].key == key:
                    # przenoszenie wskaźnika na następny element na danym poziomie
                    elem.next[lvl] = elem.next[lvl].next[lvl]
                elif elem.next[lvl].key > key:
                    lvl -= 1

    def __str__(self):
        string = ''
        current_elem = self.head.next[0]

        while current_elem.next[0] is not None:
            string += f'{current_elem}, '
            current_elem = current_elem.next[0]

        return string + f'{current_elem}'


def test1():
    skip_lst = SkipList()

    for i in range(1, 16):
        skip_lst.insert(i, chr(64 + i))

    print(skip_lst, '\n')
    print(skip_lst.search(2))
    skip_lst.insert(2, 'Z')
    print(skip_lst.search(2), '\n')
    skip_lst.remove(5)
    skip_lst.remove(6)
    skip_lst.remove(7)
    skip_lst.display_list()
    print()
    skip_lst.insert(6, 'W')
    skip_lst.display_list()


def test2():
    skip_lst = SkipList()

    for i in range(15, 0, -1):
        skip_lst.insert(i, chr(64 + i))

    print(skip_lst, '\n')
    print(skip_lst.search(2))
    skip_lst.insert(2, 'Z')
    print(skip_lst.search(2), '\n')
    skip_lst.remove(5)
    skip_lst.remove(6)
    skip_lst.remove(7)
    skip_lst.display_list()
    print()
    skip_lst.insert(6, 'W')
    skip_lst.display_list()


if __name__ == '__main__':
    test1()
    test2()
