from graph import *


#   class which finds all strongest compute components
class Scc:

    #   graph - directed graph with specified number of vertices
    #   transposed - same graph but transposed
    #   visited - array with data if vertex has been visited
    #   process_time - array of vertices sorted by process time increasingly
    def __init__(self, vertices_count):
        self.graph = getGraph("D", vertices_count)
        self.transposed = getGraph("D", vertices_count, True)
        self.visited = [False] * self.graph.vertices
        self.process_time = []

    #   dfs which adds vertices to array of process time
    def DFS(self, vertex):

        prev = [None] * self.graph.vertices

        cur = self.graph.verticesList[vertex - 1]
        self.visited[cur.name] = True

        can_move = True
        while cur.name != vertex - 1 or can_move:

            can_move = False
            for neighbour in cur.neighbours:
                if not self.visited[neighbour.name]:

                    prev[neighbour.name] = cur.name

                    cur = neighbour
                    self.visited[cur.name] = True
                    can_move = True

                    break
            if not can_move:

                #   adds vertex to process time array
                self.process_time.append(cur.name)

                #   if there is only one vertex it continues
                if prev[cur.name] is None:
                    continue

                can_move = True

                cur = self.graph.verticesList[prev[cur.name]]

                #   if previous vertex is starting vertex adds it to process time array
                if prev[cur.name] is None:
                    self.process_time.append(cur.name)

    #   dfs on transposed graph which prints strongest compute components
    def TDFS(self, vertex):

        prev = [None] * self.transposed.vertices

        cur = self.transposed.verticesList[vertex - 1]
        self.visited[cur.name] = True

        #   r - array of result vertices
        r = []
        can_move = True
        while cur.name != vertex - 1 or can_move:
            if cur.name + 1 not in r:
                r.append(cur.name + 1)

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

                cur = self.transposed.verticesList[prev[cur.name]]

        print(str(r))

    #   executes algorithm
    def execute(self):

        #   loop runs dfs on all unvisited vertices
        #   while False in self.visited:
        for i in range(self.graph.vertices):
            if not self.visited[i]:
                self.DFS(i + 1)

        #   resets array of visited vertices
        self.visited = [False] * self.graph.vertices

        #   loop runs dfs on last vertex in process time array
        while len(self.process_time) > 0:

            cur = self.process_time.pop(len(self.process_time) - 1)
            if not self.visited[cur]:
                self.TDFS(cur + 1)
