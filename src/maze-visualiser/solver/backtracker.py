from util.enum import NodeType

class BacktrackerSolver:
    """
    Backtracking algorithm used to find a path between the beginning and end of a graph.
    Finds a path using a depth first search method implemented with a stack.
    The path created will not be the shortest path.
    """
    
    def __init__(self, graph):
        self.graph = graph
        self.rows = len(graph)
        self.cols = len(graph[0])
        self.stack = [(1, 1)]
        self.visited = []
        self.path_position = 0
        self.solved = False
        self.target = self.rows - 2, self.cols - 2
        self.current = None
        self.path_node = None

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
        A node is popped from the stack and any unvisited neighbours are pushed to the stack.
        The algorithm ends when the stack is empty or the target is found.
        """
        
        if not self.stack:
            return False
        
        self.current = self.stack.pop()
        self.visited.append(self.current)
        self.graph[self.current[0]][self.current[1]] = NodeType.VISITED

        if self.current == self.target:
            self.solved = True
            self.path_node = self.target
            self.path_position = len(self.visited) - 1
            return True
        
        neighbours = self.get_neighbors(self.current)

        for neighbour in neighbours:
            if neighbour not in self.visited:
                self.stack.append(neighbour)
        
        return True

    def path_step(self):
        """Adds a single visited node to the path."""

        if self.path_position < 1:
            self.graph[1][1] = NodeType.PATH
            self.path_node = None
            return
        node = self.visited[self.path_position]
        self.path_position -= 1
        self.graph[node[0]][node[1]] = NodeType.PATH

    def get_state_info(self):
        """Returns real time data about the algorithm."""

        return (f"Backtracking Solver", f"",
                f"Current position: {self.current}",
                f"Stack size: {len(self.stack)}",
                f"Total visited nodes: {len(self.visited)}")
    