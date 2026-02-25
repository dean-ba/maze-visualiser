import random
from util.node_type import NodeType

class BacktrackerGenerator:
    """
    Class that generates a maze using a backtracking algorithm with a stack.
    The maze is a 2D grid of walls and empty cells.
    Cells are every point in the grid where the row and column is odd.
    """

    def __init__(self, rows, cols):
        """ Initialises the generator with a grid of walls, and adds a random cell to the stack. """

        rows = rows if rows % 2 == 1 else rows + 1
        cols = cols if cols % 2 == 1 else cols + 1

        self.rows = rows
        self.cols = cols
        self.grid = [[NodeType.WALL for _ in range(cols)] for _ in range(rows)]

        start_row = random.randrange(1, rows, 2)
        start_col = random.randrange(1, cols, 2)
        self.start_cell = (start_row, start_col)
        self.grid[start_row][start_col] = 0

        self.stack = [self.start_cell]
        self.visited_count = 0
        self.backtracks = 0

    def get_unvisited_neighbors(self, cell):
        """
        Gets all cells adjacent to the current cell that have not been visited.
        Cells are marked visited when they are changed to paths.
        """

        row, col = cell
        neighbors = []

        if row > 1 and self.grid[row - 2][col] == NodeType.WALL:
            neighbors.append((row - 2, col))
        if row < self.rows - 2 and self.grid[row + 2][col] == NodeType.WALL:
            neighbors.append((row + 2, col))
        if col > 1 and self.grid[row][col - 2] == NodeType.WALL:
            neighbors.append((row, col - 2))
        if col < self.cols - 2 and self.grid[row][col + 2] == NodeType.WALL:
            neighbors.append((row, col + 2))

        return neighbors

    def step(self):
        """
        Carries out one step of generation.
        Generation ends when the stack of unvisited cells is empty.
        Unvisited neighbours of each cell are added to the stack, and a wall is broken between one of them.
        """

        if not self.stack:
            return True
        
        current_cell = self.stack.pop()
        self.visited_count += 1
        neighbors = self.get_unvisited_neighbors(current_cell)

        if neighbors:
            self.stack.append(current_cell)
            next_cell = random.choice(neighbors)

            row_wall = (current_cell[0] + next_cell[0]) // 2
            col_wall = (current_cell[1] + next_cell[1]) // 2
            self.grid[row_wall][col_wall] = NodeType.EMPTY
            self.grid[next_cell[0]][next_cell[1]] = NodeType.PATH

            self.stack.append(next_cell)
        else:
            self.backtracks += 1

        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == NodeType.PATH:
                    self.grid[row][col] = NodeType.EMPTY

        if self.stack:
            row, col = self.stack[-1]
            self.grid[row][col] = NodeType.PATH

        return False
    
    def count_leaf_nodes(self):
        leaf_count = 0

        for row in range(1, self.rows, 2):
            for col in range(1, self.cols, 2):

                if self.grid[row][col] == NodeType.WALL:
                    continue

                connections = 0

                if self.grid[row - 1][col] == NodeType.EMPTY:
                    connections += 1
                if self.grid[row + 1][col] == NodeType.EMPTY:
                    connections += 1
                if self.grid[row][col - 1] == NodeType.EMPTY:
                    connections += 1
                if self.grid[row][col + 1] == NodeType.EMPTY:
                    connections += 1

                if connections == 1:
                    leaf_count += 1

        return leaf_count

    def get_state_info(self):
        return (f"Stack size: {len(self.stack)}",
                f"Visited: {self.visited_count}",
                f"Backtracks: {self.backtracks}",
                f"Leaf nodes: {self.count_leaf_nodes()}")
    