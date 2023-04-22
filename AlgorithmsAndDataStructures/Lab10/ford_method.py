# SKOŃCZONE

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

    else:
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


def printGraph(G: AdjacencyList):
    n = G.order()
    print("------GRAPH------", n)
    for i in range(n):
        v = G.getVertex(i)
        print(v, end=" -> ")
        nbrs = G.neighbours(i)
        for (j, edge) in nbrs:
            print(G.getVertex(j), edge, end="; ")
        print()
    print("-------------------")


def test1():
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]

    vertexes = ['s', 'u', 'v', 't']

    G1 = AdjacencyList()
    for v in vertexes:
        G1.insertVertex(Vertex(v))

    for v1, v2, w in graf_0:
        G1.insertEdge(v1, v2, w, False)
        G1.insertEdge(v2, v1, w, True)

    result = FF_Algorithm(G1, 's', 't')
    print('Znaleziony przepływ: ', result)
    printGraph(G1)


def test2():
    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12),
              ('b', 'c', 9), ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]

    vertexes = ['s', 'a', 'b', 'c', 'd', 't']

    G2 = AdjacencyList()
    for v in vertexes:
        G2.insertVertex(Vertex(v))

    for v1, v2, w in graf_1:
        G2.insertEdge(v1, v2, w, False)
        G2.insertEdge(v2, v1, w, True)

    result = FF_Algorithm(G2, 's', 't')
    print('Znaleziony przepływ: ', result)
    printGraph(G2)


def test3():
    graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1),
              ('b', 'd', 2), ('c', 'e', 6), ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]

    vertexes = ['s', 'a', 'b', 'c', 'd', 'e', 't']

    G3 = AdjacencyList()
    for v in vertexes:
        G3.insertVertex(Vertex(v))

    for v1, v2, w in graf_2:
        G3.insertEdge(v1, v2, w, False)
        G3.insertEdge(v2, v1, w, True)

    result = FF_Algorithm(G3, 's', 't')
    print('Znaleziony przepływ: ', result)
    printGraph(G3)


def test4():
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7),
              ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7), ('d', 'c', 4)]

    vertexes = ['s', 'a', 'b', 'c', 'd', 't']

    G4 = AdjacencyList()
    for v in vertexes:
        G4.insertVertex(Vertex(v))

    for v1, v2, w in graf_3:
        G4.insertEdge(v1, v2, w, False)
        G4.insertEdge(v2, v1, w, True)

    result = FF_Algorithm(G4, 's', 't')
    print('Znaleziony przepływ: ', result)
    printGraph(G4)


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
