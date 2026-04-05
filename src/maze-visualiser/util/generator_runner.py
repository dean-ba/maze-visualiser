from generator.backtracker import BacktrackerGenerator
from generator.eller import EllerGenerator
from generator.kruskal import KruskalGenerator
from generator.prim import PrimGenerator
from generator.aldous_broder import AldousBroderGenerator
from generator.wilson import WilsonGenerator
from util.enum import GenType

class GeneratorRunner:
    """
    Class to run both generation and solving algorithms for graphs.
    """

    def __init__(self):
        """Initialises the class with no generator, and no state information."""

        self.generator_state_info = []
        self.generator = None
        self.generating = False
        self.graph = None

    def handle_tick(self):
        """Carries out a single step of the currently running algorithm."""
        
        if self.generating and self.generator:
            done = self.generator.step()
            if done:
                self.generating = False
                self.generator = None
        
        self.graph = self.get_graph()
        self.generator_state_info = self.generator.get_state_info() if self.generator else self.generator_state_info

    def get_graph(self):
        """Updates the graph held by the class if an algorithm has an updated one."""

        if self.generator:
            return self.generator.grid
        return self.graph

    def start_gen(self, gen_algorithm, rows, cols):
        """Initialises the generation algorithm to be used."""

        if not self.generating:
            match gen_algorithm:
                case GenType.BACKTRACKER:
                    self.generator = BacktrackerGenerator(rows, cols)
                case GenType.ELLER:
                    self.generator = EllerGenerator(rows, cols)
                case GenType.KRUSKAL:                    
                    self.generator = KruskalGenerator(rows, cols)
                case GenType.PRIM:
                    self.generator = PrimGenerator(rows, cols)
                case GenType.ALDOUS_BRODER:
                    self.generator = AldousBroderGenerator(rows, cols)
                case GenType.WILSON:
                    self.generator = WilsonGenerator(rows, cols)
                case _:
                    return
            self.generating = True

    