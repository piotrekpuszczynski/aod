# tests for DFSandBFS.py - uses DFS and BFS and prints steps while walking through graph
from DFSandBFS import *


graph_type = "D"
vertices_count = "10"
search_type = "DFS"
return_tree = False

if search_type == "DFS":
    search = DFS(graph_type, vertices_count)
else:
    search = BFS(graph_type, vertices_count)

if return_tree:
    search.execute(1, return_tree).print()
else:
    search.execute(1, return_tree)
