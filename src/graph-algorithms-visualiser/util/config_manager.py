import pygame
from util.button import Button
from util.gen_type import GenType
from util.solve_type import SolveType

class ConfigManager:
    """Class to handle all configuration for the project."""

    def __init__(self, start_gen, start_solve, WINDOW_WIDTH=1000, WINDOW_HEIGHT=800, tick_rate=60):
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.ALGORITHM_PANEL_WIDTH = 200
        self.ALGORITHM_PANEL_HEIGHT = self.WINDOW_HEIGHT
        self.ENVIRONMENT_PANEL_WIDTH = self.WINDOW_WIDTH - self.ALGORITHM_PANEL_WIDTH
        self.ENVIRONMENT_PANEL_HEIGHT = 200
        self.GRAPH_PANEL_WIDTH = self.ENVIRONMENT_PANEL_WIDTH
        self.GRAPH_PANEL_HEIGHT = self.WINDOW_HEIGHT - self.ENVIRONMENT_PANEL_HEIGHT
        self.BACKGROUND_COLOUR = (255, 255, 255)
        self.GRAPH_PANEL_COLOUR = (50, 50, 50)
        self.ALGORITHM_PANEL_COLOUR = (40, 40, 40)
        self.ENVIRONMENT_PANEL_COLOUR = (40, 40, 40)
        self.WHITE = (255, 255, 255)
        self.gen_algorithm = GenType.BACKTRACKER
        self.solve_algorithm = SolveType.ASTAR

        self.tick_rate = tick_rate
        self.font = pygame.font.SysFont("arial", 18)
        self.graph_width = 21
        self.graph_height = 21
        self.cell_size = min(self.GRAPH_PANEL_WIDTH // (self.graph_width + 2), self.GRAPH_PANEL_HEIGHT // (self.graph_height + 2))

        self.buttons = [
            Button((10, 50, 150, 40), "Backtracker", self.set_backtracker, self.font, self.WHITE),
            Button((10, 100, 150, 40), "Blank", self.set_backtracker, self.font, self.WHITE),
            Button((10, 150, 150, 40), "Blank", self.set_backtracker, self.font, self.WHITE),
            Button((10, 200, 150, 40), "Blank", self.set_backtracker, self.font, self.WHITE),
            Button((10, 250, 150, 40), "Blank", self.set_backtracker, self.font, self.WHITE),
            Button((10, 300, 150, 40), "Blank", self.set_backtracker, self.font, self.WHITE),
            Button((10, 380, 150, 40), "A*", self.set_astar, self.font, self.WHITE),
            Button((10, 430, 150, 40), "Dijkstra", self.set_dijkstra, self.font, self.WHITE),
            Button((10, 480, 150, 40), "Blank", self.set_astar, self.font, self.WHITE),
            Button((10, 530, 150, 40), "Blank", self.set_astar, self.font, self.WHITE),
            Button((10, 580, 150, 40), "Blank", self.set_astar, self.font, self.WHITE),
            Button((10, 650, 150, 40), "Generate", start_gen, self.font, self.WHITE),
            Button((10, 700, 150, 40), "Solve", start_solve, self.font, self.WHITE),
        ]

        self.labels = [
            ("Generation Algorithm", (10, 20)),
            ("Solving Algorithm", (10, 350)),
            (f"Width: {self.graph_width}", (10, 750)),
            (f"Height: {self.graph_height}", (10, 770)),
        ]
    
    def handle_change_graph_size(self, event):
        match event.key:
            case pygame.K_DOWN:
                self.graph_height -= 2 if self.graph_height > 3 else 0
                self.labels[3] = (f"Height: {self.graph_height}", (10, 770))
            case pygame.K_UP:
                self.graph_height += 2
                self.labels[3] = (f"Height: {self.graph_height}", (10, 770))
            case pygame.K_LEFT:
                self.graph_width -= 2 if self.graph_width > 3 else 0
                self.labels[2] = (f"Width: {self.graph_width}", (10, 750))
            case pygame.K_RIGHT:
                self.graph_width += 2
                self.labels[2] = (f"Width: {self.graph_width}", (10, 750))
            case _:
                return
        self.cell_size = min(self.GRAPH_PANEL_WIDTH // (self.graph_width + 2), self.GRAPH_PANEL_HEIGHT // (self.graph_height + 2))

    def set_backtracker(self):
        self.gen_algorithm = GenType.BACKTRACKER

    def set_prim(self):
        self.gen_algorithm = GenType.PRIM

    def set_astar(self):
        self.solve_algorithm = SolveType.ASTAR

    def set_dijkstra(self):
        self.solve_algorithm = SolveType.DIJKSTRA
