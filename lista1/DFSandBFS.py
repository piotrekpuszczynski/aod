from graph import *


#   class to extend by DFS and BFS
class Search:

    #   graph - graph created by parameters
    #   visited - array with data if vertex has been visited
    #   result - array of steps visiting vertices
    #   unreachable - array of unreachable vertices by search
    def __init__(self, graph_type, vertices_count):
        self.graph = getGraph(graph_type, vertices_count)
        self.visited = [False] * self.graph.vertices
        self.result = []
        self.unreachable = []

    #   method which execute search
    #   parameters:
    #       vertex - vertex which from search starts
    #       return_tree - is method return tree
    def execute(self, vertex, return_tree):
        pass

    #   method prints result and unreachable vertices
    def print(self):

        #   loop that fills array of unreachable vertices by data from array of visited vertices set to False
        for v in range(len(self.visited)):
            if not self.visited[v]:
                self.unreachable.append(v + 1)

        print(self.result, self.unreachable)


#   search class extension to DFS
class DFS(Search):

    def execute(self, vertex, return_tree):

        #   array of previous vertex for vertex of each index
        prev = [None] * self.graph.vertices

        #   sets current vertex to vertex given in parameters of method, adds to result array
        #   and sets in array of visited vertices to True on index of this vertex
        cur = self.graph.verticesList[vertex - 1]
        self.result.append(cur.name + 1)
        self.visited[cur.name] = True

        #   creates instance of tree to return this in case of return_tree flag is true
        tree = DirectedGraph(self.graph.vertices)

        #   flag can_move depends on ability of moving from current vertex to next unvisited vertex
        can_move = True

        #   while lasts until current vertex is starting vertex and can_move flag is set to False
        while cur.name != vertex - 1 or can_move:

            #   sets can_move flag to false and loop at all neighbours of current vertex
            can_move = False
            for neighbour in cur.neighbours:

                #   if neighbour isn't visited it's added to tree, previous vertex of neighbour is set to current,
                #   neighbour becomes current vertex, new current vertex is added to result array,
                #   vertex is set to visited and because it moved to other vertex flag can_move is set to True
                if not self.visited[neighbour.name]:

                    tree.addEdge(cur.name, neighbour.name)

                    prev[neighbour.name] = cur.name
                    cur = neighbour
                    self.result.append(cur.name + 1)
                    self.visited[cur.name] = True
                    can_move = True
                    break

            #   if from current vertex cannot move to other it has to go back to previous vertex of current vertex
            if not can_move:

                #   it's necessary in case if dfs has only one vertex
                if prev[cur.name] is None:
                    continue

                can_move = True

                #   sets current vertex to previous and adds it to result
                cur = self.graph.verticesList[prev[cur.name]]
                self.result.append(-(cur.name + 1))

        #   prints results of algorithm
        self.print()

        # returns tree created earlier if it's set
        if return_tree:
            return tree


#   FIFO queue class
class FIFO:

    #   queue - data inserted to queue
    def __init__(self):
        self.queue = []

    #   inserts value to queue
    def insert(self, value):
        self.queue.append(value)

    #   delete value of index 0 and returns it
    def pop(self):

        #   if queue is empty returns None
        if len(self.queue) == 0:
            return None

        return self.queue.pop(0)


#   search class extension to BFS
class BFS(Search):

    def execute(self, vertex, return_tree):

        #   creates fifo queue instance and inserts starting vertex
        fifo = FIFO()
        fifo.insert(self.graph.verticesList[vertex - 1])

        #   sets current vertex to starting vertex and sets it's visited flag to True
        cur = fifo.pop()
        self.visited[cur.name] = True

        #   creates instance of tree to return this in case of return_tree flag is true
        tree = DirectedGraph(self.graph.vertices)

        #   loop until fifo queue is empty
        while cur is not None:

            #   adds vertex to result
            self.result.append(cur.name + 1)

            #   loop at all neighbours of current vertx
            for v in cur.neighbours:

                #   if vertex isn't visited adds it to tree, inserts it to queue and sets visited flag to True
                if not self.visited[v.name]:
                    tree.addEdge(cur.name, v.name)
                    fifo.insert(v)
                    self.visited[v.name] = True

            #   sets current vertex to this got from queue
            cur = fifo.pop()

        #   prints results of algorithm
        self.print()

        # returns tree created earlier if it's set
        if return_tree:
            return tree
