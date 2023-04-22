# NIESKOŃCZONE

import cv2
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt


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
    def __init__(self, capacity, isResidual):
        self.capacity = capacity       # pojemność
        self.flow = 0                  # przepływ
        self.isResidual = isResidual   # czy krawędź jest resztowa

        if isResidual:
            self.residual = 0  # przepływ resztowy
        else:
            self.residual = capacity  # przepływ resztowy

    def __repr__(self):
        return f'{self.capacity} {self.flow} {self.residual} {self.isResidual}'


class AdjacencyList:
    def __init__(self):
        self.list = []  # właściwa lista sąsiedztwa
        self.list_edges = []  # pomocnicza lista pokazująca wszystkie krawędzie
        self.vert_idx = {}  # słownik wiążący ze sobą wierzchołek z miejscem w liście sąsiedztwa

    def insertVertex(self, vertex: Vertex):
        # sprawdzenie, czy już istnieje taki wierzchołek
        for v in self.vert_idx:
            if v == vertex:
                self.vert_idx[vertex] = self.vert_idx.pop(v)
                return None

        # w przeciwnym wypadku dodaj nowy wierzchołek
        self.vert_idx[vertex] = len(self.vert_idx)
        # i dodaj go bez żadnych połączeń do listy sąsiedztwa
        self.list.append([])

    def insertEdge(self, v_start, v_end, capacity, isResidual):
        self.list_edges.append((v_start, v_end))

        # w mojej implementacji uznałem, że nie będzie możliwa sytuacja
        # dodania najpierw krawędzi, a później wierzchołków w niej występujących
        idx_v1 = self.vert_idx[v_start]
        idx_v2 = self.vert_idx[v_end]

        self.list[idx_v1].append((idx_v2, Edge(capacity, isResidual)))

    def deleteVertex(self, vertex):
        del_idx = self.vert_idx[vertex]

        for edge in self.list_edges:
            if edge[0] == del_idx and edge[1] == del_idx:
                self.list_edges.remove(edge)
                break

        # aktualizacja słownika
        del (self.vert_idx[vertex])  # usunięcie wierzchołka startowego
        for v, i in self.vert_idx.items():  # dekrementacja
            if i > del_idx:
                self.vert_idx[v] -= 1

        # aktualizacja listy sąsiedztwa
        del(self.list[del_idx])  # usunięcie wierzchołka startowego

        for idx1, v_start_list in enumerate(self.list):  # usunięcie wierzchołków końcowych i dekrementacja
            for idx2, v_end in enumerate(v_start_list):
                if v_end == del_idx:
                    v_start_list.remove(v_end)
                elif v_end > del_idx:
                    self.list[idx1][idx2][0] -= 1

    def deleteEdge(self, vertex1, vertex2):
        idx_v1 = self.vert_idx[vertex1]
        idx_v2 = self.vert_idx[vertex2]

        for edge in self.list_edges:
            if edge[0] == idx_v1 and edge[1] == idx_v2:
                self.list_edges.remove(edge)
                break

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
        for end_idx, edge in self.list[start_idx]:
            neighbour_lst.append((end_idx, edge))

        return neighbour_lst

    def order(self):
        return len(self.list)

    def size(self):
        return len(self.list_edges)

    def edges(self):
        return self.list_edges

    def getColor(self, key):
        for vertex in self.vert_idx.keys():
            if vertex == key:
                return vertex.color

    def setColor(self, key, color):
        for vertex in self.vert_idx.keys():
            if vertex == key:
                vertex.color = color


def bfs(G: AdjacencyList, start_v):
    start_idx = G.getVertexIdx(start_v)

    Q = [start_idx]
    visited = [start_idx]
    parent = [-1 for _ in range(G.order())]  # lista rodziców wierzchołków początkowo ustawiona na -1

    while Q:
        u = Q.pop(0)

        for v, edge in G.neighbours(u):
            if v not in visited and edge.residual > 0:
                Q.append(v)
                visited.append(v)
                parent[v] = u

    return parent


def analysing_path(G: AdjacencyList, idx_end, parent):
    current_v = idx_end
    smallest_capacity = float('inf')

    if parent[current_v] == -1:  # liczba -1 reprezentuje brak rodzica dla current_v
        smallest_capacity = 0
        return smallest_capacity

    while parent[current_v] != -1:  # brak rodzica (-1 w tablicy parent) oznacza wierzchołek początkowy
        for u_idx, edge in G.neighbours(parent[current_v]):
            if u_idx == current_v and not edge.isResidual:  # po znalezieniu odpowiedniego wierzchołka
                if edge.residual < smallest_capacity:       # jeśli jego przepływ jest mniejszy od obecnego
                    smallest_capacity = edge.residual       # uaktualniam najmniejszy przepływ

                current_v = parent[current_v]   # dalsze poszukiwanie w ścieżce od końca do początku
                break

    return smallest_capacity


def path_augmentation(G: AdjacencyList, idx_start, idx_end, parent, smallest_capacity):
    current_v = idx_end

    while True:
        for m_idx, edge in G.neighbours(parent[current_v]):  # uaktualnianie krawędzi rzeczywistych
            if m_idx == current_v and not edge.isResidual:
                edge.flow += smallest_capacity
                edge.residual -= smallest_capacity

        for n_idx, edge in G.neighbours(current_v):          # uaktualnianie krawędzi resztowych
            if n_idx == parent[current_v] and edge.isResidual:
                edge.residual += smallest_capacity

        if current_v == idx_start:
            break

        current_v = parent[current_v]


