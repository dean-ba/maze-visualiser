import pygame
from util.enum import NodeType

class Drawer:
    """
    Class to draw the algorithm panel and graph to the screen with provided values.
    """
    
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.text_colour = (255, 255, 255)

    def draw_algorithm_panel(self, labels, buttons, panel_colour, panel_width, panel_height):
        """Draws the panel containing options for generation and solving algorithms."""

        pygame.draw.rect(
            self.screen, 
            panel_colour, 
            (0, 
             0, 
             panel_width, 
             panel_height))

        for label in labels:
            self.screen.blit(self.font.render(label[0], True, self.text_colour), label[1])

        for button in buttons:
            button.draw(self.screen)
        
    def draw_environment_panel(self, gen_state_info, solve_state_info, colour, start_x, start_y, width, height):
        """Draws the environment panel containing generation and solving information that updates in real time."""

        pygame.draw.rect(
            self.screen, 
            colour, 
            (start_x, 
             start_y, 
             width, 
             height))
    
        for index, info_label in enumerate(gen_state_info, 1):
            self.screen.blit(
                self.font.render(info_label, True, self.text_colour), 
                (start_x + 10, start_y + (20 * index)))
        
        for index, info_label in enumerate(solve_state_info, 1):
            self.screen.blit(
                self.font.render(info_label, True, self.text_colour),
                (start_x + 250, start_y + (20 * index)))

    def draw_graph_panel(self, graph, colour, start_x, width, height, window_width, algorithm_panel_width):
        """Draws the graph centered on the graph panel."""

        pygame.draw.rect(
            self.screen, 
            colour, 
            (start_x, 
             0, 
             width, 
             height))
        
        if graph is None:
            return
        
        rows = len(graph)
        cols = len(graph[0])

        cell_size = min(width // (cols + 2), height // (rows + 2))

        left = ((window_width + algorithm_panel_width) / 2 - cols * cell_size / 2)
        top = (height / 2 - rows * cell_size / 2)

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
                    left + col * cell_size,
                    top + row * cell_size,
                    cell_size,
                    cell_size
                )
                pygame.draw.rect(self.screen, colour, rect)
