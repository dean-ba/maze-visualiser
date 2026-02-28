import random

from util.enum import NodeType

class DeadEndFiller:

    def __init__(self, graph):
        self.graph = graph
        self.rows = len(graph)
        self.cols = len(graph[0])
        self.start = 1, 1
        self.target = self.rows - 2, self.cols - 2
        self.solved = False
        self.leaves = self.count_leaf_nodes()
        random.shuffle(self.leaves)
        self.current_cell = None
        self.path_node = None
        self.visited_cells = 0

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
        Carries out one step of the algorithm.
        If a cell has one unvisited neigbour, its neighbour becomes the current cell.
        If a cell has more than one unvisited neighbours, it has reached a junction and stops visiting.
        When a dead end is fully visited, another dead end is selected from the list of leaves.
        When the leaves list is empty, all dead ends have been searched.
        """

        if not self.leaves and not self.current_cell:
            self.path_node = self.target
            self.solved = True
            return True
        
        if not self.current_cell:
            self.current_cell = self.leaves.pop()

        if self.current_cell == self.start or self.current_cell == self.target:
            self.current_cell = None
            return True

        neighbours = self.get_neighbors(self.current_cell)

        if len(neighbours) > 1:
            self.current_cell = None
        elif len(neighbours) > 0:
            self.graph[self.current_cell[0]][self.current_cell[1]] = NodeType.VISITED
            self.current_cell = neighbours[0]
            self.visited_cells += 1

        return True
    
    def path_step(self):
        """
        Finds the path of unvisited nodes from the target to the starting cell, one step at a time.
        """
        
        row, col = self.path_node
        self.graph[row][col] = NodeType.PATH

        if self.path_node == self.start:
            self.path_node = None
            return

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for r, c in directions:
            new_row = row + r
            new_col = col + c

            if (0 <= new_row < self.rows
                and 0 <= new_col < self.cols
                and self.graph[new_row][new_col] == NodeType.EMPTY
                ):
                self.path_node = (new_row, new_col)

    def count_leaf_nodes(self):
        """Function to get the positions of leaf nodes (dead ends) in a graph."""

        leaves = []

        for row in range(1, self.rows, 2):
            for col in range(1, self.cols, 2):

                if self.graph[row][col] == NodeType.WALL:
                    continue

                connections = 0

                if self.graph[row - 1][col] == NodeType.EMPTY:
                    connections += 1
                if self.graph[row + 1][col] == NodeType.EMPTY:
                    connections += 1
                if self.graph[row][col - 1] == NodeType.EMPTY:
                    connections += 1
                if self.graph[row][col + 1] == NodeType.EMPTY:
                    connections += 1

                if connections == 1:
                    leaves.append((row, col))

        return leaves

    def get_state_info(self):
        """Returns real time data about the algorithm."""
        
        return (f"Leaves to check: {len(self.leaves)}",
                f"Visited cells: {self.visited_cells}",
                f"Solved: {self.solved}")
    