from enum import Enum

class GenType(Enum):
    BACKTRACKER = 1
    ELLER = 2
    KRUSKAL = 3
    PRIM = 4
    
class NodeType(Enum):
    EMPTY = 0
    WALL = 1
    PATH = 2
    VISITED = 3

class SolveType(Enum):
    ASTAR = 1
    DIJKSTRA = 2
    DEAD_END_FILLER = 3
    BACKTRACKER_SOLVER = 4
    