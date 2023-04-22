# SKOŃCZONE

from graph_implementation import *


def dfs_iterative(G: Union[AdjacencyList, AdjacencyMatrix], start_v):
    stack = [start_v]
    visited = []

    while stack:
        d = stack.pop(-1)
        if d not in visited:
            visited.append(d)
            for u in G.neighbours(d):
                stack.append(u)

    return visited


def bfs(G: Union[AdjacencyList, AdjacencyMatrix], start_idx):
    Q = [start_idx]
    visited = [start_idx]

    while Q:
        u = Q.pop(0)

        for v in G.neighbours(u):
            if v not in visited:
                Q.append(v)
                visited.append(v)

    return visited


def fill_graph(G: Union[AdjacencyList, AdjacencyMatrix]):
    for x, y, rej in polska.polska:
        G.insertVertex(Vertex(x, y, rej))

    for v1, v2 in polska.graf:
        G.insertEdge(v1, v2)

    return G


def choose_search(G: Union[AdjacencyList, AdjacencyMatrix], start_idx, method: str):
    if method == 'DFS':
        return dfs_iterative(G, start_idx)

    elif method == 'BFS':
        return bfs(G, start_idx)

    else:
        raise ValueError('Zła metoda przeszukiwania')


def paint_graph(G: Union[AdjacencyList, AdjacencyMatrix], sequence):
    color_lst = [-1 for _ in range(G.order())]  # lista kryjąca pod odpowiednim indeksem kolor danego wierzchołka
    key_color_lst = []

    for i in sequence:
        neighbours_colors = [color_lst[j] for j in G.neighbours(i)]

        highest_color = 1
        while highest_color in neighbours_colors:
            highest_color += 1

        color_lst[i] = highest_color
        key_color_lst.append((G.getVertex(i), highest_color))

    return key_color_lst


def test1():
    G = fill_graph(AdjacencyList())  # uzupełnienie grafu wierzchołkami i krawędziami

    search_sequence = choose_search(G, 0, 'DFS')  # przeszukanie grafu odpowiednim algorytmem

    key_color_lst = paint_graph(G, search_sequence)  # uzupełnienie listy kolorów na podstawie przeszukanego grafu

    polska.draw_map(G.edges(), key_color_lst)


def test2():
    G = fill_graph(AdjacencyList())  # uzupełnienie grafu wierzchołkami i krawędziami

    search_sequence = choose_search(G, 0, 'BFS')  # przeszukanie grafu odpowiednim algorytmem

    key_color_lst = paint_graph(G, search_sequence)  # uzupełnienie listy kolorów na podstawie przeszukanego grafu

    polska.draw_map(G.edges(), key_color_lst)


def test3():
    G = fill_graph(AdjacencyMatrix())  # uzupełnienie grafu wierzchołkami i krawędziami

    search_sequence = choose_search(G, 0, 'DFS')  # przeszukanie grafu odpowiednim algorytmem

    key_color_lst = paint_graph(G, search_sequence)  # uzupełnienie listy kolorów na podstawie przeszukanego grafu

    polska.draw_map(G.edges(), key_color_lst)


def test4():
    G = fill_graph(AdjacencyMatrix())  # uzupełnienie grafu wierzchołkami i krawędziami

    search_sequence = choose_search(G, 0, 'BFS')  # przeszukanie grafu odpowiednim algorytmem

    key_color_lst = paint_graph(G, search_sequence)  # uzupełnienie listy kolorów na podstawie przeszukanego grafu

    polska.draw_map(G.edges(), key_color_lst)


if __name__ == "__main__":
    # należy uruchamiać tylko jeden test na raz
    # test1()
    # test2()
    # test3()
    test4()
