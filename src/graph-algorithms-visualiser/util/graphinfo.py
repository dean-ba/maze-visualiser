from util.enum import NodeType

def count_leaf_nodes(graph):
        """Function to count the amount of leaf nodes (dead ends) in agraph."""

        leaf_count = 0

        for row in range(1, len(graph), 2):
            for col in range(1, len(graph[0]), 2):

                if graph[row][col] == NodeType.WALL:
                    continue

                connections = 0

                if graph[row - 1][col] == NodeType.EMPTY:
                    connections += 1
                if graph[row + 1][col] == NodeType.EMPTY:
                    connections += 1
                if graph[row][col - 1] == NodeType.EMPTY:
                    connections += 1
                if graph[row][col + 1] == NodeType.EMPTY:
                    connections += 1

                if connections == 1:
                    leaf_count += 1

        return leaf_count
