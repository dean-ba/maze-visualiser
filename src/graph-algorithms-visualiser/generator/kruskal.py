import random
from util.enum import NodeType

class KruskalGenerator:
    """
    Class that generates a maze using Kruskal's algorithm.
    """

    def __init__(self, rows, cols):
        """
        Initialises the generator with a dictionary of nodes and lists for walls.
        """

        rows = rows if rows % 2 == 1 else rows + 1
        cols = cols if cols % 2 == 1 else cols + 1

        self.rows = rows
        self.cols = cols
        self.grid = [[NodeType.WALL for _ in range(cols)] for _ in range(rows)]

        self.nodes = {}
        self.h_walls = []
        self.v_walls = []

        self.init_sets()

    def init_sets(self):
        """
        Gives each node in the graph a unique set number.
        All horizontal and vertical walls are added to their respective lists.
        """

        set_num = 0
        
        for row in range(1, self.rows, 2):
            for col in range(1, self.cols, 2):
                self.nodes.update({(row, col): set_num})
                set_num += 1

                if row < self.rows - 2:
                    self.v_walls.append((row + 1, col))


            for col in range(2, self.cols - 1, 2):
                self.h_walls.append((row, col))

    def compare_nodes(self, node_1, node_2, wall):
        """
        Compares the set value of two nodes.
        If they are different then they are connected, and their sets are combined.
        """
        
        if self.nodes[node_1] != self.nodes[node_2]:

                self.grid[wall[0]][wall[1]] = NodeType.EMPTY
                self.grid[node_1[0]][node_1[1]] = NodeType.EMPTY
                self.grid[node_2[0]][node_2[1]] = NodeType.EMPTY

                join_set = self.nodes[node_1]
                old_set = self.nodes[node_2]
                for cell in self.nodes:
                    if self.nodes[cell] == old_set:
                        self.nodes.update({cell: join_set})

    def step(self):
        """
        Carries out a single step of the algorithm.
        An unvisited wall is chosen from either the horizontal or vertical list.
        If the nodes separated by it are in different sets, the wall is broken and sets combined.
        The algorithm is complete when there is only one set left.
        """
        
        if len(set(self.nodes.values())) == 1:
            return True
        
        wall = None
        choice = ''

        if not self.h_walls:
            choice = 'V'
        elif not self.v_walls:
            choice = 'H'
        else:
            choice = 'V' if random.choice([True, False]) else 'H'

        wall = random.choice(self.v_walls) if choice == 'V' else random.choice(self.h_walls)
        
        if choice == 'V':
            self.v_walls.remove(wall)

            node_above = (wall[0] - 1, wall[1])
            node_below = (wall[0] + 1, wall[1])
            self.compare_nodes(node_above, node_below, wall)
        else:
            self.h_walls.remove(wall)

            node_left = (wall[0], wall[1] - 1)
            node_right = (wall[0], wall[1] + 1)
            self.compare_nodes(node_left, node_right, wall)

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

        return (f"Wall list size: {len(self.v_walls) + len(self.h_walls)}",
                f"Total number of sets: {len(set(self.nodes.values()))}",
                f"Leaf nodes: {self.count_leaf_nodes()}")
    