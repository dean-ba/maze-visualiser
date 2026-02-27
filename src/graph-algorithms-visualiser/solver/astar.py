from util.enum import NodeType

class Node:
    """
    Helper class for storing graph node information.
    pos: node position in graph.
    g_cost: distance from node to start position.
    h_cost: manhattan distance from node to target node.
    parent: node searched before current node.
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
        self.visited_count = 0
        self.current = self.open[0]

    def get_neighbors(self, cell):
        """Gets all cells adjacent to the current cell that are not walls."""
        
        row, col = cell
        neighbors = []

        if row > 1 and self.graph[row - 1][col] != NodeType.WALL:
            neighbors.append((row - 1, col))
        if row < self.rows - 1 and self.graph[row + 1][col] != NodeType.WALL:
            neighbors.append((row + 1, col))
        if col > 1 and self.graph[row][col - 1] != NodeType.WALL:
            neighbors.append((row, col - 1))
        if col < self.cols - 1 and self.graph[row][col + 1] != NodeType.WALL:
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

        self.current = min(self.open, key=lambda x: x.f_cost)
        self.visited_count += 1
        self.open.remove(self.current)
        self.graph[self.current.pos[0]][self.current.pos[1]] = NodeType.VISITED

        if self.current.pos == self.target:
            self.solved = True
            self.path_node = self.current
            return True

        neighbours = self.get_neighbors(self.current.pos)

        for neighbour in neighbours:
            in_closed = any(node.pos == neighbour for node in self.closed)
            if in_closed:
                continue
            
            g_cost = self.current.g_cost + 1
            h_cost = abs(neighbour[0] - self.target[0]) + abs(neighbour[1] - self.target[1])
            
            existing_node = None
            for node in self.open:
                if node.pos == neighbour:
                    existing_node = node
                    break
            
            if existing_node:
                if g_cost < existing_node.g_cost:
                    existing_node.g_cost = g_cost
                    existing_node.f_cost = g_cost + existing_node.h_cost
                    existing_node.parent = self.current
            else:
                neighbour_node = Node(neighbour, g_cost, h_cost, self.current)
                self.open.append(neighbour_node)

        self.closed.append(self.current)
        return True
    
    def get_state_info(self):
        """Returns real time data about the algorithm."""
        
        return (f"Open set size: {len(self.open)}",
                f"Closed set size: {len(self.closed)}",
                f"Current position: {self.current.pos}",
                f"{"Path length: " if self.solved else "Current F cost:"} {self.current.f_cost}")
    