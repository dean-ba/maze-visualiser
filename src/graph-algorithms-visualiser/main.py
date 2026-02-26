import pygame
import sys
from util.config_manager import ConfigManager
from util.algorithm_runner import AlgorithmRunner
from util.drawer import Drawer

pygame.init()
pygame.display.set_caption("Graph Algorithms Visualiser")

runner = AlgorithmRunner()
config = ConfigManager(
    runner.start_gen, 
    runner.start_solve,
    WINDOW_WIDTH=1000,
    WINDOW_HEIGHT=800, 
    tick_rate=100
    )
runner.config = config
clock = pygame.time.Clock()
screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.RESIZABLE)
drawer = Drawer(screen, pygame.font.SysFont("arial", 18))

def main():
    running = True
    graph = None

    while running:
        clock.tick(config.tick_rate)
        screen.fill(config.BACKGROUND_COLOUR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                config.handle_change_graph_size(event)
            
            for button in config.buttons:
                button.handle_event(event)

        runner.handle_tick()
        graph = runner.get_graph()

        drawer.draw_algorithm_panel(config.labels, config.buttons, config.ALGORITHM_PANEL_COLOUR, config.ALGORITHM_PANEL_WIDTH, config.ALGORITHM_PANEL_HEIGHT)
        drawer.draw_environment_panel(runner.generator_state_info, runner.solver_state_info, config.ENVIRONMENT_PANEL_COLOUR, config.ALGORITHM_PANEL_WIDTH, config.GRAPH_PANEL_HEIGHT, config.ENVIRONMENT_PANEL_WIDTH, config.ENVIRONMENT_PANEL_HEIGHT)
        drawer.draw_graph_panel(graph, config.GRAPH_PANEL_COLOUR, config.ALGORITHM_PANEL_WIDTH, config.GRAPH_PANEL_WIDTH, config.GRAPH_PANEL_HEIGHT, config.WINDOW_WIDTH, config.ALGORITHM_PANEL_WIDTH)

        # config.WINDOW_WIDTH, config.WINDOW_HEIGHT = screen.get_size() # for resizing window

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
