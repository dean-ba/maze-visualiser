import random
from util.enum import NodeType
import util.graph_info as graphinfo

class WilsonGenerator:
    """
    Class that generates mazes using Wilson's algorithm.
    Uses random walks to create a uniform spanning tree.
    """
    
    def __init__(self, rows, cols):
        rows = rows if rows % 2 == 1 else rows + 1
        cols = cols if cols % 2 == 1 else cols + 1

        self.rows = rows
        self.cols = cols
        self.grid = [[NodeType.WALL for _ in range(cols)] for _ in range(rows)]

        self.visited = set()
        self.nodes = set()
        self.nodes.update((r, c) for r in range(1, self.rows, 2) for c in range(1, self.cols, 2))
        
        start_cell = random.choice(list(self.nodes))
        self.visited.add(start_cell)
        self.grid[start_cell[0]][start_cell[1]] = NodeType.EMPTY
        
        self.walk_nodes = []
        self.current_walk = []
        self.unvisited = set(self.nodes) - self.visited
        self.total_walks = 0

    def get_neighbors(self, cell):
        """
        Gets all adjacent cells to the current cell.
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
        Single step of Wilson's algorithm.
        Randomly walks a path from a random node until part of the generated maze is found.
        Loops in random walks are not permitted.
        The walk is then turned into part of the maze and repeats until fully generated.
        """
        
        if not self.unvisited:
            return True
        
        if not self.walk_nodes:
            start_cell = random.choice(list(self.unvisited))
            self.walk_nodes = [start_cell]
            self.current_walk = [start_cell]
            self.grid[start_cell[0]][start_cell[1]] = NodeType.VISITED
            return False
        
        current_cell = self.walk_nodes[-1]
        
        neighbors = self.get_neighbors(current_cell)
        next_cell = random.choice(neighbors)

        if next_cell in self.walk_nodes:
            loop_index = self.current_walk.index(next_cell)
            
            for cell in self.current_walk[loop_index + 1:]:
                self.grid[cell[0]][cell[1]] = NodeType.WALL
            
            self.walk_nodes = self.walk_nodes[:self.walk_nodes.index(next_cell) + 1]
            self.current_walk = self.current_walk[:loop_index + 1]
            return False
        
        self.walk_nodes.append(next_cell)

        wall_row = (current_cell[0] + next_cell[0]) // 2
        wall_col = (current_cell[1] + next_cell[1]) // 2
        between_wall = (wall_row, wall_col)

        self.current_walk.append(between_wall)  
        self.current_walk.append(next_cell)
        self.grid[next_cell[0]][next_cell[1]] = NodeType.VISITED
        self.grid[wall_row][wall_col] = NodeType.VISITED

        if next_cell in self.visited:
            self.add_walk()
            self.walk_nodes = []
        
        return False

    def add_walk(self):
        """
        Permanently adds the current walk to the grid.
        """

        self.total_walks += 1

        for cell in self.walk_nodes:
                self.visited.add(cell)
                self.unvisited.discard(cell)
            
        for i in range(len(self.walk_nodes) - 1):
            current = self.walk_nodes[i]
            next_cell = self.walk_nodes[i + 1]

            wall_row = (current[0] + next_cell[0]) // 2
            wall_col = (current[1] + next_cell[1]) // 2
            self.grid[wall_row][wall_col] = NodeType.EMPTY
            self.grid[current[0]][current[1]] = NodeType.EMPTY
        
        last_cell = self.walk_nodes[-1]
        self.grid[last_cell[0]][last_cell[1]] = NodeType.EMPTY

    def get_state_info(self):
        """
        Returns real time data about the algorithm.
        """
        
        return (f"Wilson's Algorithm Generator", f"",
                f"Cells visited: {len(self.visited)}/{len(self.nodes)}",
                f"Current walk length: {len(self.current_walk)}",
                f"Total walks: {self.total_walks}",
                f"Leaf nodes: {graphinfo.count_leaf_nodes(self.grid)}")
    