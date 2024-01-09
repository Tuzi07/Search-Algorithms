import math, time


def heuristics(a, b):
    return math.sqrt((a.x - b.x) ** 2 + abs(a.y - b.y) ** 2)


class GraphSearcher:
    def __init__(self, graph, end, algorithm):
        self.graph = graph
        self.end = end
        self.algorithm = algorithm

    def next_node(self):
        if self.algorithm == "Largura" or self.algorithm == "Hill Climbing":
            return self.graph.open_nodes[0]

        elif self.algorithm == "Profundidade":
            return self.graph.open_nodes[-1]

        elif self.algorithm == "Custo Uniforme":
            return min(self.graph.open_nodes, key=lambda x: x.cost)

        elif self.algorithm == "Best First":
            return min(self.graph.open_nodes, key=lambda x: x.heuristic)

        elif self.algorithm == "A*" or self.algorithm == "A* limitado":
            return min(self.graph.open_nodes, key=lambda x: x.estimated_cost)

    def search_node(self, current_node):
        if self.algorithm == "A* limitado":
            self.search_from_node_with_limited_memory(current_node)

        elif self.algorithm == "Hill Climbing":
            self.hill_climbing_search_from_node(current_node)

        else:
            self.default_search_from_node(current_node)

    def default_search_from_node(self, current_node):
        self.graph.open_nodes.remove(current_node)
        self.graph.visited_nodes.append(current_node)

        for neighbor in current_node.neighbors:
            if neighbor not in self.graph.visited_nodes and not neighbor.wall:
                temp_cost = current_node.cost + 1

                is_better_path = False
                if neighbor in self.graph.open_nodes:
                    if temp_cost < neighbor.cost:
                        neighbor.cost = temp_cost
                        is_better_path = True
                else:
                    neighbor.cost = temp_cost
                    is_better_path = True
                    self.graph.open_nodes.append(neighbor)

                if is_better_path:
                    neighbor.heuristic = heuristics(neighbor, self.end)
                    neighbor.estimated_cost = neighbor.cost + neighbor.heuristic
                    neighbor.previous = current_node

    def search_from_node_with_limited_memory(self, current_node):
        self.graph.open_nodes.remove(current_node)
        self.graph.visited_nodes.append(current_node)

        for neighbor in current_node.neighbors:
            if neighbor not in self.graph.visited_nodes and not neighbor.wall:
                temp_cost = current_node.cost + 1

                is_better_path = False
                should_try_to_append = False
                if neighbor in self.graph.open_nodes:
                    if temp_cost < neighbor.cost:
                        neighbor.cost = temp_cost
                        is_better_path = True
                else:
                    neighbor.cost = temp_cost
                    is_better_path = True
                    if len(self.graph.open_nodes) == 10:
                        should_try_to_append = True
                    else:
                        self.graph.open_nodes.append(neighbor)

                if is_better_path:
                    neighbor.heuristic = heuristics(neighbor, self.end)
                    neighbor.estimated_cost = neighbor.cost + neighbor.heuristic
                    neighbor.previous = current_node
                    if should_try_to_append:
                        highest_estimated_cost_node = self.highest_estimated_cost_node()
                        if (
                            neighbor.estimated_cost
                            < highest_estimated_cost_node.estimated_cost
                        ):
                            self.graph.open_nodes.remove(highest_estimated_cost_node)
                            self.graph.open_nodes.append(neighbor)

    def highest_estimated_cost_node(self):
        return max(self.graph.open_nodes, key=lambda x: x.estimated_cost)

    def hill_climbing_search_from_node(self, current_node):
        self.graph.open_nodes.remove(current_node)
        self.graph.visited_nodes.append(current_node)

        best_neighbor = None

        for neighbor in current_node.neighbors:
            if neighbor not in self.graph.visited_nodes and not neighbor.wall:
                neighbor.heuristic = heuristics(neighbor, self.end)
                if best_neighbor == None:
                    best_neighbor = neighbor
                elif neighbor.heuristic < best_neighbor.heuristic:
                    best_neighbor = neighbor

        if best_neighbor != None:
            self.graph.open_nodes.append(best_neighbor)
            best_neighbor.previous = current_node

        time.sleep(0.1)
