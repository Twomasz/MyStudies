# SKOŃCZONE

"""
    KOMENTARZ: algorytm nie jest zoptymalizowany obliczeniowo, stąd proszę o wyrozumiałość
               (u mnie na komputerze na wyniki trzeba poczekać około minuty)
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np


class Vertex:
    def __init__(self, key, color=0):
        self.key = key
        self.color = color

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return f'{self.key}'


class Edge:
    def __init__(self, vertex1, vertex2, weight=0):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.weight = weight

    def __str__(self):
        return f'({self.vertex1}--{self.weight}-->{self.vertex2})'

    def __gt__(self, other):
        return self.weight > other.weight

    def __eq__(self, other):
        return self.vertex1 == other.vertex1 and self.vertex2 == other.vertex2 and self.weight == other.weight


class AdjacencyList:
    def __init__(self):
        self.list = []         # właściwa lista sąsiedztwa
        self.edges_list = []   # pomocnicza lista pokazująca wszystkie krawędzie
        self.vert_idx = {}     # słownik wiążący ze sobą wierzchołek z miejscem w liście sąsiedztwa

    def insertVertex(self, vertex: Vertex):
        # sprawdzenie czy już istnieje taki wierzchołek
        for v in self.vert_idx:
            if v == vertex:
                self.vert_idx[vertex] = self.vert_idx.pop(v)
                return None

        # w przeciwnym wypadku dodaj nowy wierzchołek
        self.vert_idx[vertex] = len(self.vert_idx)
        # i dodaj go bez żadnych połączeń do listy sąsiedztwa
        self.list.append([])

    def insertEdge(self, v_start, v_end, weight):
        edge = Edge(v_start, v_end, weight)
        if edge not in self.edges_list:
            self.edges_list.append(edge)

        # w mojej implementacji uznałem, że nie będzie możliwa sytuacja
        # dodania najpierw krawędzi, a później wierzchołków w niej występujących
        idx_v1 = self.vert_idx[v_start]
        idx_v2 = self.vert_idx[v_end]

        self.list[idx_v1].append(idx_v2)

    def deleteVertex(self, vertex):
        # usuwam wszystkie krawędzie związane z danym wierzchołkiem
        # aby przejść po całej liście i nie przeskakiwać między elementami
        # podczas usuwania i-tego elementu startuję od końca listy
        for i in range(len(self.edges_list)-1, -1, -1):
            if self.edges_list[i].vertex1 == vertex or self.edges_list[i].vertex2 == vertex:
                del(self.edges_list[i])

        del_idx = self.vert_idx[vertex]

        # aktualizacja słownika
        del(self.vert_idx[vertex])  # usunięcie wierzchołka startowego
        for v, i in self.vert_idx.items():
            if i > del_idx:
                self.vert_idx[v] -= 1

        # aktualizacja listy sąsiedztwa
        del(self.list[del_idx])  # usunięcie wierzchołka startowego

        for idx1, v_start_list in enumerate(self.list):  # usunięcie w. końcowych i dekrementacja
            for idx2, v_end in enumerate(v_start_list):
                if v_end == del_idx:
                    v_start_list.remove(v_end)
                elif v_end > del_idx:
                    self.list[idx1][idx2] -= 1

    def deleteEdge(self, vertex1, vertex2):
        for edge in self.edges_list:
            if edge.vertex1 == vertex1 and edge.vertex2 == vertex2:
                self.edges_list.remove(edge)
                break

        idx_v1 = self.vert_idx[vertex1]
        idx_v2 = self.vert_idx[vertex2]

        self.list[idx_v1].remove(idx_v2)

    def getVertexIdx(self, vertex):
        return self.vert_idx[vertex]

    def getVertex(self, vertex_idx):
        for v, idx in self.vert_idx.items():
            if idx == vertex_idx:
                return v

        return None

    def neighbours(self, start_idx):
        neighbour_lst = []
        for end_idx in self.list[start_idx]:

            weight = None
            for edge in self.edges_list:
                v1, v2 = edge.vertex1, edge.vertex2
                idx1, idx2 = self.getVertexIdx(v1), self.getVertexIdx(v2)

                if idx1 == start_idx and idx2 == end_idx:
                    weight = edge.weight
                    break

            neighbour_lst.append((end_idx, weight))

        return neighbour_lst

    def order(self):
        return len(self.list)

    def size(self):
        return len(self.edges_list)

    def edges(self):
        return self.edges_list

    def getColor(self, key):
        for vertex in self.vert_idx.keys():
            if vertex == key:
                return vertex.color

    def setColor(self, key, color):
        for vertex in self.vert_idx.keys():
            if vertex == key:
                vertex.color = color


def Prime(G: AdjacencyList, v_start):
    n = G.order()  # liczba wierzchołków grafu
    intree = [False for _ in range(n)]    # czy jest w grafie
    distance = [float('inf') for _ in range(n)]   # minimalna waga krawędzi dla danego wierzchołka
    parent = [-1 for _ in range(n)]   # rodzic wierzchołka

    MST = AdjacencyList()   # graf reprezentujący minimal spanning tree
    idx = 0
    while G.getVertex(idx):   # dodanie wszystkich wierzchołków z G do MST (bez krawędzi)
        MST.insertVertex(G.getVertex(idx))
        idx += 1

    v = v_start

    while not intree[v]:
        intree[v] = True

        for nbrs_idx, weight in G.neighbours(v):
            if distance[nbrs_idx] > weight and intree[nbrs_idx] is False:
                distance[nbrs_idx] = weight
                parent[nbrs_idx] = v

        v = 1
        dist = float('inf')
        for i in range(G.order()):
            if intree[i] is False and dist > distance[i]:
                dist = distance[i]
                v = i

    # uzupełnienie MST na podstawie listy rodziców oraz minimalnego dystansu
    for idx_c, idx_p in enumerate(parent):
        if idx_p != -1:
            v_child = G.getVertex(idx_c)    # pobranie wierzchołka dziecka
            v_parent = G.getVertex(idx_p)   # pobranie wierzchołka rodzica
            weight = distance[idx_c]        # pobranie wagi danej krawędzi
            MST.insertEdge(v_child, v_parent, weight)
            MST.insertEdge(v_parent, v_child, weight)  # uzupełnienie aby krawędź była dwustronna

    return MST


def bfs(G: AdjacencyList, start_v):
    start_idx = G.getVertexIdx(start_v)

    Q = [start_idx]
    visited = [start_idx]

    while Q:
        u = Q.pop(0)

        for v, edge in G.neighbours(u):
            if v not in visited:
                Q.append(v)
                visited.append(v)

    return visited


def test():
    G = AdjacencyList()

    I = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)

    YY, XX = I.shape
    vertexes = [[None for _ in range(XX)] for _ in range(YY)]

    get_coords_from_idx = dict()

    # dodawanie wierzchołków
    for i in range(YY):
        for j in range(XX):
            v = Vertex((YY * j + i), I[i, j])
            G.insertVertex(v)
            vertexes[i][j] = v
            get_coords_from_idx[G.getVertexIdx(v)] = (i, j)

    # dodawanie krawędzi
    for i in range(1, YY-1):
        for j in range(1, XX-1):

            middle_v_idx = G.getVertexIdx(vertexes[i][j])
            middle_v_color = int(G.getColor(middle_v_idx))

            # m i n to współrzędne 8 sąsiadów
            for m in range(i - 1, i + 2):
                for n in range(j - 1, j + 2):
                    if m != i or n != j:
                        neighbour_v_idx = G.getVertexIdx(vertexes[m][n])
                        neighbour_v_color = int(G.getColor(neighbour_v_idx))
                        G.insertEdge(middle_v_idx, neighbour_v_idx, np.abs(middle_v_color - neighbour_v_color))

                        # ręczne dodanie dwustronnej krawędzi gdy wierzchołek znajduje się na ramce obrazu
                        if m == 1 or YY-1 or n == 1 or XX-1:
                            G.insertEdge(neighbour_v_idx, middle_v_idx, np.abs(middle_v_color - neighbour_v_color))

    MST = Prime(G, 0)  # minimal spanning tree

    # wyznaczenie krawędzi o maksymalnej wadze
    max_edge = MST.edges()[0]
    for edge in MST.edges():
        if edge > max_edge:
            max_edge = edge

    v1, v2 = max_edge.vertex1, max_edge.vertex2

    # dwustronne usunięcie rzeczonej krawędzi
    MST.deleteEdge(v1, v2)
    MST.deleteEdge(v2, v1)

    IS = np.zeros((32, 32), dtype='uint8')

    gray_lvl_1 = 100   # zdefiniowany kolor 1
    gray_lvl_2 = 200   # zdefiniowany kolor 2

    for idx in bfs(MST, v1):  # zaznaczenie kolorem 1 wierzchołków wyszukanych pierwszym BFSem
        x, y = get_coords_from_idx[idx]
        IS[x, y] = gray_lvl_1

    for idx in bfs(MST, v2):  # zaznaczenie kolorem 2 wierzchołków wyszukanych drugim BFSem
        x, y = get_coords_from_idx[idx]
        IS[x, y] = gray_lvl_2

    plt.imshow(IS, 'gray', vmin=0, vmax=255)
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    test()
