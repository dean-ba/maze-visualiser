from solver.astar import Astar
from solver.dijkstra import Dijkstra
from solver.dead_end_filling import DeadEndFiller
from solver.backtracker import BacktrackerSolver
from solver.random_mouse import RandomMouseSolver
from util.enum import NodeType
from util.enum import SolveType

class SolverRunner:
    """
    Class to run solving algorithms for graphs.
    """

    def __init__(self):
        """Initialises the class with no solver, and no state information."""

        self.state_info = []
        self.generator = None
        self.solver = None
        self.generating = False
        self.solving = False
        self.graph = None

    def handle_tick(self):
        """Carries out a single step of the currently running algorithm."""

        if self.solving and self.solver:
            solvable = self.solver.step()
            if self.solver.solved or not solvable:
                self.solving = False

        if self.solver and self.solver.solved:
            if self.solver.path_node != None:
                self.solver.path_step()
            if not self.solver.path_node:
                self.solver = None
        
        self.graph = self.get_graph()
        self.state_info = self.solver.get_state_info() if self.solver else self.state_info

    def get_graph(self):
        """Updates the graph held by the class if an algorithm has an updated one."""

        if self.solver:
            return self.solver.graph
        return self.graph


    def start_solve(self, solve_algorithm):
        """Initialises the solving algorithm to be used."""

        if not self.graph:
            return

        if not self.solving:
            self.clean_graph()

            match solve_algorithm:
                case SolveType.ASTAR:
                    self.solver = Astar(self.graph)
                case SolveType.DIJKSTRA:
                    self.solver = Dijkstra(self.graph)
                case SolveType.DEAD_END_FILLER:
                    self.solver = DeadEndFiller(self.graph)
                case SolveType.BACKTRACKER_SOLVER:
                    self.solver = BacktrackerSolver(self.graph)
                case SolveType.RANDOM_MOUSE:
                    self.solver = RandomMouseSolver(self.graph)
                case _:
                    return
            self.solving = True

    def clean_graph(self):
        """Function to reset search and path cells to empty cells for a new solving algorithm."""

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
    