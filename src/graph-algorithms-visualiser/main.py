import pygame
import sys
from util.config_manager import ConfigManager
from util.algorithm_runner import AlgorithmRunner
from util.drawer import Drawer

pygame.init()
pygame.display.set_caption("Graph Algorithms Visualiser")

runner = AlgorithmRunner()
config = ConfigManager()
screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.RESIZABLE)
drawer = Drawer(screen, pygame.font.SysFont("arial", 18))
clock = pygame.time.Clock()

def main():
    running = True

    while running:
        clock.tick(config.tick_rate)
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                config.handle_change_graph_size(event)
            
            for button in config.buttons:
                button.handle_event(event)
            
        if config.gen_start:
            runner.start_gen(config.gen_algorithm, config.graph_height, config.graph_width)
            config.gen_start = False

        if config.solve_start:
            runner.start_solve(config.solve_algorithm)
            config.solve_start = False

        runner.handle_tick()

        drawer.draw_algorithm_panel(config.labels, config.buttons, config.ALGORITHM_PANEL_COLOUR, 
                                    config.ALGORITHM_PANEL_WIDTH, config.ALGORITHM_PANEL_HEIGHT, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        drawer.draw_environment_panel(runner.generator_state_info, runner.solver_state_info, config.ENVIRONMENT_PANEL_COLOUR, config.ALGORITHM_PANEL_WIDTH, 
                                      config.GRAPH_PANEL_HEIGHT, config.ENVIRONMENT_PANEL_WIDTH, config.ENVIRONMENT_PANEL_HEIGHT)
        
        drawer.draw_graph_panel(runner.get_graph(), config.GRAPH_PANEL_COLOUR, config.ALGORITHM_PANEL_WIDTH, config.GRAPH_PANEL_WIDTH, 
                                config.GRAPH_PANEL_HEIGHT, config.WINDOW_WIDTH, config.ALGORITHM_PANEL_WIDTH)

        config.update_screen_size(*screen.get_size())

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
