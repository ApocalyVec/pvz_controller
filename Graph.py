# adapted from https://www.bogotobogo.com/python/python_graph_data_structures.php


class Graph:
    def __init__(self):
        self.vertex_dic = {}  # [key: Variable, value: list of Variables as connection]
        self.size = 0

    def __iter__(self):
        return iter(self.vertex_dic.values())  # return a list for iterating through

    def add_vertex(self, vertex):
        self.vertex_dic[vertex] = []  # a vertex is adjacent to itself
        self.size = self.size + 1
        return vertex

    def get_vertex(self, name):

        rtn = None
        for key in self.vertex_dic.keys():
            if key.name == name:
                rtn = key
        return rtn

    def get_connecting_vertices(self, vertex):
        return self.vertex_dic[vertex]

    def add_edge(self, start, end):

        if start not in self.vertex_dic:
            self.add_vertex(start)  # add the starting vertex if it is not in the graph
        if end not in self.vertex_dic:
            self.add_vertex(end)  # add the ending vertex if it is not in the graph

        self.vertex_dic[start].append(end)
        self.vertex_dic[end].append(start)

    def get_all_vertices(self):
        return self.vertex_dic.keys()

    '''
    :return list of list with two vertices
    '''

    def get_edges(self, vertex):
        rtn = []
        for connection in self.vertex_dic[vertex]:
            rtn.append([vertex, connection])
        return rtn

    '''
    :return a list of tuples with two vertices
    '''

    def get_all_edges(self):
        rtn = []
        # existing = {}
        for vertex in self.vertex_dic.keys():
            edges = self.get_edges(vertex)
            for edge in edges:
                # if edge[0] in existing.keys():
                #     if existing[edge[0]] != edge[1]:
                #         continue
                # existing[edge[1]] = edge[0]
                rtn.append(edge)

        return rtn

    def print_all_vertices(self):
        for vertex, connections in self.vertex_dic.items():
            print("Vertex: " + vertex.name + " Connection: ", end="")
            for c in connections:
                print(c.name, end=" ,")
            print()
