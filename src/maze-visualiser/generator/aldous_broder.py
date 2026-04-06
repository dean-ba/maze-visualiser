import random
from util.enum import NodeType
import util.graph_info as graphinfo

class AldousBroderGenerator:
    """
    Algorithm to produce uniform spanning trees, adapted to be viewed as a graph.
    """
    
    def __init__(self, rows, cols):

        rows = rows if rows % 2 == 1 else rows + 1
        cols = cols if cols % 2 == 1 else cols + 1

        self.rows = rows
        self.cols = cols
        self.grid = [[NodeType.WALL for _ in range(cols)] for _ in range(rows)]

        start_row = random.randrange(1, rows, 2)
        start_col = random.randrange(1, cols, 2)
        self.current = (start_row, start_col)

        self.nodes = [(row, col) for row in range(1, self.rows, 2) for col in range(1, self.cols, 2)]
        self.visited = {self.current}

        self.steps = 0

    def get_neighbors(self, cell):
        """
        Gets all cells adjacent to the current cell that have not been visited.
        Cells are marked visited when they are changed to paths.
        """

        row, col = cell
        neighbors = []

        if row > 1:
            neighbors.append((row - 2, col))
        if row < self.rows - 2:
            neighbors.append((row + 2, col))
        if col > 1:
            neighbors.append((row, col - 2))
        if col < self.cols - 2:
            neighbors.append((row, col + 2))

        return neighbors
    
    def step(self):
        """
        Picks a random neighbour to the current cell.
        If the neighbour is unvisited, the separating wall is broken.
        The neighbour then becomes the current cell.
        Ends when all cells are visited.
        """
        
        self.steps += 1
        self.grid[self.current[0]][self.current[1]] = NodeType.EMPTY
        
        if len(self.nodes) == len(self.visited):
            return True
        
        neighbour = random.choice(self.get_neighbors(self.current))

        if not neighbour in self.visited:
            self.visited.add(neighbour)
            row_wall = (self.current[0] + neighbour[0]) // 2
            col_wall = (self.current[1] + neighbour[1]) // 2
            self.grid[row_wall][col_wall] = NodeType.EMPTY

        self.grid[neighbour[0]][neighbour[1]] = NodeType.PATH
        self.current = neighbour

    def get_state_info(self):
        """Returns real time data about the algorithm."""
        
        return (f"Aldous-Broder Generator", f"",
                f"Steps: {self.steps}",
                f"Unique cells visited: {len(self.visited)}",
                f"Leaf nodes: {graphinfo.count_leaf_nodes(self.grid)}")
    