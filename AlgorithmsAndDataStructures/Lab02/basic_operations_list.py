# NIESKOŃCZONY

from copy import deepcopy


class Element:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __str__(self):
        return f'{self.data}'


# OPERACJE BAZOWE
def nil():
    return None


def cons(elem: Element, lst):
    elem = deepcopy(elem)
    new_head = Element(elem)
    if lst is None:
        return new_head
    new_head.next = lst
    return new_head


def first(lst):
    return lst.data


def rest(lst):
    return lst.next


# INTERFEJS
def create():
    return nil()


def destroy():
    return None


def add(new_head, lst):
    return cons(new_head, lst)


def remove(lst):
    return rest(lst)


def add_end(el, lst):
    if is_empty(lst):
        return cons(el, lst)  # dojście do końca i wstawienie tam elementu
    else:
        first_el = first(lst)  # podział listy na: pierwszy element
        rest_lst = rest(lst)  # i całą resztę
        recreated_lst = add_end(el, rest_lst)  # 'zejście 'w dół' rekurencji z przekazaniem dodawanego elementu,
        # przy powrocie 'w górę' zwracana jest odtworzona lista
        return cons(first_el, recreated_lst)  # cons dołącza pierwszy element do 'odtwarzanej' przez rekurencję listy
        # zmienne first-el, rest_lst i recreated_lst są wprowadzone pomocniczo, dla wyjaśnienia działania funkcji


def remove_end(lst):
    if is_empty(rest(lst)):
        lst = None
        return lst
    else:
        first_el = first(lst)
        rest_lst = rest(lst)
        recreated_lst = remove_end(rest_lst)

        return cons(first_el, recreated_lst)


def is_empty(lst):
    if lst is None:
        return True
    else:
        return False


def length(lst):
    if lst is None:
        return 0
    else:
        return 1 + length(rest(lst))


def get(lst):
    return first(lst)


def print_list(lst):
    if lst is None:
        return ''
    else:
        return f'{first(lst)} ' + print_list(rest(lst))


def take(n, lst):
    new_lst = create()
    counter = 1
    help_lst = lst

    while counter <= n and help_lst is not None:
        new_lst = add_end(first(help_lst), new_lst)
        counter += 1
        help_lst = rest(help_lst)

    return new_lst


def drop(n, lst):
    new_lst = create()

    if n >= length(lst):
        return new_lst

    help_lst = lst
    for _ in range(n):
        help_lst = rest(help_lst)

    for _ in range(length(lst) - n):
        new_lst = add_end(first(help_lst), new_lst)
        help_lst = rest(help_lst)

    return new_lst


if __name__ == '__main__':
    elem1 = Element(('AGH', 'Kraków', 1919))
    elem2 = Element(('UJ', 'Kraków', 1364))
    elem3 = Element(('PW', 'Warszawa', 1915))
    elem4 = Element(('UW', 'Warszawa', 1915))
    elem5 = Element(('UP', 'Poznań', 1919))
    elem6 = Element(('PG', 'Gdańsk', 1945))

    lista = create()

    lista = add(elem1, lista)
    lista = add_end(elem2, lista)
    lista = add(elem3, lista)
    lista = add_end(elem4, lista)
    lista = add_end(elem5, lista)
    lista = add(elem6, lista)

    print('Test dodawania elementów na początek i na koniec listy:\n', print_list(lista), '\n')

    lista = remove(lista)
    lista = remove_end(lista)

    print('Test usuwania elementów z początku i końca listy:\n', print_list(lista), '\n')

    print('Długość listy po usunięciu dwóch z czterech elementów: ', length(lista), '\n')
    print('Pierwszy element obecnej listy: ', get(lista), '\n')

    lista = add(elem1, lista)
    lista = add(elem4, lista)

    print('Test metody "take":\n', print_list(take(2, lista)), '\n')
    print('Test metody "drop":\n', print_list(drop(2, lista)), '\n')

    print('Test metod "is_empty" i "destroy":')
    print('Przed usunięciem: ', is_empty(lista))
    lista = destroy()
    print('Po usunięciu: ', is_empty(lista))
