# NIESKOŃCZONE

import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from math import degrees


class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f'{self.x}, {self.y}'


class Edge:
    def __init__(self, length, theta):
        self.length = length       # długość krawędzi
        self.theta = theta         # orientacja krawędzi

    def __repr__(self):
        return f'{self.length}, {self.theta}'


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

    def insertEdge(self, v_start, v_end):
        self.list_edges.append((v_start, v_end))

        # w mojej implementacji uznałem, że nie będzie możliwa sytuacja
        # dodania najpierw krawędzi, a później wierzchołków w niej występujących
        idx_v1 = self.vert_idx[v_start]
        idx_v2 = self.vert_idx[v_end]

        length = np.sqrt((v_end[0] - v_start[0]) ** 2 + (v_end[1] - v_start[1]) ** 2)
        theta = np.arctan2((v_end[1] - v_start[1]), (v_end[0] - v_start[0]))

        self.list[idx_v1].append((idx_v2, Edge(length, theta)))

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


class BiometricGraph(AdjacencyList):
    def printGraph(self):
        for i in range(len(self.list)):
            vertex1 = self.getVertex(i)
            plt.scatter(vertex1.x, vertex1.y, c='#1f77b4')

            for v_and_edge in self.list[i]:
                vertex2 = self.getVertex(v_and_edge[0])

                x_line = np.linspace(vertex1.x, vertex2.x, 20)
                y_line = np.linspace(vertex1.y, vertex2.y, 20)

                plt.plot(x_line, y_line, 'r')

    def translate_and_rotate(self, trans_vector, rotate_angle):
        # rotate
        graph1 = BiometricGraph()
        for vertex in self.list.keys():
            vertx = vertex.x * np.cos(rotate_angle) + vertex.y * np.sin(rotate_angle) + trans_vector[0]
            verty = -vertex.x * np.sin(rotate_angle) + vertex.y * np.cos(rotate_angle) + trans_vector[1]
            graph1.insertVertex(Vertex(int(vertx), int(verty)))
            for edge in self.list[vertex]:
                edgex = edge.vertex.x * np.cos(rotate_angle) + edge.vertex.y * np.sin(rotate_angle) + trans_vector[0]
                edgey = -edge.vertex.x * np.sin(rotate_angle) + edge.vertex.y * np.cos(rotate_angle) + trans_vector[1]
                graph1.insertEdge((int(vertx), int(verty)), (int(edgex), int(edgey)))
                graph1.insertEdge((int(edgex), int(edgey)), (int(vertx), int(verty)))

        return graph1


def fill_biometric_graph_from_image(img_bin, G: BiometricGraph):
    size = img_bin.shape

    for y in range(1, size[0]):
        for x in range(1, size[1] - 1):
            if img_bin[y, x] == 255:
                G.insertVertex(Vertex(x, y))

                if img_bin[y-1, x-1] == 255:
                    G.insertEdge((x, y), (x-1, y-1))
                    G.insertEdge((x-1, y-1), (x, y))

                if img_bin[y-1, x] == 255:
                    G.insertEdge((x, y), (x-1, y))
                    G.insertEdge((x-1, y), (x, y))

                if img_bin[y-1, x+1] == 255:
                    G.insertEdge((x, y), (x-1, y+1))
                    G.insertEdge((x-1, y+1), (x, y))

                if img_bin[y, x-1] == 255:
                    G.insertEdge((x, y), (x, y-1))
                    G.insertEdge((x, y-1), (x, y))


def unclutter_biometric_graph(graph):
    to_delete = set()
    to_add = set()

    for vertex in graph.list.keys():
        if len(graph.list[vertex]) != 2:
            for edge in graph.list[vertex]:
                curr_edge_list = graph.list[edge.vertex]
                curr_vertex = edge.vertex
                prev_vertex = vertex
                while len(curr_edge_list) == 2:
                    to_delete.add(curr_vertex)
                    if curr_edge_list[1].vertex == prev_vertex:
                        prev_vertex = curr_vertex
                        curr_vertex = curr_edge_list[0].vertex
                    else:
                        prev_vertex = curr_vertex
                        curr_vertex = curr_edge_list[1].vertex
                    curr_edge_list = graph.list[curr_vertex]

                # jeśli while się skończył to znaleźliśmy pkt charakterystyczny
                to_add.add((vertex, curr_vertex))

    # usuwanie i dodawanie
    for vertex in to_delete:
        graph.deleteVertex(vertex.x, vertex.y)
    for edge in to_add:
        if edge[0].x != edge[1].x or edge[0].y != edge[1].y:
            graph.insertEdge(edge[0].x, edge[0].y, edge[1].x, edge[1].y)


