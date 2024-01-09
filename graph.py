from settings import cols, rows
from node import Node


class Graph:
    def __init__(self):
        self.nodes = [[Node(x, y) for y in range(rows)] for x in range(cols)]
        self.open_nodes = []
        self.visited_nodes = []
        self.path_nodes = []

        self.add_edges()

    def add_edges(self):
        for column in self.nodes:
            for node in column:
                node.add_neighbors(self.nodes)
