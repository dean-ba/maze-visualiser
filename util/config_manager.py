import pygame
from util.button import Button

class ConfigManager:

    def __init__(self, set_backtracker, start_gen, set_astar, start_solve):
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 800
        self.SETTINGS_PANEL_WIDTH = 200
        self.GRAPH_PANEL_WIDTH = self.WINDOW_WIDTH - self.SETTINGS_PANEL_WIDTH
        self.BACKGROUND_COLOUR = (255, 255, 255)
        self.GRAPH_PANEL_COLOUR = (50, 50, 50)
        self.SETTINGS_PANEL_COLOUR = (40, 40, 40)
        self.WHITE = (255, 255, 255)

        self.tick_rate = 60
        self.font = pygame.font.SysFont("arial", 18)
        self.graph_width = 11
        self.graph_height = 11
        self.cell_size = min(self.GRAPH_PANEL_WIDTH // (self.graph_width + 2), self.WINDOW_HEIGHT // (self.graph_height + 2))

        self.buttons = [
            Button((10, 50, 150, 40), "Backtracker", set_backtracker, self.font, self.WHITE),
            Button((10, 130, 150, 40), "A*", set_astar, self.font, self.WHITE),
            Button((10, 650, 150, 40), "Generate", start_gen, self.font, self.WHITE),
            Button((10, 700, 150, 40), "Solve", start_solve, self.font, self.WHITE),
        ]
    
    def handle_change_graph_size(self, event):
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
        self.cell_size = min(self.GRAPH_PANEL_WIDTH // (self.graph_width + 2), self.WINDOW_HEIGHT // (self.graph_height + 2))
