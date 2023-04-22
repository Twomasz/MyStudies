# SKOŃCZONE

# względem kodu z zadania podstawowego został tutaj dołożony
# tylko parametr factor do konstruktora
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left_child = None
        self.right_child = None
        self.factor = 0    # współczynnik zrównoważenia


# klasa reprezentująca drzewo AVL z przerobionymi funkcjami z zadania podstawowego
class AVL:
    def __init__(self):
        self.root = None

    def search(self, key):
        def search_inside(node, _key):
            if node is None:
                return None

            else:
                if node.key == _key:
                    return node

                if _key < node.key:
                    return search_inside(node.left_child, _key)

                elif _key > node.key:
                    return search_inside(node.right_child, _key)

        find_node = search_inside(self.root, key)

        if find_node is not None:
            return f'{find_node.key}:{find_node.value}'
        else:
            return None

    def insert(self, elem: Node):
        def insert_inside(node, key, value):
            if node is None:
                node = Node(key, value)

            if key < node.key:
                node.left_child = insert_inside(node.left_child, key, value)
                # nadpisywanie współczynników zrównoważenia
                self.overwrite_factors(node)
                self.restore_balans(node)
                return node

            elif key > node.key:
                node.right_child = insert_inside(node.right_child, key, value)
                # nadpisywanie współczynników zrównoważenia
                self.overwrite_factors(node)
                self.restore_balans(node)
                return node

            elif key == node.key:
                node.value = value
                return node

        self.root = insert_inside(self.root, elem.key, elem.value)

    def delete(self, key):
        # dodana flaga aby nie przy każdym wywołaniu funkcja wykonywała
        # wszystkie instrukcje
        def delete_inside(node, _key, flag: bool):
            if node is None:   # dotarcie do końca gałęzi
                pass

            elif _key == node.key:
                l = node.left_child
                r = node.right_child

                if l is None and r is None:  # node nie ma dzieci
                    return None

                elif l is not None and r is None:  # node ma dziecko na lewo
                    return l      # node przyjmuje wartość dziecka

                elif l is None and r is not None:  # node ma dziecko na prawo
                    return r

                elif l is not None and r is not None:  # node ma dwoje dzieci
                    # znalezienie elementu z min. kluczem (szukanie tylko w lewej podgałęzi)
                    # i przechowanie go w zmiennej min_elem
                    min_elem = r
                    while r.left_child is not None:
                        if r.left_child.key < r.key:
                            min_elem = r.left_child
                        r = r.left_child  # przejście w głąb

                    node = delete_inside(node, min_elem.key, False)    # usuwam z node wybrany do przeniesienia elem

                    min_elem.left_child = node.left_child       # uzupełniam wstawiany elem o lewe i prawe dzieci
                    min_elem.right_child = node.right_child

                    self.overwrite_factors(min_elem)
                    self.restore_balans(min_elem)

                    return min_elem      # zwracam wybrany elem z uzupełnionymi już wskaźnikami

            elif _key > node.key:
                node.right_child = delete_inside(node.right_child, _key, True)
                if flag:   # filtrowanie rzeczonych na wstępie instrukcji
                    self.overwrite_factors(node)
                    self.restore_balans(node)
                return node

            elif _key < node.key:
                node.left_child = delete_inside(node.left_child, _key, True)
                if flag:   # filtrowanie rzeczonych na wstępie instrukcji
                    self.overwrite_factors(node)
                    self.restore_balans(node)
                return node

        self.root = delete_inside(self.root, key, True)

    def print_tree_as_list(self):
        def find_elems(node, held_elems):
            if node is None:
                pass
            else:
                held_elems[node.key] = node.value

                find_elems(node.left_child, held_elems)
                find_elems(node.right_child, held_elems)
                return held_elems

        elems_in_tree = find_elems(self.root, {})

        string = '['
        for key in sorted(elems_in_tree)[:-1]:
            string += f'{key}:{elems_in_tree[key]}, '
        last_key = sorted(elems_in_tree)[-1]

        print(string + f'{last_key}:{elems_in_tree[last_key]}' + ']')

    def __height_inside(self, node):
        if node is None:
            return 0
        else:
            h1 = self.__height_inside(node.right_child)
            h2 = self.__height_inside(node.left_child)
            if h1 > h2:
                return 1 + h1
            else:
                return 1 + h2

    def height(self):
        return self.__height_inside(self.root)

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            self._print_tree(node.right_child, lvl + 5)

            print()
            print(lvl * " ", node.key, node.value)
            print()

            self._print_tree(node.left_child, lvl + 5)

    # w tym miejscu zaczynają się dołożone, względem BST funkcje
    def overwrite_factors(self, node):
        if node is None:
            return None

        node.factor = self.__height_inside(node.right_child) - self.__height_inside(node.left_child)

        self.overwrite_factors(node.left_child)
        self.overwrite_factors(node.right_child)

    def restore_balans(self, node):
        if node.factor == -2:
            if node.left_child.factor == (0 or -1):
                self.LL(node)
            else:
                self.RL(node)

        elif node.factor == 2:
            if node.right_child.factor == (0 or 1):
                self.RR(node)
            else:
                self.LR(node)

        self.overwrite_factors(node)

    @staticmethod
    def LL(node):
        new_node = Node(node.key, node.value)

        node.key = node.left_child.key
        node.value = node.left_child.value

        new_node.left_child, new_node.right_child = node.left_child.right_child, node.right_child
        node.right_child, node.left_child = new_node, node.left_child.left_child

    @staticmethod
    def RR(node):
        new_node = Node(node.key, node.value)

        node.key = node.right_child.key
        node.value = node.right_child.value

        new_node.left_child, new_node.right_child = node.left_child, node.right_child.left_child
        node.left_child, node.right_child = new_node, node.right_child.right_child

    def RL(self, node):
        self.RR(node.left_child)
        self.LL(node)

    def LR(self, node):
        self.LL(node.right_child)
        self.RR(node)


if __name__ == '__main__':
    avl = AVL()
    elems = {50: 'A', 15: 'B', 62: 'C',
             5:  'D', 2:  'E', 1:  'F',
             11: 'G', 100: 'H', 7:  'I',
             6:  'J', 55: 'K', 52: 'L',
             51: 'M', 57: 'N', 8:  'O',
             9:  'P', 10: 'R', 99: 'S',
             12: 'T'}

    for key in elems:
        avl.insert(Node(key, elems[key]))

    avl.print_tree()
    avl.print_tree_as_list()
    print(avl.search(10))
    avl.delete(50)
    avl.delete(52)
    avl.delete(11)
    avl.delete(57)
    avl.delete(1)
    avl.delete(12)
    avl.insert(Node(3, 'AA'))
    avl.insert(Node(4, 'BB'))
    avl.delete(7)
    avl.delete(8)
    avl.print_tree()
    avl.print_tree_as_list()
