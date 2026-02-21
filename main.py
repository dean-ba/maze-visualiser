import pygame
import sys
from ui.button import Button
from generator.backtracker import BacktrackerGenerator

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
SETTINGS_PANEL_WIDTH = 200
GRAPH_PANEL_WIDTH = WINDOW_WIDTH - SETTINGS_PANEL_WIDTH

BACKGROUND_COLOUR = (255, 255, 255)
GRAPH_PANEL_COLOUR = (50, 50, 50)
SETTINGS_PANEL_COLOUR = (40, 80, 160)
WHITE = (255, 255, 255)

generation_algorithm = None
solving_algorithm = None
generator = None
generating = False
graph = None

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Graph Algorithms Visualiser")

font = pygame.font.SysFont("arial", 18)
clock = pygame.time.Clock()

def select_backtracker():
    global generation_algorithm
    generation_algorithm = "Backtracker"
    print("backtracker")

def select_astar():
    global solving_algorithm
    solving_algorithm = "A*"
    print("astar")

def generate():
    global generator, generating

    if generation_algorithm == "Backtracker":
        generator = BacktrackerGenerator(21, 21)
        generating = True
    print("generate")

def solve():
    print("solve")

buttons = [
    Button((10, 50, 150, 40), "Backtracker", select_backtracker, font, WHITE),
    Button((10, 130, 150, 40), "A*", select_astar, font, WHITE),
    Button((10, 360, 150, 40), "Generate", generate, font, WHITE),
    Button((10, 410, 150, 40), "Solve", solve, font, WHITE),
]

def draw_settings_panel():
    pygame.draw.rect(screen, SETTINGS_PANEL_COLOUR, (0, 0, SETTINGS_PANEL_WIDTH, WINDOW_HEIGHT))

    screen.blit(font.render("Generation Algorithm", True, WHITE), (10, 20))
    screen.blit(font.render("Solving Algorithm",    True, WHITE), (10, 100))
    screen.blit(font.render("Width:",               True, WHITE), (10, 580))
    screen.blit(font.render("Height:",              True, WHITE), (10, 510))

    for button in buttons:
        button.draw(screen)

def draw_graph_panel():
    pygame.draw.rect(screen, GRAPH_PANEL_COLOUR, (SETTINGS_PANEL_WIDTH, 0, GRAPH_PANEL_WIDTH, WINDOW_HEIGHT))
    cell_size = 20
    
    if graph is None:
        return
    
    rows = len(graph)
    cols = len(graph[0])
    margin = 0

    for row in range(rows):
        for col in range(cols):
            value = graph[row][col]
            if value == 1:       # wall
                color = (0, 0, 0)
            elif value == 0:     # path
                color = (255, 255, 255)
            elif value == 2:     # current cell (optional)
                color = (255, 0, 0)
            rect = pygame.Rect(
                SETTINGS_PANEL_WIDTH + col*cell_size + margin,
                row*cell_size + margin,
                cell_size - 2*margin,
                cell_size - 2*margin
            )
            pygame.draw.rect(screen, color, rect)

def main():
    global generation_algorithm, solving_algorithm, generator, generating, graph
    generation_algorithm = None
    solving_algorithm = None
    generator = None
    generating = False
    graph = None
    running = True

    while running:
        clock.tick(20)
        screen.fill(BACKGROUND_COLOUR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            for button in buttons:
                button.handle_event(event)

        if generating and generator:
            done = generator.step()
            graph = generator.grid

            if done:
                generating = False
                generator = None
        
        draw_settings_panel()
        draw_graph_panel()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
