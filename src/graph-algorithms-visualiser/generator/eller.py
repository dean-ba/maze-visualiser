import random
from util.enum import NodeType

class EllerGenerator:
    """
    Class that generates a maze using Eller's algorithm using sets.
    The maze is a 2D grid of walls and empty cells.
    Cells are every point in the grid where the row and column is odd.
    """

    def __init__(self, rows, cols):
        """
        Initialises the generator with a grid of walls, and an empty dictionary of rows. 
        row_sets is a dictionary that contains a dictionary for each row.
        Each row dictionary holds positions as keys and set ID's as values.
        """

        rows = rows if rows % 2 == 1 else rows + 1
        cols = cols if cols % 2 == 1 else cols + 1

        self.cols = cols
        self.rows = rows
        self.grid = [[NodeType.WALL for _ in range(self.cols)] for _ in range(self.rows)]
        self.row_sets = {}
        self.set_id_counter = 0
        self.current_row = 1

    def gen_sets(self):
        """
        Initialises a new row in row_sets.
        positions are added to the new row, and given a new set ID if their parent created a south wall.
        """
        
        if self.current_row not in self.row_sets:
            self.row_sets[self.current_row] = {}

        for col in range(1, self.cols, 2):
            if col not in self.row_sets[self.current_row]:
                self.row_sets[self.current_row][col] = self.set_id_counter
                self.set_id_counter += 1
            self.grid[self.current_row][col] = NodeType.EMPTY

    def remove_east_walls(self):
        """
        Removes the east wall of cells if they are not part of the same set.
        East walls are also removed at random.
        If the final row is being generated, east walls between different sets are always removed

        If a wall is removed, the sets are then merged.
        """

        for pos in range(1, self.cols - 2, 2):
            if self.row_sets[self.current_row][pos] != self.row_sets[self.current_row][pos + 2]:
                if random.choice([True, False]) or self.current_row == self.rows - 2:
                    self.grid[self.current_row][pos + 1] = NodeType.EMPTY
                    old_set = self.row_sets[self.current_row][pos + 2]
                    new_set = self.row_sets[self.current_row][pos]
                    
                    for cell in self.row_sets[self.current_row]:
                        if self.row_sets[self.current_row][cell] == old_set:
                            self.row_sets[self.current_row][cell] = new_set
    
    def create_south_passages(self):
        """
        Cells are categorised into sets, then south passages are carved into the maze.
        South passages can be made at random, but each set must have at least one cell with a south passage.
        This ensures that the graph is fully connected.
        """
        
        new_row_sets = {}
        set_cells = {}

        for col in self.row_sets[self.current_row]:
            cell_set = self.row_sets[self.current_row][col]
            if cell_set not in set_cells:
                set_cells[cell_set] = []
            set_cells[cell_set].append(col)

        for cell_set, cells in set_cells.items():
            south_passages = 0
            last_cell = None
            for c in cells:
                if random.choice([True, False]) or len(cells) == 1:
                    self.grid[self.current_row + 1][c] = NodeType.EMPTY
                    self.grid[self.current_row + 2][c] = NodeType.EMPTY
                    new_row_sets[c] = cell_set
                    south_passages += 1
                last_cell = c

            if south_passages == 0:
                self.grid[self.current_row + 1][last_cell] = NodeType.EMPTY
                self.grid[self.current_row + 2][last_cell] = NodeType.EMPTY
                new_row_sets[last_cell] = cell_set

        self.row_sets[self.current_row + 2] = new_row_sets      

    def step(self):
        """
        Carries out one step of generation.
        Each step generates a single row.
        """

        if self.current_row >= self.rows:
            return True
        
        self.gen_sets()
        self.remove_east_walls()    
        if self.current_row < self.rows - 2:
            self.create_south_passages()
        self.current_row += 2

        return False
    
    def count_leaf_nodes(self):
        """Function to count the amount of leaf nodes (dead ends) in a graph."""

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
        """Returns real time data about the algorithm."""
        
        return (f"Leaf nodes: {self.count_leaf_nodes()}", 
                f"Active sets: {len(set(self.row_sets.get(self.current_row, {}).values()))}")
    