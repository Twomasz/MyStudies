# SKOŃCZONE

import numpy as np
from copy import deepcopy


class Vertex:
    def __init__(self, key):
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


class AdjacencyMatrix:
    def __init__(self):
        self.matrix = []       # właściwa lista sąsiedztwa
        self.edges_list = []   # pomocnicza lista pokazująca wszystkie krawędzie
        self.vert_idx = {}     # słownik wiążący ze sobą wierzchołek z miejscem w liście sąsiedztwa

    def insertVertex(self, vertex: Vertex):
        # sprawdzenie, czy już istnieje taki wierzchołek
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

    def insertEdge(self, v_start, v_end, weight):
        self.edges_list.append(Edge(v_start, v_end, weight))

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

    def get_matrix(self):
        return np.array(self.matrix)


def fill_matrixes(G, P):
    # uzupełnianie grafu G
    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    vertexes_G = ['A', 'B', 'C', 'D', 'E', 'F']

    for v in vertexes_G:
        G.insertVertex(Vertex(v))

    for v_start, v_end, weight in graph_G:
        G.insertEdge(v_start, v_end, weight)
        G.insertEdge(v_end, v_start, weight)

    # uzupełnianie grafu P
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]
    vertexes_P = ['A', 'B', 'C']

    for v in vertexes_P:
        P.insertVertex(Vertex(v))

    for v_start, v_end, weight in graph_P:
        P.insertEdge(v_start, v_end, weight)
        P.insertEdge(v_end, v_start, weight)


def create_matrix_M0(G: AdjacencyMatrix, P: AdjacencyMatrix):
    x, y = P.order(), G.order()
    M0 = np.zeros((x, y))

    for i in range(x):
        deg_vi = sum(P.get_matrix()[i])
        for j in range(y):
            deg_vj = sum(G.get_matrix()[j])

            if deg_vi <= deg_vj:
                M0[i][j] = 1

    return M0


def Prune(M, G, P):  # G i P to np.array (nie AdjacencyMatrix)
    Vp, Vg = M.shape

    M_is_changed = True
    while M_is_changed:
        M_is_changed = False

        for i in range(Vp):
            for j in range(Vg):
                if M[i][j] == 1:

                    any_counterpart = False

                    for x, vi in enumerate(P[i]):
                        for y, vj in enumerate(G[j]):
                            if M[x, y] == 1:
                                any_counterpart = True
                                break
                            else:
                                continue

                        if any_counterpart:
                            continue
                        else:
                            M[i, j] = 0
                            M_is_changed = True
                            break


def Ullman(used_cols, current_row, G, P, M, no_isomorphism=0, no_recursion=0, version='1.0', M0=None):
    # sprawdzenie wersji algorytmu
    if not (version == '1.0' or version == '2.0' or version == '3.0'):
        raise ValueError('Niepoprawna wersja algorytmu')

    no_recursion += 1  # inkrementacja licznika wywołań rekurencji

    if current_row == M.shape[0]:
        if np.array_equal(P, M @ (M @ G).T):
            no_isomorphism += 1  # inkrementacja licznika znalezionych izomorfizmów
            # print(M, '\n')
            return no_isomorphism, no_recursion

        else:
            return no_isomorphism, no_recursion

    M_copy = deepcopy(M)

    if version == '3.0':  # pruning w wersji 3.0
        Prune(M_copy, G, P)

    for col in range(M.shape[1]):
        if col not in used_cols:
            # sprawdzanie macierzy M0 tylko w wersji 2.0 i 3.0
            if version == '1.0' or ((version == '2.0' or '3.0') and M0[current_row][col] == 1):
                # wyzerowanie wszystkich kolumn w danym wierszu i zaznaczenie 1 w obecnej kolumnie
                M_copy[current_row] = [0 for _ in range(M.shape[1])]
                M_copy[current_row][col] = 1

                used_cols.append(col)  # zamarkowanie obecnej kolumny jako użytej

                figures = Ullman(used_cols, current_row + 1, G, P, M_copy, no_isomorphism, no_recursion, version, M0)
                no_isomorphism, no_recursion = figures

                used_cols.remove(col)  # zamarkowanie obecnej kolumny jako nieużytej

    return no_isomorphism, no_recursion


def test():
    G = AdjacencyMatrix()
    P = AdjacencyMatrix()

    fill_matrixes(G, P)  # uzupełnienie grafów wierzchołkami i krawędziami

    M = np.zeros((P.order(), G.order()))

    results_1 = Ullman([], 0, G.get_matrix(), P.get_matrix(), M, version='1.0')
    print(results_1)

    M0 = create_matrix_M0(G, P)  # stworzenie macierzy M0 dla wersji 2.0 i 3.0

    results_2 = Ullman([], 0, G.get_matrix(), P.get_matrix(), M, version='2.0', M0=M0)
    print(results_2)

    results_3 = Ullman([], 0, G.get_matrix(), P.get_matrix(), M, version='3.0', M0=M0)
    print(results_3)


if __name__ == "__main__":
    test()
