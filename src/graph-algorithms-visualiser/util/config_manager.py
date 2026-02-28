import pygame
from util.button import Button
from util.enum import GenType
from util.enum import SolveType

class ConfigManager:
    """Class to handle all configuration for the project."""

    def __init__(self, WINDOW_WIDTH=1000, WINDOW_HEIGHT=800):
        """Initialises the configuration manager with default values for the program."""

        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.ALGORITHM_PANEL_WIDTH = 200
        self.ALGORITHM_PANEL_HEIGHT = self.WINDOW_HEIGHT
        self.ENVIRONMENT_PANEL_WIDTH = self.WINDOW_WIDTH - self.ALGORITHM_PANEL_WIDTH
        self.ENVIRONMENT_PANEL_HEIGHT = 200
        self.GRAPH_PANEL_WIDTH = self.ENVIRONMENT_PANEL_WIDTH
        self.GRAPH_PANEL_HEIGHT = self.WINDOW_HEIGHT - self.ENVIRONMENT_PANEL_HEIGHT
        self.GRAPH_PANEL_COLOUR = (40, 40, 40)
        self.ALGORITHM_PANEL_COLOUR = (50, 50, 50)
        self.ENVIRONMENT_PANEL_COLOUR = (50, 50, 50)
        self.BUTTON_COLOUR = (80, 80, 80)
        self.BUTTON_BORDER_COLOUR = (40, 40, 40)
        self.gen_algorithm = GenType.BACKTRACKER
        self.solve_algorithm = SolveType.ASTAR
        self.gen_start = False
        self.solve_start = False
        self.tick_rate = 50
        self.font = pygame.font.SysFont("arial", 18)
        self.graph_width = 21
        self.graph_height = 21

        self.buttons = [
            Button((25, 50, 150, 40), "Backtracker", self.set_backtracker, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
            Button((25, 100, 150, 40), "Eller", self.set_eller, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
            Button((25, 150, 150, 40), "Kruskal", self.set_kruskal, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
            Button((25, 200, 150, 40), "Blank", self.set_backtracker, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
            Button((25, 250, 150, 40), "Blank", self.set_backtracker, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
            Button((25, 300, 150, 40), "Blank", self.set_backtracker, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
            Button((25, 380, 150, 40), "A*", self.set_astar, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
            Button((25, 430, 150, 40), "Dijkstra", self.set_dijkstra, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
            Button((25, 480, 150, 40), "DEF", self.set_dead_end_filler, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
            Button((25, 530, 150, 40), "Blank", self.set_astar, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
            Button((25, 580, 150, 40), "Blank", self.set_astar, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
            Button((25, 650, 150, 40), f"Speed: {self.tick_rate}", self.cycle_tick_rate, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
            Button((10, 700, 85, 40), "Generate", self.start_gen, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
            Button((105, 700, 85, 40), "Solve", self.start_solve, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR),
        ]

        self.labels = [
            ("Generation Algorithm", (10, 20)),
            ("Solving Algorithm", (10, 350)),
            (f"Width: {self.graph_width}", (50, 750)),
            (f"Height: {self.graph_height}", (50, 770)),
        ]
    
    def handle_change_graph_size(self, event):
        """Updates the graph size based on arrow key inputs."""

        match event.key:
            case pygame.K_DOWN:
                self.graph_height -= 2 if self.graph_height > 3 else 0
            case pygame.K_UP:
                self.graph_height += 2
            case pygame.K_LEFT:
                self.graph_width -= 2 if self.graph_width > 3 else 0
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
        self.buttons[11] = Button((25, 650, 150, 40), f"Speed: {self.tick_rate}", self.cycle_tick_rate, self.font, self.BUTTON_COLOUR, self.BUTTON_BORDER_COLOUR)

    def update_screen_size(self, width, height):
        """Dynamically updates panel sizes based on the new screen size. Option panels still require a minimum size to function correctly."""

        if width == self.WINDOW_WIDTH and height == self.WINDOW_HEIGHT:
            return
        
        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height
        self.ALGORITHM_PANEL_HEIGHT = self.WINDOW_HEIGHT
        self.ENVIRONMENT_PANEL_WIDTH = self.WINDOW_WIDTH - self.ALGORITHM_PANEL_WIDTH
        self.GRAPH_PANEL_WIDTH = self.ENVIRONMENT_PANEL_WIDTH
        self.GRAPH_PANEL_HEIGHT = self.WINDOW_HEIGHT - self.ENVIRONMENT_PANEL_HEIGHT


    def set_backtracker(self):
        self.gen_algorithm = GenType.BACKTRACKER

    def set_eller(self):
        self.gen_algorithm = GenType.ELLER
    
    def set_kruskal(self):
        self.gen_algorithm = GenType.KRUSKAL

    def set_astar(self):
        self.solve_algorithm = SolveType.ASTAR

    def set_dijkstra(self):
        self.solve_algorithm = SolveType.DIJKSTRA

    def set_dead_end_filler(self):
        self.solve_algorithm = SolveType.DEAD_END_FILLER

    def start_gen(self):
        self.gen_start = True

    def start_solve(self):
        self.solve_start = True
