# tests for graph.py - creates new graph and prints it
from graph import *


graph_type = "D"
vertices_amount = "10"

graph = getGraph(graph_type, vertices_amount)
graph.print()
