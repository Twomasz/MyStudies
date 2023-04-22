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
    def __init__(self, vertex1, vertex2, weight=0):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.weight = weight

    def __str__(self):
        return f'({self.vertex1}--{self.weight}-->{self.vertex2})'


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
        self.edges_list.append(Edge(v_start, v_end, weight))

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
        # lst = []
        # for edge in self.edges_list:
        #     lst.append((edge.vertex1, edge.vertex2))
        # return lst
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

    print(parent)
    return MST


def printGraph(G: AdjacencyList):
    n = G.order()
    print("------GRAPH------", n)
    for i in range(n):
        v = G.getVertex(i)
        print(v, end=" -> ")
        nbrs = G.neighbours(i)
        for (j, w) in nbrs:
            print(G.getVertex(j), w, end="; ")
        print()
    print("-------------------")


def test():

    graf = [('A', 'B', 4), ('A', 'C', 1), ('A', 'D', 4),
            ('B', 'E', 9), ('B', 'F', 9), ('B', 'G', 7), ('B', 'C', 5),
            ('C', 'G', 9), ('C', 'D', 3),
            ('D', 'G', 10), ('D', 'J', 18),
            ('E', 'I', 6), ('E', 'H', 4), ('E', 'F', 2),
            ('F', 'H', 2), ('F', 'G', 8),
            ('G', 'H', 9), ('G', 'J', 8),
            ('H', 'I', 3), ('H', 'J', 9),
            ('I', 'J', 9)]

    vertexes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    G = AdjacencyList()
    for v in vertexes:
        G.insertVertex(Vertex(v))

    for v1, v2, w in graf:
        G.insertEdge(v1, v2, w)
        G.insertEdge(v2, v1, w)

    MST = Prime(G, 0)
    printGraph(MST)


if __name__ == "__main__":
    test()
