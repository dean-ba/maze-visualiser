import random
from util.node_type import NodeType

class Node:
    def __init__(self, set):
        self.set = set
        self.east = False
        self.south = False

class EllerGenerator:

    def __init__(self, rows, cols):
        rows = rows if rows % 2 == 1 else rows + 1
        cols = cols if cols % 2 == 1 else cols + 1

        self.rows = rows
        self.cols = cols
        self.grid = [[NodeType.EMPTY for _ in range(cols)] for _ in range(rows)]
        self.grid[0] = [NodeType.WALL for _ in range(cols)]
        self.current_row = [Node(0) for _ in range((cols - 1) // 2)]
        self.current_row_num = 0
        self.new_set_num = 1


    def gen_sets(self):
        for index, node in enumerate(self.current_row):
            if node.set == 0:
                node.set = self.new_set_num
                self.new_set_num += 1
    
    def union(self, set_1, set_2):
        self.new_set_num += 1
        for index, node in enumerate(self.current_row):
            if node.set == set_1 or node.set == set_2:
                node.set = set_2
    
    def not_isolated(self, set):
        open_count = 0

        for node in self.current_row:
            if node.set == set and not node.south:
                open_count += 1
                if open_count > 1:
                    return True
                
        return False

    def gen_row(self):
        for i in range(len(self.current_row) - 1): #east walls
            if self.current_row[i].set == self.current_row[i + 1].set or random.choice([True, False]):
                self.current_row[i].east = True
            else:
                self.union(self.current_row[i].set, self.current_row[i + 1].set)
        self.current_row[len(self.current_row) - 1].east = True

        for index, node in enumerate(self.current_row):
            if random.choice([True, False]) and self.not_isolated(node.set):
                node.south = True

    def reset_row(self):
        for col, node in enumerate(self.current_row):
            node.east = False
            if node.south:
                node.set = 0
                node.south = False

    def update_grid(self):
        grid_idx = self.current_row_num * 2 + 1
        self.grid[grid_idx][0] = NodeType.WALL
        self.grid[grid_idx + 1][0] = NodeType.WALL

        for col, node in enumerate(self.current_row):
            if node.east:
                self.grid[grid_idx + 1][col * 2 + 2] = NodeType.WALL
                self.grid[grid_idx][col * 2 + 2] = NodeType.WALL
                self.grid[grid_idx - 1][col * 2 + 2] = NodeType.WALL
            if node.south:
                self.grid[grid_idx + 1][col * 2 + 2] = NodeType.WALL
                self.grid[grid_idx + 1][col * 2 + 1] = NodeType.WALL
                self.grid[grid_idx + 1][col * 2] = NodeType.WALL
                


    def step(self):

        if self.current_row_num < self.rows / 2 - 2:

            self.gen_sets()

            self.gen_row()

            self.update_grid()

            self.current_row_num += 1

            if self.current_row_num < self.rows / 2 - 2:
                self.reset_row()
            return False
        
        for i in range(len(self.current_row) - 1):
            self.current_row[i].south = True

            if self.current_row[i].set != self.current_row[i + 1].set:
                self.current_row[i].east = False
                self.union(self.current_row[i].set, self.current_row[i + 1].set)

        self.update_grid()

        return True

    def get_state_info(self):
        return (f"",
                f"")
