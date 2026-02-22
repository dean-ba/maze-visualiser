import pygame
import sys
from util.node_type import NodeType
from util.config_manager import ConfigManager
from util.algorithm_runner import AlgorithmRunner

pygame.init()

runner = AlgorithmRunner()
config = ConfigManager(runner.set_backtracker, runner.start_gen, runner.set_astar, runner.start_solve)

screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
pygame.display.set_caption("Graph Algorithms Visualiser")

clock = pygame.time.Clock()

def draw_settings_panel():
    pygame.draw.rect(screen, config.SETTINGS_PANEL_COLOUR, (0, 0, config.SETTINGS_PANEL_WIDTH, config.WINDOW_HEIGHT))

    screen.blit(config.font.render("Generation Algorithm",     True, config.WHITE), (10, 20))
    screen.blit(config.font.render("Solving Algorithm",        True, config.WHITE), (10, 100))
    screen.blit(config.font.render(f"Width: {config.graph_width}",    True, config.WHITE), (10, 580))
    screen.blit(config.font.render(f"Height: {config.graph_height}",  True, config.WHITE), (10, 510))

    for button in config.buttons:
        button.draw(screen)

def handle_change_graph_size(event):

    match event.key:
        case pygame.K_DOWN:
            config.graph_height -= 2 if config.graph_height > 3 else 0
        case pygame.K_UP:
            config.graph_height += 2
        case pygame.K_LEFT:
            config.graph_width -= 2 if config.graph_width > 3 else 0
        case pygame.K_RIGHT:
            config.graph_width += 2
        case _:
            return


def draw_graph_panel(graph):
    pygame.draw.rect(screen, config.GRAPH_PANEL_COLOUR, (config.SETTINGS_PANEL_WIDTH, 0, config.GRAPH_PANEL_WIDTH, config.GRAPH_PANEL_HEIGHT))
    
    if graph is None:
        return
    
    rows = len(graph)
    cols = len(graph[0])

    left = ((config.WINDOW_WIDTH + config.SETTINGS_PANEL_WIDTH) / 2 - cols * config.cell_size / 2)
    top = (config.GRAPH_PANEL_HEIGHT / 2 - rows * config.cell_size / 2)

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
                left + col * config.cell_size,
                top + row * config.cell_size,
                config.cell_size,
                config.cell_size
            )
            pygame.draw.rect(screen, colour, rect)

def main():
    running = True

    while running:
        clock.tick(config.tick_rate)
        screen.fill(config.BACKGROUND_COLOUR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                handle_change_graph_size(event)
            
            for button in config.buttons:
                button.handle_event(event)

        runner.handle_tick()
        graph = runner.get_graph()

        draw_settings_panel()
        draw_graph_panel(graph)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
