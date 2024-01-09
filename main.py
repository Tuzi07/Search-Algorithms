import pygame, sys, inquirer
from graph import Graph
from graph_searcher import GraphSearcher
from settings import cols, rows, tile_size

WHITE = 255, 255, 255
BLACK = 0, 0, 0
LIGHT_BLUE = 25, 120, 250
RED = 255, 0, 0
GREEN = 0, 255, 0

# x0 = int(input("x inicial: "))
# y0 = int(input("y inicial: "))

# xf = int(input("x final: "))
# yf = int(input("y final: "))

algorithms = [
    "Largura",
    "Profundidade",
    "Custo Uniforme",
    "Best First",
    "Hill Climbing",
    "A*",
    "A* limitado",
]
algorithm_question = [
    inquirer.List("algorithm", message="Algorithm", choices=algorithms),
]

answer = inquirer.prompt(algorithm_question)
algorithm = answer["algorithm"]

pygame.init()
display_window = pygame.display.set_mode((cols * tile_size, rows * tile_size))
clock = pygame.time.Clock()

graph = Graph()


# start = graph.nodes[x0][x0]
# end = graph.nodes[xf][yf]
start = graph.nodes[cols // 4][rows // 4]
end = graph.nodes[cols - cols // 4][rows - rows // 4]

start.wall = False
end.wall = False

graph.open_nodes.append(start)
graph_searcher = GraphSearcher(graph, end, algorithm)


class PyGameInterface:
    def __init__(self):
        self.should_run = True
        self.is_searching = False

    def start(self):
        while self.should_run:
            self.handle_events()

            if self.is_searching:
                self.search()

            # print("open_nodes size = " + str(len(graph.open_nodes)))
            self.draw_result()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    self.put_or_remove_wall(pygame.mouse.get_pos(), event.button == 1)

            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] or event.buttons[2]:
                    self.put_or_remove_wall(pygame.mouse.get_pos(), event.buttons[0])

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.is_searching = True

    def put_or_remove_wall(self, pos, state):
        tile = graph.nodes[pos[0] // tile_size][pos[1] // tile_size]
        if tile not in (start, end):
            tile.wall = state

    def search(self):
        if len(graph.open_nodes) > 0:
            current_node = graph_searcher.next_node()

            if current_node == end:
                self.make_path(current_node)

            if self.is_searching:
                graph_searcher.search_node(current_node)

        else:
            self.should_run = False

    def make_path(self, current_node):
        temp = current_node
        while temp.previous:
            graph.path_nodes.append(temp.previous)
            temp = temp.previous

        self.is_searching = False

    def draw_result(self):
        for column in graph.nodes:
            for node in column:
                tile = node.x, node.y
                if node.wall:
                    self.paint(tile, BLACK)
                elif node == end:
                    self.paint(tile, LIGHT_BLUE)
                elif node in graph.path_nodes and not self.is_searching:
                    self.paint(tile, LIGHT_BLUE)
                elif node in graph.visited_nodes:
                    self.paint(tile, RED)
                elif node in graph.open_nodes:
                    self.paint(tile, GREEN)
                else:
                    self.paint(tile, WHITE)

        pygame.display.flip()

    def paint(self, tile, color):
        x, y = tile
        pygame.draw.rect(
            display_window,
            color,
            (x * tile_size, y * tile_size, tile_size - 1, tile_size - 1),
        )


PyGameInterface().start()
