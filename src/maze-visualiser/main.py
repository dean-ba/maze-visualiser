import pygame
import sys
from util.config_manager import ConfigManager
from util.solver_runner import SolverRunner
from util.generator_runner import GeneratorRunner
from util.drawer import Drawer

pygame.init()
pygame.display.set_caption("Maze Algorithms Visualiser")

solver_runner = SolverRunner()
gen_runner = GeneratorRunner()
config = ConfigManager()
screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.RESIZABLE)
drawer = Drawer(screen, pygame.font.SysFont("arial", 18))
clock = pygame.time.Clock()

def main():
    accumulated_time = 0.0
    running = True
    graph = None

    while running:
        accumulated_time += clock.tick(60) / 1000
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                config.handle_change_graph_size(event)
            
            for button in config.buttons:
                button.handle_event(event)
            
        if config.gen_start:
            gen_runner.start_gen(config.gen_algorithm, config.graph_height, config.graph_width)
            config.gen_start = False

        if config.solve_start and not gen_runner.generating:
            solver_runner.graph = gen_runner.get_graph()
            solver_runner.start_solve(config.solve_algorithm)
            config.solve_start = False
        
        tick_interval = 1 / config.tick_rate
        while accumulated_time >= tick_interval:
            accumulated_time -= tick_interval
            solver_runner.handle_tick()
            gen_runner.handle_tick()

        if gen_runner.generating:
            graph = gen_runner.get_graph()
        elif solver_runner.solving:
            graph = solver_runner.get_graph()

        drawer.draw_algorithm_panel(config.labels, config.buttons, config.ALGORITHM_PANEL_COLOUR, 
                                    config.ALGORITHM_PANEL_WIDTH, config.ALGORITHM_PANEL_HEIGHT, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        drawer.draw_environment_panel(gen_runner.generator_state_info, solver_runner.solver_state_info, config.ENVIRONMENT_PANEL_COLOUR, config.ALGORITHM_PANEL_WIDTH, 
                                      config.GRAPH_PANEL_HEIGHT, config.ENVIRONMENT_PANEL_WIDTH, config.ENVIRONMENT_PANEL_HEIGHT)
        
        drawer.draw_graph_panel(graph, config.GRAPH_PANEL_COLOUR, config.ALGORITHM_PANEL_WIDTH, config.GRAPH_PANEL_WIDTH, 
                                config.GRAPH_PANEL_HEIGHT, config.WINDOW_WIDTH, config.ALGORITHM_PANEL_WIDTH)

        config.update_screen_size(*screen.get_size())

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
