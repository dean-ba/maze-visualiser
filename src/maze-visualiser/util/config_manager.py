import pygame
from util.button import Button
from util.enum import GenType
from util.enum import SolveType

class ButtonFactory:
    """Helper class to create buttons for the panels."""

    def __init__(self, font, button_colour, border_colour):
        self.font = font
        self.button_colour = button_colour
        self.border_colour = border_colour

    def create_button(self, x, y, width, height, text, callback):
        rect = (x, y, width, height)
        return Button(rect, text, callback, self.font, self.button_colour, self.border_colour)

class ConfigManager:
    """Class to handle all configuration for the project."""

    DEFAULT_WINDOW_WIDTH = 1000
    DEFAULT_WINDOW_HEIGHT = 800
    ALGORITHM_PANEL_WIDTH = 200
    ENVIRONMENT_PANEL_HEIGHT = 200

    COLOURS = {
        "graph_panel": (40, 40, 40),
        "algorithm_panel": (50, 50, 50),
        "environment_panel": (50, 50, 50),
        "button": (80, 80, 80),
        "button_border": (40, 40, 40)
    }

    def __init__(self, width = None, height = None):
        """Initialises the configuration manager with default values for the program."""

        self.window_width = width or self.DEFAULT_WINDOW_WIDTH
        self.window_height = height or self.DEFAULT_WINDOW_HEIGHT
        self.algorithm_panel_width = self.ALGORITHM_PANEL_WIDTH
        self.algorithm_panel_height = self.window_height
        self.environment_panel_width = self.window_width - self.algorithm_panel_width
        self.environment_panel_height = self.ENVIRONMENT_PANEL_HEIGHT
        self.graph_panel_width = self.environment_panel_width
        self.graph_panel_height = self.window_height - self.environment_panel_height

        self.gen_algorithm = GenType.BACKTRACKER
        self.solve_algorithm = SolveType.ASTAR
        self.gen_start = False
        self.solve_start = False
        self.tick_rate = 50
        self.graph_width = 21
        self.graph_height = 21

        self.font = pygame.font.SysFont("arial", 18)
        self.button_factory = ButtonFactory(self.font, self.COLOURS["button"], self.COLOURS["button_border"])

        self.algorithms = [
            (50, "Backtracker", self.set_backtracker),
            (100, "Eller", self.set_eller),
            (150, "Kruskal", self.set_kruskal),
            (200, "Prim", self.set_prim),
            (250, "Aldous-Broder", self.set_aldous_broder),
            (300, "Wilson", self.set_wilson),
            (380, "A*", self.set_astar),
            (430, "Dijkstra", self.set_dijkstra),
            (480, "Dead End Filler", self.set_dead_end_filler),
            (530, "Backtracker", self.set_backtracker_solver),
            (580, "Random Mouse", self.set_random_mouse)
        ]

        self.buttons = [self.button_factory.create_button(25, y, 150, 40, text, callback) for y, text, callback in self.algorithms]
        self.buttons += [
            self.button_factory.create_button(25, 650, 150, 40, f"Speed: {self.tick_rate}", self.cycle_tick_rate),
            self.button_factory.create_button(10, 700, 85, 40, "Generate", self.start_gen),
            self.button_factory.create_button(105, 700, 85, 40, "Solve", self.start_solve)
        ]

        self.labels = [
            ("Generation Algorithm", (15, 20)),
            ("Solving Algorithm", (30, 350)),
            (f"Width: {self.graph_width}", (50, 750)),
            (f"Height: {self.graph_height}", (50, 770)),
        ]
    
    def handle_change_graph_size(self, event):
        """Updates the graph size based on arrow key inputs."""

        match event.key:
            case pygame.K_DOWN:
                self.graph_height = max(3, self.graph_height - 2)
            case pygame.K_UP:
                self.graph_height += 2
            case pygame.K_LEFT:
                self.graph_width = max(3, self.graph_width - 2)
            case pygame.K_RIGHT:
                self.graph_width += 2
            case _:
                return
        self.labels[2] = (f"Width: {self.graph_width}", (50, 750))
        self.labels[3] = (f"Height: {self.graph_height}", (50, 770))

    def cycle_tick_rate(self):
        """Updates the generation speed when the tick rate button is pressed."""

        match self.tick_rate:
            case 1:
                self.tick_rate = 5
            case 5:
                self.tick_rate = 20
            case 20:
                self.tick_rate = 50
            case 50:
                self.tick_rate = 100
            case 100:
                self.tick_rate = 1
            case _:
                self.tick_rate = 1
        self.buttons[11] = self.button_factory.create_button(25, 650, 150, 40, f"Speed: {self.tick_rate}", self.cycle_tick_rate)

    def update_screen_size(self, width, height):
        """Dynamically updates panel sizes based on the new screen size. Option panels still require a minimum size to function correctly."""

        if width == self.window_width and height == self.window_height:
            return
        
        self.window_width = width
        self.window_height = height
        self.algorithm_panel_height = self.window_height
        self.environment_panel_width = self.window_width - self.algorithm_panel_width
        self.graph_panel_width = self.environment_panel_width
        self.graph_panel_height = self.window_height - self.environment_panel_height

    def set_backtracker(self):
        self.gen_algorithm = GenType.BACKTRACKER

    def set_eller(self):
        self.gen_algorithm = GenType.ELLER
    
    def set_kruskal(self):
        self.gen_algorithm = GenType.KRUSKAL

    def set_prim(self):
        self.gen_algorithm = GenType.PRIM
    
    def set_aldous_broder(self):
        self.gen_algorithm = GenType.ALDOUS_BRODER

    def set_wilson(self):
        self.gen_algorithm = GenType.WILSON

    def set_astar(self):
        self.solve_algorithm = SolveType.ASTAR

    def set_dijkstra(self):
        self.solve_algorithm = SolveType.DIJKSTRA

    def set_dead_end_filler(self):
        self.solve_algorithm = SolveType.DEAD_END_FILLER

    def set_backtracker_solver(self):
        self.solve_algorithm = SolveType.BACKTRACKER_SOLVER

    def set_random_mouse(self):
        self.solve_algorithm = SolveType.RANDOM_MOUSE

    def start_gen(self):
        self.gen_start = True

    def start_solve(self):
        self.solve_start = True
