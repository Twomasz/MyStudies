# SKOŃCZONE

from copy import deepcopy


class Element:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return f'{self.data}'


class LinkedList:
    def __init__(self, head=None):
        self.head = head

    def destroy(self):
        self.head = None

    def add(self, new_head):
        new_head = deepcopy(new_head)     # use deepcopy to avoid endless loop
        help_value = self.head            # firstly set up pointer on previous head
        self.head = new_head              # secondly set up new head
        self.head.next = help_value

    def remove(self):
        self.head = self.head.next

    def add_last(self, last_elem):
        last_elem = deepcopy(last_elem)   # use deepcopy to avoid endless loop

        if self.head is None:
            self.head = last_elem
        else:
            pointer = self.head

            while pointer.next is not None:
                pointer = pointer.next
            pointer.next = last_elem

    def remove_last(self):
        if self.head is None:
            pass

        elif self.head.next is None:
            self.head = None

        else:
            pointer = self.head
            help_value = pointer

            while pointer.next is not None:
                help_value = pointer
                pointer = pointer.next
            help_value.next = None

    def is_empty(self):
        if self.head is None:
            return True
        else:
            return False

    def length(self):
        counter = 0
        pointer = self.head

        while pointer is not None:
            counter += 1
            pointer = pointer.next
        return counter

    def get(self):
        return self.head.data

    def __str__(self):
        string = ''
        if self.head is None:
            return string
        else:
            pointer = self.head
            while pointer.next is not None:
                string += f'{pointer.data}, '
                pointer = pointer.next
            return string + f'{pointer.data}'

    def take(self, n):
        new_list = LinkedList()
        counter = 1
        pointer = self.head

        while counter <= n and pointer is not None:
            new_list.add_last(Element(pointer.data))
            pointer = deepcopy(pointer.next)
            counter += 1
        return new_list

    def drop(self, n):
        new_list = LinkedList()

        if n >= self.length():
            return new_list

        pointer = self.head
        for _ in range(n):
            pointer = pointer.next

        for _ in range(self.length() - n):
            new_list.add_last(Element(pointer.data))
            pointer = pointer.next

        return new_list


if __name__ == '__main__':
    elem1 = Element(('AGH', 'Kraków', 1919))
    elem2 = Element(('UJ', 'Kraków', 1364))
    elem3 = Element(('PW', 'Warszawa', 1915))
    elem4 = Element(('UW', 'Warszawa', 1915))
    elem5 = Element(('UP', 'Poznań', 1919))
    elem6 = Element(('PG', 'Gdańsk', 1945))

    lista = LinkedList()

    lista.add(elem1)
    lista.add_last(elem2)
    lista.add(elem3)
    lista.add_last(elem4)
    lista.add_last(elem5)
    lista.add(elem6)

    print('Test dodawania elementów na początek i na koniec listy:\n', lista, '\n')

    lista.remove()
    lista.remove_last()

    print('Test usuwania elementów z początku i końca listy:\n', lista, '\n')

    print('Długość listy po usunięciu dwóch z czterech elementów: ', lista.length(), '\n')
    print('Pierwszy element obecnej listy: ', lista.get(), '\n')

    lista.add(elem1)
    lista.add(elem4)

    print('Test metody "take":\n', lista.take(2), '\n')
    print('Test metody "drop":\n', lista.drop(2), '\n')

    print('Test metod "is_empty" i "destroy":')
    print('Przed usunięciem: ', lista.is_empty())
    lista.destroy()
    print('Po usunięciu: ', lista.is_empty())
