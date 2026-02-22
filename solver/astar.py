class Node:
    """
    Helper class for storing graph node information.
    pos: node position in graph
    g_cost: distance from node to start position
    h_cost: manhattan distance from node to target node
    parent: node searched before current node
    """

    def __init__(self, pos, g_cost, h_cost, parent):
        self.pos = pos
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent

class Astar:
    """
    Class that finds a path between the top left and bottom right of a graph.
    Uses a heuristic to estimate the distance to the target cell.
    """

    def __init__(self, graph):
        self.graph = graph
        self.rows = len(graph)
        self.cols = len(graph[0])
        self.solved = False
        self.open = [Node((1, 1), 0, 0, None)]
        self.closed = []
        self.target = self.rows - 2, self.cols - 2
        self.path_node = None

    def get_neighbors(self, cell):
        """Gets all cells adjacent to the current cell that are not walls."""
        
        row, col = cell
        neighbors = []

        if row > 1 and self.graph[row - 1][col] != 1:
            neighbors.append((row - 1, col))
        if row < self.rows - 1 and self.graph[row + 1][col] != 1:
            neighbors.append((row + 1, col))
        if col > 1 and self.graph[row][col - 1] != 1:
            neighbors.append((row, col - 1))
        if col < self.cols - 1 and self.graph[row][col + 1] != 1:
            neighbors.append((row, col + 1))

        return neighbors

    def step(self):
        """
        Carries out a single step of the algorithm.
        Neighbours of nodes are selected based on their f_cost and added to the open list.
        Searched nodes are added to the closed list.
        """

        if not self.open:
            return False

        current = min(self.open, key=lambda x: x.f_cost)
        self.open.remove(current)
        self.graph[current.pos[0]][current.pos[1]] = 3

        neighbours = self.get_neighbors(current.pos)

        for neighbour in neighbours:
            if neighbour == self.target:
                self.solved = True
                self.path_node = Node(neighbour, 0, 0, current)
                return True
            else:
                g_cost = current.g_cost + 1
                h_cost = abs(neighbour[0] - self.target[0]) + abs(neighbour[1] - self.target[1])
                neighbour_node = Node(neighbour, g_cost, h_cost, current)

                in_open = any(node.pos == neighbour and node.f_cost < neighbour_node.f_cost for node in self.open)
                in_closed = any(node.pos == neighbour and node.f_cost < neighbour_node.f_cost for node in self.closed)

                if not in_open and not in_closed:
                    self.open.append(neighbour_node)

        self.closed.append(current)
        return True
    