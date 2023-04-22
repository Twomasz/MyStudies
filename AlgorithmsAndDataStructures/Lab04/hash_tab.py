# SKOŃCZONE

class Element:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f'{self.key}: {self.value}'


class HashTable:
    def __init__(self, size, c1=1, c2=0):
        self.tab = [None for _ in range(size)]
        self.size = size
        self.c1 = c1
        self.c2 = c2

    def hash(self, key):    # funkcja hashująca
        if isinstance(key, int):
            return key % self.size

        elif isinstance(key, str):
            str_key = 0
            for char in list(key):
                str_key += ord(char)

            return str_key % self.size

        else:
            print('Zły rodzaj klucza')

    def insert_index(self, index, key):
        cant_find_empty_place = False

        i = 0
        start_index = index
        while self.tab[index] is not None and i < self.size:    # warunek zabezpieczający
            # sprawdzanie czy element tablicy o podanym indeksie jest taki sam
            # jak elementu przy wywołaniu tej funkcji
            if self.tab[index].key == key:
                break

            # dzielenie modulo zapewnia zawijanie indeksu z końca na początek
            i += 1
            index = (start_index + self.c1 * i + self.c2 * i ** 2) % self.size

        if i == self.size:
            cant_find_empty_place = True

        return index, cant_find_empty_place

    def insert(self, elem: Element):
        index = self.hash(elem.key)   # hashowanie indeksu do wpisu

        if self.tab[index] is None:      # wolne miejsce
            self.tab[index] = elem

        else:              # zbieżność indeksów
            index, cant_find_empty_place = self.insert_index(index, elem.key)

            if cant_find_empty_place:
                print('Brak miejsca')
            else:
                self.tab[index] = elem

    def search_remove_index(self, index, key):
        same_keys = False

        start_index = index
        for i in range(self.size):
            # sprawdzanie czy element tablicy o podanym indeksie jest taki sam
            # jak elementu przy wywołaniu tej funkcji
            if self.tab[index] is not None and self.tab[index].key == key:
                same_keys = True
                break

            # dzielenie modulo zapewnia zawijanie indeksu z końca na początek
            index = (start_index + self.c1 * i + self.c2 * i ** 2) % self.size

        return index, same_keys

    def remove(self, key):
        index = self.hash(key)
        index, same_keys = self.search_remove_index(index, key)

        if same_keys:
            self.tab[index] = None
        else:
            print('Brak danej')

    def search(self, key):
        index = self.hash(key)
        index, same_keys = self.search_remove_index(index, key)

        if same_keys:
            return self.tab[index]
        else:
            return None

    def __str__(self):
        string = '{'
        for i in range(self.size - 1):
            string += f'{self.tab[i]}, '

        return string + f'{self.tab[-1]}' + '}'


def test1(c1, c2):
    table1 = HashTable(13, c1, c2)

    for i in range(1, 6):
        table1.insert(Element(i, chr(64 + i)))
    table1.insert(Element(18, 'F'))
    table1.insert(Element(31, 'G'))
    for i in range(8, 16):
        table1.insert(Element(i, chr(64 + i)))

    print(table1)
    print(table1.search(5))
    print(table1.search(14))
    table1.insert(Element(5, 'Z'))
    print(table1.search(5))
    table1.remove(5)
    print(table1)
    print(table1.search(31))
    table1.insert(Element('test', 'W'))
    print(table1)


def test2(c1, c2):
    table2 = HashTable(13, c1, c2)

    for i in range(1, 14):
        table2.insert(Element(13*i, chr(64 + i)))
    print(table2)


if __name__ == '__main__':
    test1(1, 0)
    # test2(1, 0)
    # # w przypadku próbkowania kwadratowego powstaje powstaje 13sto elementowy ciąg
    # # powtarzających się indeksów, które nie trafiają w wolne miejsca
    # test2(0, 1)
    # test1(0, 1)
