import random
from settings import cols, rows


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []

        self.heuristic = 0
        self.estimated_cost = 0
        self.cost = 0

        self.previous = None

        self.wall = False
        if random.randint(0, 100) < 20:
            self.wall = True

    def add_neighbors(self, graph):
        x_offset = (1, 0, 0, -1)
        y_offset = (0, -1, 1, 0)

        # Diagonals
        # x_offset = (1,  1,  1,  0, 0, -1, -1, -1)
        # y_offset = (-1, 0,  1, -1, 1, -1,  0,  1)

        for x, y in zip(x_offset, y_offset):
            if (
                self.x + x > -1
                and self.y + y > -1
                and self.x + x < cols
                and self.y + y < rows
            ):
                self.neighbors.append(graph[self.x + x][self.y + y])
