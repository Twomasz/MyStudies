# SKOŃCZONE

import polska
from typing import Union


class Vertex:
    def __init__(self, x=0, y=0, key=0):
        self.x = x
        self.y = y
        self.key = key

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
        return f'({self.vertex1}, {self.vertex2})'


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

    def insertEdge(self, v_start, v_end, edge=None):
        self.edges_list.append(Edge(v_start, v_end))

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
        for v, i in self.vert_idx.items():  #
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

    def neighbours(self, vertex_idx):
        return self.list[vertex_idx]

    def order(self):
        return len(self.list)

    def size(self):
        return len(self.edges_list)

    def edges(self):
        lst = []
        for edge in self.edges_list:
            lst.append((edge.vertex1, edge.vertex2))
        return lst


class AdjacencyMatrix:
    def __init__(self):
        self.matrix = []      # właściwa lista sąsiedztwa
        self.edges_list = []  # pomocnicza lista pokazująca wszystkie krawędzie
        self.vert_idx = {}    # słownik wiążący ze sobą wierzchołek z miejscem w liście sąsiedztwa

    def insertVertex(self, vertex: Vertex):
        # sprawdzenie czy już istnieje taki wierzchołek
        for v in self.vert_idx:
            if v == vertex:
                self.vert_idx[vertex] = self.vert_idx.pop(v)
                return None

        # w przeciwnym wypadku dodaj nowy wierzchołek
        size = len(self.vert_idx)
        self.vert_idx[vertex] = size

        # i dodaj go bez żadnych połączeń do macierzy sąsiedztwa
        for row in self.matrix:
            row.extend([0 for _ in range(size - len(row) + 1)])
        self.matrix.append([0 for _ in range(size + 1)])

    def insertEdge(self, v_start, v_end):
        self.edges_list.append(Edge(v_start, v_end))

        # w mojej implementacji uznałem, że nie będzie możliwa sytuacja
        # dodania najpierw krawędzi, a później wierzchołków w niej występujących
        idx_v1 = self.vert_idx[v_start]
        idx_v2 = self.vert_idx[v_end]

        # uzupełnienie macierzy sąsiedztwa
        self.matrix[idx_v1][idx_v2] += 1

    def deleteVertex(self, vertex):
        # usuwam wszystkie krawędzie związane z danym wierzchołkiem
        # aby przejść po całej liście i nie przeskakiwać między elementami
        # podczas usuwania i-tego elementu startuję od końca listy
        for i in range(len(self.edges_list) - 1, -1, -1):
            if self.edges_list[i].vertex1 == vertex or self.edges_list[i].vertex2 == vertex:
                del (self.edges_list[i])

        del_idx = self.vert_idx[vertex]

        # aktualizacja słownika
        del(self.vert_idx[vertex])  # usunięcie wierzchołka startowego
        for v, i in self.vert_idx.items():  #
            if i > del_idx:
                self.vert_idx[v] -= 1

        # aktualizacja listy sąsiedztwa
        del(self.matrix[del_idx])  # usunięcie wiersza z danym wierzchołkiem
        for row in self.matrix:      # usunięcie kolumny z danym wierzchołkiem
            del(row[del_idx])

    def deleteEdge(self, vertex1, vertex2):
        # usuwanie z listy krawędzi
        for edge in self.edges_list:
            if edge.vertex1 == vertex1 and edge.vertex2 == vertex2:
                self.edges_list.remove(edge)
                break

        idx_v1 = self.vert_idx[vertex1]
        idx_v2 = self.vert_idx[vertex2]

        self.matrix[idx_v1][idx_v2] -= 1

    def getVertexIdx(self, vertex):
        return self.vert_idx[vertex]

    def getVertex(self, vertex_idx):
        for v, idx in self.vert_idx.items():
            if idx == vertex_idx:
                return v

        return None

    def neighbours(self, vertex_idx):
        neighbours_list = []
        for i, val in enumerate(self.matrix[vertex_idx]):
            for k in range(val):
                neighbours_list.append(i)

        return neighbours_list

    def order(self):
        return len(self.matrix)

    def size(self):
        return len(self.edges_list)

    def edges(self):
        lst = []
        for edge in self.edges_list:
            lst.append((edge.vertex1, edge.vertex2))
        return lst


def test(G: Union[AdjacencyList, AdjacencyMatrix]):

    for x, y, rej in polska.polska:
        G.insertVertex(Vertex(x, y, rej))

    for v1, v2 in polska.graf:
        G.insertEdge(v1, v2)

    G.deleteVertex('K')
    G.deleteEdge('E', 'W')
    G.deleteEdge('W', 'E')

    polska.draw_map(G.edges())


if __name__ == "__main__":
    # należy uruchamiać tylko jeden test na raz
    test(AdjacencyList())
    # test(AdjacencyMatrix())