def merge_near_vertices(G, thr):
    to_merge = []
    for vertex in G.list.keys():
        inside_merge = []
        is_vertex_present = any(vertex in sublist for sublist in to_merge)
        if not is_vertex_present:
            inside_merge.append(vertex)
            for other_vert in G.keys_without_vertex(vertex):
                is_other_vert_present = any(other_vert in sublist for sublist in to_merge)
                if not is_other_vert_present and np.sqrt(
                        (other_vert.x - vertex.x) ** 2 + (other_vert.y - vertex.y) ** 2) <= thr:
                    inside_merge.append(other_vert)
            if len(inside_merge) > 1:
                to_merge.append(inside_merge)
        else:
            continue

    for inside_list in to_merge:
        # średnia
        meanx = int(sum(vert.x for vert in inside_list) / len(inside_list))
        meany = int(sum(vert.y for vert in inside_list) / len(inside_list))

        # destynacja
        destinations = []
        for vertex in inside_list:
            for edge in G.list[vertex]:
                if edge.vertex not in inside_list:
                    destinations.append(edge.vertex)

        # usuwanko
        for vertex in inside_list:
            G.deleteVertex(vertex.x, vertex.y)
        G.insertVertex(meanx, meany)
        for vertex in destinations:
            if meanx != vertex.x or meany != vertex.y:
                G.insertEdge(meanx, meany, vertex.x, vertex.y)
                G.insertEdge(vertex.x, vertex.y, meanx, meany)


def biometric_graph_registration(G1, G2, Ni, eps):
    S_ab = []
    edges1 = G1.edges()
    edges2 = G2.edges()
    for edge1 in edges1:
        for edge2 in edges2:
            whatev = (1 / (0.5 * (edge1[1].l + edge2[1].l))) * np.sqrt(
                ((edge1[1].l - edge2[1].l) ** 2) + (degrees(edge1[1].theta) - degrees(edge2[1].theta)) ** 2)
            S_ab.append([whatev, edge1, edge2])

    # sortowanie i wybranie 50 najmniejszych
    S_ab = sorted(S_ab, key=lambda x: x[0])
    S_ab = S_ab[:Ni]
    d = float('inf')
    min_pair = []
    for pair in S_ab:
        # graf uno
        edge1 = pair[1]
        angle = np.arccos((edge1[1].vertex.x - edge1[0].x) / edge1[1].l)
        graph1 = G1.translate_and_rotate((-edge1[0].x, -edge1[0].y), 0)
        graph1 = graph1.translate_and_rotate((0, 0), angle)

        # graf dos
        edge2 = pair[2]
        angle = np.arccos((edge2[1].vertex.x - edge2[0].x) / edge2[1].l)
        graph2 = G2.translate_and_rotate((-edge2[0].x, -edge2[0].y), 0)
        graph2 = graph2.translate_and_rotate((0, 0), angle)

        C = 0
        for vertex1 in graph1.list.keys():
            for vertex2 in graph2.list.keys():
                if np.sqrt((vertex2.x - vertex1.x) ** 2 + (vertex2.y - vertex1.y) ** 2) < eps:
                    C += 1
                    break

        d1 = 1 - C / np.sqrt(graph1.order() * graph2.order())
        if d1 < d:
            d = d1
            min_pair = (graph1, graph2)

    return min_pair


def main():
    data_path = "C:/Programowanie/ASD/Lab11"
    img_level = "easy"
    img_list = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]

    input_data = []
    for img_name in img_list:
        if img_name[-3:] == "png":
            if img_name.split('_')[-2] == img_level:
                print("Processing ", img_name, "...")

                img = cv2.imread(os.path.join(data_path, img_name))
                img_1ch = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, img_bin = cv2.threshold(img_1ch, 127, 255, cv2.THRESH_BINARY)

                graph = BiometricGraph()
                fill_biometric_graph_from_image(img_bin, graph)
                unclutter_biometric_graph(graph)
                merge_near_vertices(graph, thr=5)

                input_data.append((img_name, graph))
                print("Saved!")

    for i in range(len(input_data)):
        for j in range(len(input_data)):
            graph1_input = input_data[i][1]
            graph2_input = input_data[j][1]

            graph1, graph2 = biometric_graph_registration(graph1_input, graph2_input, Ni=50, eps=10)

            plt.figure()
            graph1.plot_graph(v_color='red', e_color='green')

            graph2.plot_graph(v_color='gold', e_color='blue')
            plt.title('Graph comparison')
            plt.show()


if __name__ == "__main__":
    # main()

    bio = BiometricGraph()

    # bio.insertVertex(Vertex(1, 2))
    # bio.insertVertex(Vertex(3, 6))
    # bio.insertVertex(Vertex(0, 4))
    # bio.insertVertex(Vertex(5, 2))
    #
    # bio.insertEdge((1, 2), (0, 4), 1, 0)
    # bio.insertEdge((5, 2), (3, 6), 1, 0)
    #
    # bio.printGraph()
