import random

from util.enum import NodeType

class RandomMouseSolver:
    """Solving algorithm using a random walk."""

    def __init__(self, graph):
        self.graph = graph
        self.rows = len(graph)
        self.cols = len(graph[0])
        self.current = 1, 1
        self.graph[self.current[0]][self.current[1]] = NodeType.PATH
        self.target = self.rows - 2, self.cols - 2
        self.solved = False
        self.path_node = None
        self.steps = 0

    def get_neighbors(self, cell):
        """Returns all empty cells next to the current cell."""
        
        row, col = cell
        neighbors = []

        if row > 1 and self.graph[row - 1][col] == NodeType.EMPTY:
            neighbors.append((row - 1, col))
        if row < self.rows - 1 and self.graph[row + 1][col] == NodeType.EMPTY:
            neighbors.append((row + 1, col))
        if col > 1 and self.graph[row][col - 1] == NodeType.EMPTY:
            neighbors.append((row, col - 1))
        if col < self.cols - 1 and self.graph[row][col + 1] == NodeType.EMPTY:
            neighbors.append((row, col + 1))

        return neighbors
    
    def step(self):
        """
        Moves to a random neigbour each step until the end is reached with no bias.
        """

        if self.current == self.target:
            self.solved = True
            return True
        
        self.steps += 1
        
        self.graph[self.current[0]][self.current[1]] = NodeType.EMPTY
        self.current = random.choice(self.get_neighbors(self.current))
        self.graph[self.current[0]][self.current[1]] = NodeType.PATH
        return True
        
    def path_step(self):
        """Never used since the mouse does not remember the path."""
        return

    def get_state_info(self):
        """Returns real time data about the algorithm."""
        
        return (f"Random Mouse Solver", f"",
                f"Steps: {self.steps}")
    