from enum import Enum

class GenType(Enum):
    BACKTRACKER = 1
    ELLER = 2
    
class NodeType(Enum):
    EMPTY = 0
    WALL = 1
    PATH = 2
    VISITED = 3

class SolveType(Enum):
    ASTAR = 1
    DIJKSTRA = 2
    