#   vertex class
class Vertex:

    #   name - id of vertex
    #   neighbours - array of vertices that can be moved to
    def __init__(self, name):
        self.name = name
        self.neighbours = []

    #   addNeighbour - method that adds vertex to array of neighbours
    #   parameters:
    #       vertex - neighbour of this vertex
    def addNeighbour(self, vertex):

        #   if neighbours array doesn't contain vertex it's added
        if vertex not in self.neighbours:
            self.neighbours.append(vertex)


#   graph class
class Graph:

    #   vertices - number of vertices
    #   edges - number of edges
    #   verticesList - array of vertices
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = 0
        self.verticesList = []

        #   creates instances of vertices in loop
        for i in range(vertices):
            self.verticesList.append(Vertex(i))

    #   addEdge - adds edge to graph
    #   parameters:
    #       source - index of source vertex in verticesList
    def addEdge(self, source, destination):
        return None

    #   print - prints whole graph (one line is vertex id and array of vertices that can be moved to)
    def print(self):
        #   loop at all vertices in verticesList
        for vertex in self.verticesList:
            neighbours = []

            #   loop at all vertices in neighbours of actual vertex
            for neighbour in vertex.neighbours:
                neighbours.append(neighbour.name + 1)

            #   prints line - vertex and array of neighbours of this vertex
            print(str(vertex.name + 1) + " -> " + str(neighbours))


#   graph class extension to directed graph
class DirectedGraph(Graph):

    #   addEdge - adds vertex on destination index of verticesList
    #   to list of neighbours of vertex on source index of verticesList
    #   and increases number of edges
    def addEdge(self, source, destination):
        if self.verticesList[destination] not in self.verticesList[source].neighbours:
            self.verticesList[source].addNeighbour(self.verticesList[destination])
            self.edges = self.edges + 1


#   graph class extension to undirected graph
class UndirectedGraph(Graph):

    #   addEdge - adds vertex on destination index of verticesList
    #   to list of neighbours of vertex on source index of verticesList and vice versa
    #   and increases number of edges
    def addEdge(self, source, destination):
        if self.verticesList[destination] not in self.verticesList[source].neighbours:
            self.verticesList[source].addNeighbour(self.verticesList[destination])
            self.verticesList[destination].addNeighbour(self.verticesList[source])
            self.edges = self.edges + 1


#   function which creates graph from file with data
#   graph_type - type of graph (D - directed, U - undirected)
#   transpose - is graph transposed
def getGraph(graph_type, vertices_count, transpose=False):

    try:
        #   file - opens file from given parameters
        file = open(graph_type + vertices_count + ".txt", "r")

        #   lines - array of all lines in file
        lines = file.readlines()

        #   T - type of graph from file
        #   vertices - number of vertices from file
        #   edges - number of edges from file
        T = str(lines[0])
        vertices = int(lines[1])
        # edges = int(lines[2])

        #   checks  if graph is directed or not
        if T == "U\n":
            graph = UndirectedGraph(vertices)
        else:
            graph = DirectedGraph(vertices)

        #   loop at all edges from file
        for i in range(3, len(lines)):

            #   if graph isn't transposed adds normal edge, otherwise adds inverted edge
            if transpose:
                graph.addEdge(int(lines[i].split()[1]) - 1, int(lines[i].split()[0]) - 1)
            else:
                graph.addEdge(int(lines[i].split()[0]) - 1, int(lines[i].split()[1]) - 1)

        #   returns graph created from file
        return graph

    #   throws exception if file of given parameters doesn't exist
    except FileNotFoundError:
        print("invalid parameters")
