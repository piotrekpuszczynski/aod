from graph import *


class Bigraph:
    #   graph - graph
    #   visited - visited vertices
    #   colors - array of colors for each vertex
    def __init__(self, graph_type, vertices_count):
        self.graph = getGraph(graph_type, vertices_count)
        self.visited = [False] * self.graph.vertices
        self.colors = [""] * self.graph.vertices

    #   executes algorithm
    def execute(self):

        #   checks if graph is bigraph for all unvisited vertices
        for i in range(self.graph.vertices):
            if not self.visited[i]:
                if not self.isBigraph(i):
                    print("graph is not bipartite")
                    return False

        #   prints two vertices collections
        red = []
        blue = []

        for i in range(len(self.colors)):
            if self.colors[i] == "red":
                red.append(i + 1)
            else:
                blue.append(i + 1)

        print(red)
        print(blue)
        return True

    #   check if graph is bigraph by dfs
    #   parameters:
    #       vertex - starting vertex
    def isBigraph(self, vertex):

        prev = [None] * self.graph.vertices

        cur = self.graph.verticesList[vertex]
        self.visited[cur.name] = True

        #   finds starting color
        color = "red"
        for neighbour in cur.neighbours:
            if self.colors[neighbour.name] == "red":
                color = "blue"
            else:
                color = "red"

        self.colors[cur.name] = color

        can_move = True
        while cur.name != vertex or can_move:

            #   change color of neighbours of current vertex
            if not self.colorNeighbours(cur):
                return False

            can_move = False
            for neighbour in cur.neighbours:
                if not self.visited[neighbour.name]:

                    prev[neighbour.name] = cur.name
                    cur = neighbour
                    self.visited[cur.name] = True
                    can_move = True
                    break

            if not can_move:

                if prev[cur.name] is None:
                    continue

                can_move = True

                cur = self.graph.verticesList[prev[cur.name]]

        return True

    #   changes color of neighbours
    #   parameters:
    #       vertex - vertex to change color of it's neighbours
    def colorNeighbours(self, vertex):
        for neighbour in vertex.neighbours:
            if self.colors[neighbour.name] == self.colors[vertex.name]:
                return False
            else:
                if self.colors[vertex.name] == "red":
                    self.colors[neighbour.name] = "blue"
                else:
                    self.colors[neighbour.name] = "red"

        return True