def FF_Algorithm(G: AdjacencyList, v_start, v_end):
    parent = bfs(G, v_start)

    idx_start = G.getVertexIdx(v_start)
    idx_end = G.getVertexIdx(v_end)
    smallest_capacity = analysing_path(G, idx_end, parent)

    sum_of_capacity = smallest_capacity

    while smallest_capacity > 0:
        path_augmentation(G, idx_start, idx_end, parent, smallest_capacity)
        parent = bfs(G, v_start)
        smallest_capacity = analysing_path(G, idx_end, parent)

        sum_of_capacity += smallest_capacity

    return sum_of_capacity


def min_cut(G: AdjacencyList, start_v, end_v):
    curr_v = G.getVertexIdx(end_v)

    min_cut_G = deepcopy(G)

    parent = bfs(G, start_v)

    if parent[curr_v] == -1:
        raise Exception('Nie ma ścieżki z punktu początkowego do końcowego')

    while parent[curr_v] != -1:
        for ngbr, edge in G.neighbours(curr_v):
            if parent[ngbr] == -1 and not edge.isResidual or edge.capacity == 0:
                min_cut_G.deleteEdge(curr_v, ngbr)

        curr_v = parent[curr_v]


def test():
    I = cv2.imread('min_cut_seg_1.png', cv2.IMREAD_GRAYSCALE)
    YY, XX = I.shape

    scrible_FG = np.zeros((YY, XX), dtype=np.ubyte)
    scrible_FG[100:120, 100:120] = 255

    scrible_BG = np.zeros((YY, XX), dtype=np.ubyte)
    scrible_BG[0:20, 0:20] = 255

    I = cv2.resize(I, (32, 32))
    scrible_BG = cv2.resize(scrible_BG, (32, 32))
    scrible_FG = cv2.resize(scrible_FG, (32, 32))
    YY, XX = I.shape

    hist_FG = cv2.calcHist([I], [0], scrible_FG, [256], [0, 256])
    hist_FG = hist_FG / sum(hist_FG)

    hist_BG = cv2.calcHist([I], [0], scrible_BG, [256], [0, 256])
    hist_BG = hist_BG / sum(hist_BG)

    G = AdjacencyList()
    # G.insertVertex(Vertex('s'))
    # G.insertVertex(Vertex('t'))

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
    for i in range(1, YY - 1):
        for j in range(1, XX - 1):

            middle_v_idx = G.getVertexIdx(vertexes[i][j])
            middle_v_color = int(G.getColor(middle_v_idx))

            # m i n to współrzędne 8 sąsiadów
            for m in range(i - 1, i + 2):
                for n in range(j - 1, j + 2):
                    if m != i or n != j:
                        # print(m, n)
                        neighbour_v_idx = G.getVertexIdx(vertexes[m][n])
                        neighbour_v_color = int(G.getColor(neighbour_v_idx))

                        dist = abs(middle_v_color - neighbour_v_color)
                        weight = np.exp(-0.5 * dist)

                        G.insertEdge(middle_v_idx, neighbour_v_idx, weight, True)

                        # ręczne dodanie dwustronnej krawędzi gdy wierzchołek znajduje się na ramce obrazu
                        if m == 1 or YY - 1 or n == 1 or XX - 1:
                            G.insertEdge(neighbour_v_idx, middle_v_idx, weight, True)

    G.insertVertex(Vertex('s'))
    G.insertVertex(Vertex('t'))

    # połączenie grafu z wierzchołkiem początkowym
    for i in range(YY):
        for j in range(XX):
            G.insertEdge(YY * j + i, 's', 0, False)
            if scrible_FG[i, j]:
                G.insertEdge('s', YY * j + i, float('inf'), False)
            elif scrible_BG[i, j]:
                G.insertEdge('s', YY * j + i, 0, False)
            else:
                G.insertEdge('s', YY * j + i, hist_FG[I[i, j]], False)

    # połączenie grafu z wierzchołkiem końcowym
    for i in range(YY):
        for j in range(XX):
            G.insertEdge('t', YY * j + i, 0, False)
            if scrible_FG[i, j]:
                G.insertEdge(YY * j + i, 't', 0, False)
            elif scrible_BG[i, j]:
                G.insertEdge(YY * j + i, 't', float('inf'), False)
            else:
                G.insertEdge(YY * j + i, 't', hist_FG[I[i, j]], False)

    FF_Algorithm(G, 's', 't')
    min_cut_G = min_cut(G, 's', 't')

    I_seg = np.zeros(shape=I.shape)
    parent_ = bfs(min_cut_G, 0)

    for elem in parent_[:-2]:  # lista parent bez dwóch ostatnich wierzchołków tj. 's' i 't'
        I_seg[elem % YY, elem // YY] = 255

    I_seg[0, 0] = 255

    plt.figure(figsize=(10, 5))
    plt.subplot(121)
    plt.imshow(I, 'gray', vmin=0, vmax=255)
    plt.axis('off')
    plt.title('Obraz oryginalny')

    plt.subplot(122)
    plt.imshow(I_seg, 'gray', vmin=0, vmax=255)
    plt.axis('off')
    plt.title('Segmentacja obrazu - rezultat')
    plt.show()


if __name__ == "__main__":
    test()
