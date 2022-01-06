from graph import *


#   class which sorts topologically vertices of graph and detects if graph contains cycle
class Sort:

    #   creates directed graph with specified number of vertices
    def __init__(self, vertices_count):
        self.graph = getGraph("D", vertices_count)

    #   does main goal of class
    def execute(self):

        #   degrees - array of degrees of each vertex
        #   result - array for topologically sorted vertices
        degrees = [0] * self.graph.vertices
        result = []

        #   loop calculates degrees for vertices
        for vertex in self.graph.verticesList:
            for neighbour in vertex.neighbours:
                degrees[neighbour.name] = degrees[neighbour.name] + 1

        #   loop sorts vertices topologically until result array contains all vertices
        while len(result) < self.graph.vertices:

            cycle = True

            #   loop at all vertices
            for i in range(len(degrees)):

                #   if any vertex has degree equal 0 which is not already in result array changes
                #   cycle flag to False, adds it to result array and decrease degree of all neighbours of this vertex
                if degrees[i] == 0 and i + 1 not in result:

                    cycle = False
                    result.append(i + 1)

                    for neighbour in self.graph.verticesList[i].neighbours:
                        degrees[neighbour.name] = degrees[neighbour.name] - 1

                    break

            #   if any degree of vertex is not equal 0 it imply that in graph is cycle
            #   so it prints that there is cycle and exit loop
            if cycle:
                print("graph contains cycle")
                break

        #   prints all vertices that can be sorted topologically
        print(str(result))
