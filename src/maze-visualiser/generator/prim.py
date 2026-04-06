import random
from util.enum import NodeType
import util.graph_info as graphinfo

class PrimGenerator:
    """
    Class that generates mazes using a randomised Prim's algorithm.
    """
    
    def __init__(self, rows, cols):
        """
        The algorithm is initialised with a random cell and it's adjacent walls.
        """
        
        rows = rows if rows % 2 == 1 else rows + 1
        cols = cols if cols % 2 == 1 else cols + 1

        self.rows = rows
        self.cols = cols
        self.grid = [[NodeType.WALL for _ in range(cols)] for _ in range(rows)]

        self.visited = set()
        self.nodes = set()
        self.nodes.update((r, c) for r in range(1, self.rows, 2) for c in range(1, self.cols, 2))
        self.h_walls = []
        self.v_walls = []

        start_cell = random.choice(list(self.nodes))
        self.add_walls(start_cell)
        self.visited.add(start_cell)

    def add_walls(self, cell):
        """
        Adds adjacent walls of the given cell to the wall lists.
        """
        
        row, col = cell
        
        if (row > 2):
            self.h_walls.append((row - 1, col)) # North wall
        if (row < self.rows - 2):
            self.h_walls.append((row + 1, col)) # South wall
        if (col > 2):
            self.v_walls.append((row, col - 1)) # West wall
        if (col < self.cols - 2):
            self.v_walls.append((row, col + 1)) # East wall

    def step(self):
        """
        Single step of Prim's algorithm.
        A random vertical or horizontal wall is chosen from the wall list.
        If one of the cells separated by the wall is visited:
            The wall is removed and turned into a passage.
            The walls of the unvisited cell are added to the wall list.
        Otherwise step() repeats.
        """
        
        if not self.h_walls and not self.v_walls:
            return True
        
        wall_orientation = random.choice(['V', 'H'])

        if not self.h_walls:
            wall_orientation = 'V'
        elif not self.v_walls:
            wall_orientation = 'H'

        node_1 = None
        node_2 = None

        match wall_orientation:
            case 'V':
                wall = random.choice(self.v_walls)
                node_1 = (wall[0], wall[1] - 1)
                node_2 = (wall[0], wall[1] + 1)
                self.v_walls.remove(wall)
            case 'H':
                wall = random.choice(self.h_walls)
                self.h_walls.remove(wall)
                node_1 = (wall[0] - 1, wall[1])
                node_2 = (wall[0] + 1, wall[1])
        
        node_1_visited = node_1 in self.visited
        node_2_visited = node_2 in self.visited

        if node_1_visited ^ node_2_visited:
            self.grid[wall[0]][wall[1]] = NodeType.EMPTY
            
            if node_1_visited:
                new_node = node_2
            else:
                new_node = node_1

            self.visited.add(new_node)
            self.add_walls(new_node)
            self.grid[node_1[0]][node_1[1]] = NodeType.EMPTY
            self.grid[node_2[0]][node_2[1]] = NodeType.EMPTY
        else: 
            self.step() # Run step() until a single passage is made

    def get_state_info(self):
        """Returns real time data about the algorithm."""

        return (f"Prim's Algorithm Generator", f"",
                f"Vertical Wall list size: {len(self.v_walls)}",
                f"Horizontal Wall list size: {len(self.h_walls)}",
                f"Visited nodes: {len(self.visited)}",
                f"Leaf nodes: {graphinfo.count_leaf_nodes(self.grid)}")
    