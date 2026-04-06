import pygame
import sys
from util.config_manager import ConfigManager
from util.solver_runner import SolverRunner
from util.generator_runner import GeneratorRunner
from util.drawer import Drawer

class MazeVisualiser:
    """Class to encapsulate maze generation and solving."""

    def __init__(self):
        """Initialise pygame, components and state."""
        pygame.init()
        pygame.display.set_caption("Maze Visualiser")

        self.config = ConfigManager()
        self.solver_runner = SolverRunner()
        self.gen_runner = GeneratorRunner()
        self.screen = pygame.display.set_mode((self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT), pygame.RESIZABLE)
        self.drawer = Drawer(self.screen, pygame.font.SysFont("arial", 18))
        self.clock = pygame.time.Clock()

        self.accumulated_time = 0.0
        self.running = True
        self.graph = None

    def run(self):
        """Main application loop."""

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        """process key and button presses."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                self.config.handle_change_graph_size(event)
            
            for button in self.config.buttons:
                button.handle_event(event)

    def update(self):
        """Update generation or solving algorithm logic."""

        self.accumulated_time += self.clock.tick(60) / 1000

        if self.config.gen_start:
            self.start_generation()

        if self.config.solve_start and not self.gen_runner.generating:
            self.start_solving()

        self.process_ticks()

        self.update_graph()

    def start_generation(self):
        """Start a generation algorithm."""

        self.gen_runner.start_gen(
            self.config.gen_algorithm, 
            self.config.graph_height, 
            self.config.graph_width
        )
        self.solver_runner = SolverRunner()
        self.config.gen_start = False

    def start_solving(self):
        """Start a solving algorithm."""

        self.solver_runner.graph = self.gen_runner.get_graph()
        self.solver_runner.start_solve(self.config.solve_algorithm)
        self.config.solve_start = False

    def process_ticks(self):
        """Process the number of ticks as stated in self.config."""

        tick_interval = 1 / self.config.tick_rate
        while self.accumulated_time >= tick_interval:
            self.accumulated_time -= tick_interval
            self.solver_runner.handle_tick()
            self.gen_runner.handle_tick()

    def update_graph(self):
        """Gets the most recent version of the graph."""

        if self.gen_runner.generating:
            self.graph = self.gen_runner.get_graph()
        elif self.solver_runner.solving:
            self.graph = self.solver_runner.get_graph()

    def draw(self):
        """Draw all visual elements of the visualiser"""
        
        self.screen.fill((255, 255, 255))
        self.draw_algorithm_panel()
        self.draw_environment_panel()
        self.draw_graph_panel()

        self.config.update_screen_size(*self.screen.get_size())

    def draw_algorithm_panel(self):
        """Draw the algorithm selection panel."""

        self.drawer.draw_algorithm_panel(
            self.config.labels, 
            self.config.buttons, 
            self.config.ALGORITHM_PANEL_COLOUR, 
            self.config.ALGORITHM_PANEL_WIDTH, 
            self.config.ALGORITHM_PANEL_HEIGHT, 
            self.config.WINDOW_WIDTH, 
            self.config.WINDOW_HEIGHT
        )

    def draw_environment_panel(self):
        """Draw the environment information panel."""

        self.drawer.draw_environment_panel(
            self.gen_runner.state_info, 
            self.solver_runner.state_info, 
            self.config.ENVIRONMENT_PANEL_COLOUR, 
            self.config.ALGORITHM_PANEL_WIDTH, 
            self.config.GRAPH_PANEL_HEIGHT, 
            self.config.ENVIRONMENT_PANEL_WIDTH, 
            self.config.ENVIRONMENT_PANEL_HEIGHT
        )

    def draw_graph_panel(self):
        """Draw the maze graph panel."""

        self.drawer.draw_graph_panel(
            self.graph, 
            self.config.GRAPH_PANEL_COLOUR, 
            self.config.ALGORITHM_PANEL_WIDTH, 
            self.config.GRAPH_PANEL_WIDTH, 
            self.config.GRAPH_PANEL_HEIGHT, 
            self.config.WINDOW_WIDTH, 
            self.config.ALGORITHM_PANEL_WIDTH
        )
