import math
from util.node_type import NodeType

class Node:
    """
    Helper class for storing graph node information.
    pos: node position in graph.
    parent: previous node in the path from the start to the current node.
    distance: distance from the current node to the start node.
    """

    def __init__(self, pos, parent, distance):
        self.pos = pos
        self.parent = parent
        self.distance = distance

class Dijkstra:
    """
    Class that finds a path between the top left and bottom right of a graph.
    Searches all available nodes and calculates their distance to the start node.
    the path to any node from the start can be found using the parents of the target node.
    """

    def __init__(self, graph):
        self.graph = graph
        self.rows = len(graph)
        self.cols = len(graph[0])
        self.solved = False
        self.path_node = None
        self.find_node = lambda target_pos: next((n for n in self.vertices if n.pos == target_pos), None)
        self.vertices = [
            Node((row, col), None, math.inf)
            for row in range(self.rows)
            for col in range(self.cols)
            if self.graph[row][col] == NodeType.EMPTY
        ]
        self.target = self.find_node((self.rows - 2, self.cols - 2))
        start = self.find_node((1, 1))
        start.distance = 0
        self.visited_count = 0

    def get_neighbors(self, cell):
        """Gets all nodes adjacent to the current cell that are not visited yet."""
        
        row, col = cell
        neighbors = []

        if row > 1 and self.graph[row - 1][col] != NodeType.WALL:
            node = self.find_node((row - 1, col))
            if node is not None:
                neighbors.append(node)
        if row < self.rows - 1 and self.graph[row + 1][col] != NodeType.WALL:
            node = self.find_node((row + 1, col))
            if node is not None:
                neighbors.append(node)
        if col > 1 and self.graph[row][col - 1] != NodeType.WALL:
            node = self.find_node((row, col - 1))
            if node is not None:
                neighbors.append(node)
        if col < self.cols - 1 and self.graph[row][col + 1] != NodeType.WALL:
            node = self.find_node((row, col + 1))
            if node is not None:
                neighbors.append(node)

        return neighbors

    def step(self):
        """
        Carries out a single step of the algorithm.
        The vertex with the shortest distance from the start node is removed from the queue.
        If the distance from the start to a neighbour through this node is lower than the neighbours current distance:
        - The neighbour's distance is updated to the lower value.
        - The neighbour's parent is set to the current node.
        """
        
        if not self.vertices:
            self.solved = True
            self.path_node = self.target
            return True
        
        current = min(self.vertices, key=lambda x: x.distance)
        self.visited_count += 1
        self.vertices.remove(current)
        self.graph[current.pos[0]][current.pos[1]] = NodeType.VISITED

        for node in self.get_neighbors(current.pos):
            dist = current.distance + 1
            if dist < node.distance:
                node.distance = dist
                node.parent = current

        return True
    
    def get_state_info(self):
        return (f"Vertices left: {len(self.vertices)}",
                f"Visited: {self.visited_count}",
                f"Path length: {self.target.distance}")
