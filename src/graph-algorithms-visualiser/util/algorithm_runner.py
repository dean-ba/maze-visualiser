from generator.backtracker import BacktrackerGenerator
from generator.eller import EllerGenerator
from solver.astar import Astar
from solver.dijkstra import Dijkstra
from util.node_type import NodeType
from util.gen_type import GenType
from util.solve_type import SolveType

class AlgorithmRunner:
    """
    Class to run both generation and solving algorithms for graphs.
    """

    def __init__(self):
        self.generator_state_info = []
        self.solver_state_info = []
        self.generator = None
        self.solver = None
        self.generating = False
        self.solving = False
        self.graph = None
        self.config = None
        self.cell_size = 0

    def handle_tick(self):
        """Carries out a single step of the currently running algorithm."""
        if self.generating and self.generator:
            done = self.generator.step()
            if done:
                self.generating = False
                self.generator = None

        if self.solving and self.solver and not self.generating:
            solvable = self.solver.step()
            if self.solver.solved or not solvable:
                self.solving = False

        if self.solver and self.solver.path_node != None:
            self.solver.graph[self.solver.path_node.pos[0]][self.solver.path_node.pos[1]] = NodeType.PATH
            self.solver.path_node = self.solver.path_node.parent
            if not self.solver.path_node:
                self.solver = None
        
        self.graph = self.get_graph()
        self.solver_state_info = self.solver.get_state_info() if self.solver else self.solver_state_info
        self.generator_state_info = self.generator.get_state_info() if self.generator else self.generator_state_info

    def get_graph(self):
        if self.generator:
            return self.generator.grid
        elif self.solver:
            return self.solver.graph
        return self.graph

    def start_gen(self):
        """Initialises the generation algorithm to be used."""

        if not self.generating and not self.solving:
            match self.config.gen_algorithm:
                case GenType.BACKTRACKER:
                    self.generator = BacktrackerGenerator(self.config.graph_height, self.config.graph_width)
                case GenType.ELLER:
                    self.generator = EllerGenerator(self.config.graph_height, self.config.graph_width)
                case _:
                    return
            self.cell_size = self.config.cell_size
            self.generating = True
            self.solver_state_info = []

    def start_solve(self):
        """Initialises the solving algorithm to be used."""

        if not self.graph:
            return

        if not self.generating and not self.solving:
            self.clean_graph()

            match self.config.solve_algorithm:
                case SolveType.ASTAR:
                    self.solver = Astar(self.graph)
                case SolveType.DIJKSTRA:
                    self.solver = Dijkstra(self.graph)
                case _:
                    return
            self.solving = True

    def clean_graph(self):
        rows = len(self.graph)
        cols = len(self.graph[0])
        for row in range(rows):
            for col in range(cols):
                match self.graph[row][col]:
                    case NodeType.WALL:
                        continue
                    case NodeType.EMPTY:
                        continue
                    case _:
                        self.graph[row][col] = NodeType.EMPTY
    