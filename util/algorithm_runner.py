from generator.backtracker import BacktrackerGenerator
from solver.astar import Astar
from util.node_type import NodeType

class AlgorithmRunner:
    def __init__(self):
        self.generator = None
        self.solver = None
        self.generating = False
        self.solving = False
        self.graph = None

    def handle_tick(self):
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

    def get_graph(self):
        if self.generator:
            return self.generator.grid
        elif self.solver:
            return self.solver.graph
        return self.graph
    
    def set_backtracker(self):
        self.generator = BacktrackerGenerator(11, 11)

    def start_gen(self):
        self.generating = True

    def set_astar(self):
        self.solver = Astar(self.graph)

    def start_solve(self):
        self.solving = True