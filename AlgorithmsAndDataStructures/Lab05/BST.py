# SKOŃCZONE

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left_child = None
        self.right_child = None


class Root:
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
                return node

            elif key > node.key:
                node.right_child = insert_inside(node.right_child, key, value)
                return node

            elif key == node.key:
                node.value = value
                return node

        self.root = insert_inside(self.root, elem.key, elem.value)

    def delete(self, key):
        def delete_inside(node, _key):
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

                    node = delete_inside(node, min_elem.key)    # usuwam z node wybrany do przeniesienia elem
                    min_elem.left_child = node.left_child       # uzupełniam wstawiany elem o lewe i prawe dzieci
                    min_elem.right_child = node.right_child
                    return min_elem                             # zwracam wybrany elem z uzupełnionymi już wskaźnikami

            elif _key > node.key:
                node.right_child = delete_inside(node.right_child, _key)
                return node

            elif _key < node.key:
                node.left_child = delete_inside(node.left_child, _key)
                return node

        self.root = delete_inside(self.root, key)

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

    def height(self):
        def height_inside(node):
            if node is None:
                return 0
            else:
                h1 = height_inside(node.right_child)
                h2 = height_inside(node.left_child)
                if h1 > h2:
                    return 1 + h1
                else:
                    return 1 + h2

        return height_inside(self.root)

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


if __name__ == '__main__':
    elems = {50: 'A', 15: 'B', 62: 'C', 5: 'D', 20: 'E', 58: 'F', 91: 'G', 3: 'H', 8: 'I', 37: 'J', 60: 'K', 24: 'L'}

    bst = Root()
    for i in elems:
        bst.insert(Node(i, elems[i]))

    bst.print_tree()
    bst.print_tree_as_list()
    print(bst.search(24))
    bst.insert(Node(20, 'AA'))
    bst.insert(Node(6, 'M'))
    bst.delete(62)
    bst.insert(Node(59, 'N'))
    bst.insert(Node(100, 'P'))
    bst.delete(8)
    bst.delete(15)
    bst.insert(Node(55, 'R'))
    bst.delete(50)
    bst.delete(5)
    bst.delete(24)
    print(bst.height())
    bst.print_tree_as_list()
    bst.print_tree()
