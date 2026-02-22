import pygame
from util.node_type import NodeType

class Drawer:
    """
    Class to draw the settings panel and graph to the screen with provided values.
    """
    
    def __init__(self, screen, config, runner):
        self.screen = screen
        self.config = config
        self.runner = runner

    def draw_settings_panel(self):
        pygame.draw.rect(self.screen, self.config.SETTINGS_PANEL_COLOUR, (0, 0, self.config.SETTINGS_PANEL_WIDTH, self.config.WINDOW_HEIGHT))

        for label in self.config.labels:
            self.screen.blit(self.config.font.render(label[0], True, self.config.WHITE), label[1])

        for button in self.config.buttons:
            button.draw(self.screen)


    def draw_graph_panel(self, graph):
        """Draws the graph centered on the graph panel."""

        pygame.draw.rect(self.screen, self.config.GRAPH_PANEL_COLOUR, (self.config.SETTINGS_PANEL_WIDTH, 0, self.config.GRAPH_PANEL_WIDTH, self.config.WINDOW_HEIGHT))
        
        if graph is None:
            return
        
        rows = len(graph)
        cols = len(graph[0])

        left = ((self.config.WINDOW_WIDTH + self.config.SETTINGS_PANEL_WIDTH) / 2 - cols * self.runner.cell_size / 2)
        top = (self.config.WINDOW_HEIGHT / 2 - rows * self.runner.cell_size / 2)

        for row in range(rows):
            for col in range(cols):
                match graph[row][col]:
                    case NodeType.WALL:
                        colour = (0, 0, 0)
                    case NodeType.EMPTY:
                        colour = (255, 255, 255)
                    case NodeType.PATH:
                        colour = (255, 0, 0)
                    case NodeType.VISITED:
                        colour = (50, 50, 50)
                    case _:
                        colour = (255, 255, 255)

                rect = pygame.Rect(
                    left + col * self.runner.cell_size,
                    top + row * self.runner.cell_size,
                    self.runner.cell_size,
                    self.runner.cell_size
                )
                pygame.draw.rect(self.screen, colour, rect)
