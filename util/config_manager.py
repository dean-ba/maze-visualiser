import pygame
from util.button import Button
from generator.backtracker import BacktrackerGenerator
from solver.astar import Astar



class ConfigManager:

    def __init__(self, set_backtracker, start_gen, set_astar, start_solve):
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 800
        self.SETTINGS_PANEL_WIDTH = 200
        self.GRAPH_PANEL_WIDTH = self.WINDOW_WIDTH - self.SETTINGS_PANEL_WIDTH
        self.GRAPH_INFO_PANEL_HEIGHT = 200
        self.GRAPH_PANEL_HEIGHT = self.WINDOW_HEIGHT - self.GRAPH_INFO_PANEL_HEIGHT
        self.BACKGROUND_COLOUR = (255, 255, 255)
        self.GRAPH_PANEL_COLOUR = (50, 50, 50)
        self.SETTINGS_PANEL_COLOUR = (40, 40, 40)
        self.WHITE = (255, 255, 255)

        self.tick_rate = 60
        self.font = pygame.font.SysFont("arial", 18)
        self.graph_width = 11
        self.graph_height = 11
        self.cell_size = min(self.GRAPH_PANEL_WIDTH // (self.graph_width), self.GRAPH_PANEL_HEIGHT // (self.graph_height))

        self.buttons = [
            Button((10, 50, 150, 40), "Backtracker", set_backtracker, self.font, self.WHITE),
            Button((10, 130, 150, 40), "A*", set_astar, self.font, self.WHITE),
            Button((10, 360, 150, 40), "Generate", start_gen, self.font, self.WHITE),
            Button((10, 410, 150, 40), "Solve", start_solve, self.font, self.WHITE),
        ]
    
    def select_backtracker(self):
        self.generation_algorithm = "Backtracker"
        print("backtracker")

    def select_astar(self):
        self.solving_algorithm = "A*"
        print("astar")

    def generate(self):
        if self.generation_algorithm == "Backtracker":
            self.generator = BacktrackerGenerator(self.graph_height, self.graph_width)
            self.cell_size = min(self.GRAPH_PANEL_WIDTH // (self.graph_width), self.GRAPH_PANEL_HEIGHT // (self.graph_height))
            self.generating = True
        print("generate")

    def solve(self):

        if self.solving_algorithm == "A*":
            self.solver = Astar(self.graph)
            self.solving = True
        print("solve")